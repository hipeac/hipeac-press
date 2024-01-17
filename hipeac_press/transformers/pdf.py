from pathlib import Path

from pdfino import Document as PdfDocument
from pdfino import Margins, mm
from reportlab.platypus import Frame, PageTemplate

<<<<<<< Updated upstream
from hipeac_press.type_definitions import Header, Paragraph, Quote
=======
from hipeac_press.type_definitions import AuthorBio, BulletList, Header, Image, OrderedList, Paragraph, Quote, Reference
>>>>>>> Stashed changes

from .base import Transformer
from .pdf_templates import FRONT_PAGE_PAD, HipeacVisionArticle


class PdfTransformer(Transformer):
    """A transformer that converts a Document object into a PDF."""

    def add_custom_templates(self, document: PdfDocument) -> None:
        """Add custom templates to a PDFino Document object.

        :param document: The PDFino Document object to add the templates to.
        """
        width, height = document.template.pagesize
        top_margin, right_margin, bottom_margin, left_margin = document.template.margins
        left_margin += FRONT_PAGE_PAD
        right_margin += FRONT_PAGE_PAD

        # Create a single-column layout for the first page
        first_page_frame = Frame(
            left_margin, bottom_margin, width - left_margin - right_margin, height - top_margin - bottom_margin
        )
        first_page_template = PageTemplate(id="first_page", frames=[first_page_frame])
        document.doc.pageTemplates.insert(0, first_page_template)
        return document

    def get(self, section: str | None) -> bytes:
        """Return the PDF representation of a Document object.

        :return: The PDF representation of the document as bytes.
        """
        pdf = HipeacVisionArticle(
            title=self.document.title,
            author="HiPEAC",
            outline=True,
        )
        pdf = self.add_custom_templates(pdf)
        pdf.use_template("first_page")

        first_paragraph_found = False
        first_author_found = False
        title = self.document.title
        pdf.set_section(section)
        pdf.set_title(self.document.title)

        for element in self.document.elements:
            if isinstance(element, Quote):
                pdf.add_svg(
                    str((Path(__file__).parent.parent.parent / "public" / "avatar.svg").absolute()), max_height=9 * mm
                )
                pdf.add_paragraph(element.to_html(), style="quote")
                pdf.use_template("main")

            elif isinstance(element, Header):
                pdf.add_header(element.to_html(), style=f"h{element.level}")
                if element.level == 1:
                    title = element.to_string()

            elif isinstance(element, AuthorBio):
                if not first_author_found:
                    pdf.add_paragraph(element.to_html(), style="authors")
                    first_author_found = True
                continue

            elif isinstance(element, Reference):
                print(element.to_html())
                pdf.add_paragraph(element.to_html(), style="reference")

            elif isinstance(element, Paragraph):
                try:
                    if isinstance(element, Paragraph) and not first_paragraph_found:
                        # first occurrence of paragraph should have a bigger font
                        first_paragraph_found = True
                        pdf.add_paragraph(element.to_html(), style="p_first")
                    else:
                        pdf.p(element.to_html())
                except Exception:
                    pdf.add_paragraph("ERROR", style="p")

            elif isinstance(element, BulletList):
                pdf.add_list_from_markdown(element.to_markdown(), style="ul")

            elif isinstance(element, OrderedList):
                pdf.add_list_from_markdown(element.to_markdown(), style="ol")

            elif isinstance(element, Image):
                pdf.add_spacer(10)
                pdf.add_image(
                    str(element.path.absolute()).replace("/hipeac-press/", "/hipeac-press/.build/"),
                    max_height=100 * mm,
                    keep_with_next=element.caption is not None,
                )
                if element.caption:
                    pdf.add_paragraph(element.caption.to_html(), style="caption")

        # add references

        if self.document.references:
            pdf.add_column_break()
            pdf.add_paragraph("References", style="h2", options={"color": "#333333"})

            for element in self.document.references:
                if element.to_string() == "References":
                    continue
                pdf.add_paragraph(element.to_html(), style="reference")

        # add final column with metadata

        pdf.add_column_break()
        authors = ""
        i = 0

        if len(self.document.authors) > 1:
            authors = ", ".join([author.name for author in self.document.authors[:-1]]) + " and "
            authors += self.document.authors[-1].name
        elif len(self.document.authors) == 1:
            authors = self.document.authors[0].name

        for element in self.document.elements:
            if isinstance(element, AuthorBio):
                i += 1
                if i == 1:
                    continue

                pdf.add_separator(
                    height=0.5 * mm,
                    options={"color": "#555555", "margins": Margins(10 * mm if i > 2 else 0, 0, 3 * mm, 0)},
                    keep_with_next=True,
                )
                pdf.add_paragraph(element.to_html(), style="author")

        pdf.add_separator(
            height=0.5 * mm,
            options={"color": "#555555", "margins": Margins(10 * mm, 0, 3 * mm, 0)},
            keep_with_next=True,
        )

        pdf.add_paragraph(
            "This document is part of the HiPEAC Vision available at "
            f"<a href='https://vision.hipeac.net/{self.docx.slug}.html'><strong>vision.hipeac.net</strong></a>.",
            style="p_metadata",
        )
        pdf.add_paragraph(
            f'Cite as: {authors}, "{title}". ' "In Marc Duranton et al., editors, HiPEAC Vision 2024, Jan 2024.",
            style="p_metadata",
        )
        pdf.add_paragraph(
            "The HiPEAC project has received funding from the European Union's Horizon Europe research and innovation "
            "funding programme under grant agreement number 101069836. Views and opinions expressed are however those "
            "of the author(s) only and do not necessarily reflect those either of the full HiPEAC community nor of the "
            "European Union. Neither the European Union nor the granting authority can be held responsible for them.",
            style="p_metadata",
        )
        pdf.add_paragraph("© 2024 HiPEAC", style="p_metadata")

        return pdf.bytes
