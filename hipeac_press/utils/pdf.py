from io import BytesIO
from pathlib import Path

from pypdf import PageObject, PdfReader, PdfWriter
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg


def draw(article_title: str, num: int, vision_year: str, logo_path: str = None) -> PdfReader:
    """Generate a header for the PDFs.

    :param article_title: The title of the article.
    :param num: The number of the page.
    :param vision_year: The vision year.
    :param logo_path: The path to the logo image.
    """
    b = BytesIO()
    c = canvas.Canvas(b, pagesize=A4)
    pdfmetrics.registerFont(TTFont("Roboto Slab", "./public/fonts/RobotoSlab-Light.ttf"))
    c.setFont("Roboto Slab", 6)
    bottom_position = A4[1] - (28.45 * cm)
    left_margin = 4 * cm
    right_margin = A4[0] - (4 * cm)

    if num == 1 and logo_path:
        logo_width = 4 * cm
        logo_height = 4 * cm
        drawing = svg2rlg(logo_path)
        drawing.width = logo_width
        drawing.height = logo_height
        renderPDF.draw(drawing, c, left_margin, A4[1] - logo_height + 1.25 * cm)

    if num % 2 == 0:
        c.drawRightString(right_margin, bottom_position, article_title)
        c.drawString(left_margin, bottom_position, str(num))
    else:
        c.drawString(left_margin, bottom_position, f"HiPEAC Vision {vision_year} - Articles")
        c.drawRightString(right_margin, bottom_position, str(num))

    c.save()
    b.seek(0)

    return PdfReader(b)


def set_headers_footers(item, pdf_path: Path, vision_year: str, logo_path: str):
    """Set headers and footers for individual PDF files.

    :param item: The item to set headers and footers.
    :param pdf_path: The path where individual PDFs are stored.
    :param vision_year: The vision year.
    :param logo_path: The path to the logo image.
    """
    pdf_file_path = pdf_path / f"{item.slug}.pdf"
    pdf_reader = PdfReader(pdf_file_path)
    writer = PdfWriter()

    for i, page in enumerate(pdf_reader.pages, start=1):
        header_footer = draw(item.title, i, vision_year, logo_path)
        page.merge_page(header_footer.pages[0], True)
        writer.add_page(page)

    with open(pdf_file_path, "wb") as f:
        writer.write(f)


def concatenate_pdfs(tree, pdf_path: Path, vision_year: str, *, cover_pdf: Path | None = None):
    """Concatenate PDFs and add headers.

    :param tree: The tree structure containing sections and items.
    :param pdf_path: The path where individual PDFs are stored.
    :param vision_year: The vision year.
    :param cover_pdf: The path to the cover PDF file.
    """
    writer = PdfWriter()
    i = 0

    if cover_pdf:
        cover_reader = PdfReader(cover_pdf)
        for page in cover_reader.pages:
            i += 1
            writer.add_page(page)

    for _, section in enumerate(tree):
        for item in section["items"]:
            pdf_reader = PdfReader(pdf_path / f"{item.slug}.pdf")

            for page in pdf_reader.pages:
                i += 1
                page.merge_page(draw(item.title, i, vision_year).pages[0], True)
                writer.add_page(page)

            if len(pdf_reader.pages) % 2 == 1:
                i += 1
                blank_page = PageObject.create_blank_page(pdf_reader)
                blank_page.merge_page(draw(item.title, i, vision_year).pages[0], True)
                writer.add_page(blank_page)

    with BytesIO() as bytes_stream:
        writer.write(bytes_stream)
        bytes_stream.seek(0)

        with open(pdf_path / f"hipeac-vision-{vision_year}.pdf", "wb") as f:
            f.write(bytes_stream.read())
