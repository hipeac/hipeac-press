from pathlib import Path

from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration

from ..type_definitions import Document
from .html import HtmlTransformer


CURRENT_PATH = Path(__file__).parent


class PdfTransformer(HtmlTransformer):
    """A transformer that converts a Document object into a PDF starting from a HTML."""

    def __init__(self, document: Document, image_path: Path):
        """Initialize the transformer with a document.

        :param document: The document to transform.
        :param image_path: The path to the images.
        """
        self.document = document
        self.image_path = image_path

    def _setup_pdf_template(self):
        """Set up the PDF template."""
        self.font_config = FontConfiguration()
        self.stylesheets = [
            CSS(filename=CURRENT_PATH / "pdf" / "pdf.css", font_config=self.font_config),
        ]

    def get(self, section: str | None) -> bytes:
        """Return the PDF representation of a Document object.

        :return: The PDF representation of the document as bytes.
        """
        self._setup_pdf_template()

        html = self.get_html()
        pdf_writer = HTML(string=html, base_url=self.image_path)
        pdf = pdf_writer.write_pdf(stylesheets=self.stylesheets, font_config=self.font_config)

        return pdf
