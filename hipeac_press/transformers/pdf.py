from pathlib import Path

from pdfino import Document as PdfDocument
from pdfino import Font, Margins, Style, Template

from hipeac_press.types import Header, Paragraph, Quote

from .base import Transformer


FONTS_PATH = Path(__file__).parent.parent.parent / "public" / "fonts"
HIPEAC_BLUE = "#005eb8"


class HipeacVisionTemplate(Template):
    """A custom PDFino template for the HiPEAC Vision articles."""

    margins = Margins(50, 100, 50, 100)
    font_size = 10
    fonts = [
        Font("Roboto", default=True, normal=FONTS_PATH / "Roboto-Regular.ttf", bold=FONTS_PATH / "Roboto-Bold.ttf"),
        Font("RobotoSlab", normal=FONTS_PATH / "RobotoSlab-Light.ttf", bold=FONTS_PATH / "RobotoSlab-SemiBold.ttf"),
    ]
    styles = [
        Style("body", options={"color": "#15141A"}),
        Style("p", options={"align": "justify", "margins": Margins(10, 0, 10, 0)}),
        Style(
            "h1",
            font_name="RobotoSlab-Bold",
            font_size=22,
            line_height=1.15,
            options={"color": "#222222", "margins": Margins(50, 30, 50, 0)},
        ),
    ]


class PdfTransformer(Transformer):
    """A transformer that converts a Document object into a PDF."""

    def get(self) -> bytes:
        """Return the PDF representation of a Document object.

        Returns:
            The PDF representation of the document as bytes.
        """
        pdf = PdfDocument(template=HipeacVisionTemplate())

        for element in self.document.elements:
            if isinstance(element, Header):
                if element.text == "References":
                    continue
                pdf.add_paragraph(element.text, style=f"h{element.level}")

            elif isinstance(element, Quote):
                pdf.p(element.text, options={"color": HIPEAC_BLUE})

            elif isinstance(element, Paragraph):
                pdf.p(element.text)

        return pdf.bytes
