from pathlib import Path

from pdfino import Document, Font, Margins, Style, Template, mm
from pdfino.platypus import Canvas, CanvasSignal


FONTS_PATH = Path(__file__).parent.parent.parent / "public" / "fonts"
BASE_FONT_SIZE = 8.75
HIPEAC_BLUE = "#005eb8"
SIDE_MARGIN = 20 * mm
FRONT_PAGE_PAD = 15 * mm

REPORTLAB_INNER_FRAME_PADDING = 6


class FooterCanvas(Canvas):
    """A custom ReportLab canvas that adds page numbers to the bottom of each page."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_footer()
            super().showPage()
        super().save()

    def draw_footer(self):
        """Draw the footer on a page."""
        available_width = self._pagesize[0] - REPORTLAB_INNER_FRAME_PADDING - SIDE_MARGIN
        self.saveState()
        self.setFont("Roboto-Bold", 8)

        if self.page_number % 2:
            self.drawRightString(available_width, FRONT_PAGE_PAD, f"{self.page_number}")
            if self.page_number > 1:
                self.drawString(
                    REPORTLAB_INNER_FRAME_PADDING + SIDE_MARGIN, FRONT_PAGE_PAD, self.get_custom_var("title", "")
                )
        else:
            self.drawRightString(available_width, FRONT_PAGE_PAD, self.get_custom_var("section", ""))
            self.drawString(REPORTLAB_INNER_FRAME_PADDING + SIDE_MARGIN, FRONT_PAGE_PAD, f"{self.page_number}")

        self.restoreState()


class HipeacVisionTemplate(Template):
    """A custom PDFino template for the HiPEAC Vision articles."""

    margins = Margins(15 * mm, SIDE_MARGIN, 25 * mm, SIDE_MARGIN)
    columns = 2

    font_size = BASE_FONT_SIZE
    line_height = 1.45
    fonts = [
        Font(
            "Roboto",
            default=True,
            normal=FONTS_PATH / "Roboto-Regular.ttf",
            bold=FONTS_PATH / "Roboto-Bold.ttf",
            italic=FONTS_PATH / "Roboto-Italic.ttf",
        ),
        Font("RobotoSlab", normal=FONTS_PATH / "RobotoSlab-Regular.ttf", bold=FONTS_PATH / "RobotoSlab-SemiBold.ttf"),
    ]
    styles = [
        Style("body", options={"color": "#15141A"}),
        Style("p", options={"align": "justify", "margins": Margins(2.5 * mm, 0, 2.5 * mm, 0)}),
        Style("p_first", parent="p", font_size=BASE_FONT_SIZE + 1.25),
        Style("p_metadata", parent="p", font_name="RobotoSlab", options={"align": "left"}),
        Style(
            "h1",
            font_name="RobotoSlab-Bold",
            font_size=BASE_FONT_SIZE * 2.5,
            line_height=1.15,
            options={"color": "#222222", "margins": Margins(SIDE_MARGIN, FRONT_PAGE_PAD, 5 * mm, 0)},
        ),
        Style(
            "h2",
            font_name="Roboto-Bold",
            font_size=10,
            line_height=1.25,
            options={"color": HIPEAC_BLUE, "margins": Margins(7 * mm, 0, 4 * mm, 0)},
        ),
        Style("h3", options={"color": "#333333"}),
        Style(
            "quote",
            font_name="RobotoSlab",
            line_height=1.4,
            font_size=BASE_FONT_SIZE + 2,
            options={"color": HIPEAC_BLUE, "margins": Margins(0, -FRONT_PAGE_PAD, 0, 0)},
        ),
        Style(
            "caption",
            font_name="RobotoSlab",
            font_size=BASE_FONT_SIZE - 1,
            line_height=1.3,
            options={"align": "center", "color": "#555555", "margins": Margins(4 * mm, 7.5 * mm, 10 * mm, 7.5 * mm)},
        ),
        Style("authors", font_name="Roboto-Bold", options={"margins": Margins(0, 0, 15 * mm, 0)}),
        Style("author", font_name="RobotoSlab", font_size=BASE_FONT_SIZE + 1),
    ]


class HipeacVisionPrintedTemplate(Template):
    """A custom PDFino template for the HiPEAC Vision articles when printed."""

    margins = Margins(15 * mm, SIDE_MARGIN, 25 * mm, SIDE_MARGIN)
    columns = 2

    font_size = BASE_FONT_SIZE + 1.5
    line_height = 1.4
    fonts = [
        Font("RobotoSlab", normal=FONTS_PATH / "RobotoSlab-Regular.ttf", bold=FONTS_PATH / "RobotoSlab-SemiBold.ttf"),
        Font(
            "Roboto",
            normal=FONTS_PATH / "Roboto-Regular.ttf",
            bold=FONTS_PATH / "Roboto-Bold.ttf",
            italic=FONTS_PATH / "Roboto-Italic.ttf",
        ),
        Font(
            "Garamond",
            default=True,
            normal=FONTS_PATH / "EBGaramond-Medium.ttf",
            bold=FONTS_PATH / "EBGaramond-SemiBold.ttf",
            italic=FONTS_PATH / "EBGaramond-MediumItalic.ttf",
        ),
    ]
    styles = [
        Style("body", options={"color": "#15141A"}),
        Style("p", options={"align": "justify", "margins": Margins(2.5 * mm, 0, 2.5 * mm, 0)}),
        Style("p_first", parent="p", font_size=BASE_FONT_SIZE + 2.5),
        Style("p_metadata", parent="p", font_name="Roboto", font_size=BASE_FONT_SIZE - 1, options={"align": "left"}),
        Style(
            "h1",
            font_name="RobotoSlab-Bold",
            font_size=BASE_FONT_SIZE * 3,
            line_height=1.2,
            options={"color": "#222222", "margins": Margins(SIDE_MARGIN, FRONT_PAGE_PAD, 5 * mm, 0)},
        ),
        Style(
            "h2",
            font_name="Roboto-Bold",
            font_size=BASE_FONT_SIZE + 2,
            line_height=1.25,
            options={"color": HIPEAC_BLUE, "margins": Margins(7 * mm, 0, 4 * mm, 0)},
        ),
        Style("h3", parent="h2", font_size=BASE_FONT_SIZE + 1, options={"color": "#333333", "margin_top": 5 * mm}),
        Style(
            "quote",
            font_name="RobotoSlab",
            line_height=1.4,
            font_size=BASE_FONT_SIZE + 3,
            options={"color": HIPEAC_BLUE, "margins": Margins(0, -FRONT_PAGE_PAD, 0, 0)},
        ),
        Style(
            "caption",
            font_name="Garamond-Italic",
            font_size=BASE_FONT_SIZE - 1,
            line_height=1.3,
            options={"align": "center", "color": "#333333", "margins": Margins(4 * mm, 5 * mm, 10 * mm, 5 * mm)},
        ),
        Style("authors", font_name="Garamond-Bold", options={"margins": Margins(0, 0, 15 * mm, 0)}),
        Style("author", font_name="Roboto", font_size=BASE_FONT_SIZE + 2),
        Style(
            "reference",
            font_size=BASE_FONT_SIZE - 1.5,
            line_height=1.35,
            options={"align": "left", "margins": Margins(1.5 * mm, 0, 1.5 * mm, 0)},
        ),
    ]


class HipeacVisionArticle(Document):
    template_class = HipeacVisionPrintedTemplate
    canvas_class = FooterCanvas

    def set_section(self, section: str) -> None:
        self.add(CanvasSignal("section", section))

    def set_title(self, title: str) -> None:
        self.add(CanvasSignal("title", title))
