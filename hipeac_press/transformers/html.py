import re
from pathlib import Path

import markdown2

from ..type_definitions import Image
from .markdown import MarkdownTransformer, process_text


def _process_urls(text) -> str:
    """Process URLs in text. Detect urls and make them clickable.

    :param text: The text to process.
    :return: The text with links processed.
    """
    url_regex = r"(https?://\S+)"
    urls = re.findall(url_regex, text)

    for url in urls:
        text = text.replace(url, f"<a href='{url}'>{url}</a>")

    return text


class HtmlTransformer(MarkdownTransformer):
    """A transformer that converts a Document object into HTML. Some elements use the markdown to HTML transformer."""

    @staticmethod
    def _image_to_html(element, v: int = 5) -> str:
        figure, figcaption = ("figure", "figcaption") if v == 5 else ("div", "small")
        img_path = "./images/" + str(Path(element.path).relative_to(Path(element.path).parents[1]))
        html = f"<{figure} class='figure image-block'>"
        html += f"<img src='{img_path}' />"
        if element.caption:
            html += f"<{figcaption} class='figcaption'>{process_text(element.caption)}</{figcaption}>"
        return f"{html}</{figure}>\n"

    def to_html(self, element) -> str:
        """Convert an element to HTML.

        :param element: The element to convert to HTML.
        :return: The HTML representation of the element.
        """
        md = self.to_markdown(element)
        return markdown2.markdown(md)

    def get_html(self, v: int = 5) -> str:
        """Return the HTML representation of a Document object.

        :return: The HTML representation of the document as a string.
        """
        html = ""
        samp = "samp" if v == 5 else "strong"

        for element in self.document.elements:
            if isinstance(element, Image):
                html += self._image_to_html(element, v) + "\n"
            else:
                html += self.to_html(element) + "\n"

        if self.document.references:
            for ref in self.document.references:
                html = html.replace(f"[{ref.code}]", f"<{samp}>[{ref.code}]</{samp}>")

        if self.document.references:
            html += "<div class='references-block'>" + "\n"
            html += "<h2 class='title'>References</h2>\n"
            html += "<ul class='references'>\n"

            for ref in self.document.references:
                html += f"<li><{samp}>{ref.code}:</{samp}> {_process_urls(ref.text)}</li>\n"

            html += "</ul>\n"
            html += "</div>\n"

        return html

    def get(self, v: int = 5) -> bytes:
        """Return the HTML representation of a Document object.

        :return: The HTML representation of the document as bytes.
        """
        return self.get_html(v).encode("utf-8")
