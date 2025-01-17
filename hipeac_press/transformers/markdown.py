"""Markdown transformer for the hipeac_press package."""

import re
from pathlib import Path

from ..type_definitions import BulletList, Header, Image, OrderedList, Paragraph, Quote, Table
from .base import Transformer


def _process_footnotes(text: str) -> str:
    """Convert references to footnotes.

    Converts:
    - [number] to [^number]
    - [text] to [^text]
    - [text1, text2] to [^text1][^text2]
    """
    # First pass: handle comma-separated references
    text = re.sub(
        r"\[([^\]]+(?:,\s*[^\]]+)+)\]", lambda m: "".join(f"[^{r.strip()}]" for r in m.group(1).split(",")), text
    )

    # Second pass: convert single numbered references
    text = re.sub(r"\[(\d+)\]", r"[^\1]", text)

    # Third pass: convert remaining single text references (but not image alt text)
    text = re.sub(r"\[([^\]^!][^\]]*)\]", r"[^\1]", text)

    return text


def _process_co2(text: str) -> str:
    """Convert CO2 and CO2e to CO<sub>2</sub> and CO<sub>2</sub>e."""
    text = re.sub(r"\bCO2e\b", "CO<sub>2</sub>e", text)
    text = re.sub(r"\bCO2\b", "CO<sub>2</sub>", text)
    return text


def process_text(text: str) -> str:
    """Process text for references and specific patterns."""
    text = _process_co2(text)
    return text


class MarkdownTransformer(Transformer):
    """A transformer that converts a Document object into markdown."""

    @staticmethod
    def _badges(document) -> str:
        md = f"<a href='./pdf/{document.slug}.pdf' target='_blank'><badge type='danger' text='PDF' /></a>"
        md += "\n\n"
        return md

    @staticmethod
    def _frontmatter(document) -> str:
        md = "---\n"
        md += f"title: >\n  {document.title}\n" if document.title else ""
        md += f"description: >\n  {document.description}\n" if document.description else ""
        md += f"authors: {', '.join(author.name for author in document.authors)}\n" if document.authors else ""
        md += f"keywords: {', '.join(document.keywords)}\n" if document.keywords else ""
        md += f"lastUpdated: {document.updated_at.isoformat()}\n"  # Use isoformat
        md += (
            f"""prev:
  text: >
    {document.prev.text}
  link: {document.prev.link}
"""
            if document.prev
            else "prev: false\n"
        )
        md += (
            f"""next:
  text: >
    {document.next.text}
  link: {document.next.link}
"""
            if document.next
            else "next: false\n"
        )
        md += "---\n\n\n"

        return md

    @staticmethod
    def _header_to_markdown(element):
        return f"{'#' * element.level} {element.text}\n"

    @staticmethod
    def _paragraph_to_markdown(element):
        # Process text in paragraph
        return process_text(element.text) + "\n"

    @staticmethod
    def _bullet_list_to_markdown(element):
        items = "\n".join(f"- {process_text(item)}" for item in element.items)
        return f"{items}\n"

    @staticmethod
    def _ordered_list_to_markdown(element):
        items = "\n".join(f"{i + 1}. {process_text(item)}" for i, item in enumerate(element.items))
        return f"{items}\n"

    @staticmethod
    def _quote_to_markdown(element):
        return f"> {process_text(element.text)}\n\n<small>{process_text(element.ref.text)}</small>\n"

    @staticmethod
    def _image_to_markdown(element):
        # Convert the path to be relative to the markdown file
        relative_path = "./images/" + str(Path(element.path).relative_to(Path(element.path).parents[1]))
        md = f"![]({relative_path})"
        if element.caption:
            md += f"  \n*{process_text(element.caption)}*"
        return f"{md}\n"

    @staticmethod
    def _table_to_markdown(element):
        header_row = "| " + " | ".join(element.headers) + " |"
        separator = "| " + " | ".join(["---"] * len(element.headers)) + " |"
        rows = "\n".join("| " + " | ".join(row) + " |" for row in element.rows)
        return f"{header_row}\n{separator}\n{rows}"

    @staticmethod
    def _info_box_to_markdown(element):
        return f"::: info\n\n{process_text(element.text)}\n\n:::"

    def to_markdown(self, element):
        """Convert an element to markdown format."""
        markdown_methods = {
            Header: self._header_to_markdown,
            Paragraph: self._paragraph_to_markdown,
            BulletList: self._bullet_list_to_markdown,
            OrderedList: self._ordered_list_to_markdown,
            Quote: self._quote_to_markdown,
            Image: self._image_to_markdown,
            Table: self._table_to_markdown,
        }

        element_type = type(element)

        if element_type in markdown_methods:
            return markdown_methods[element_type](element)

        return ""

    def get(
        self,
        *,
        with_badges: bool = True,
        with_frontmatter: bool = True,
    ) -> bytes:
        """Return the markdown representation of a Document object."""
        md = ""

        if with_frontmatter:
            md += self._frontmatter(self.document)

        if with_badges:
            md += self._badges(self.document)

        # Convert main content
        for element in self.document.elements:
            md += self.to_markdown(element) + "\n"

        md = _process_footnotes(md)

        # Add references as footnotes if they exist
        if self.document.references:
            md += "\n## References\n\n"

            for ref in self.document.references:
                md += f"[^{ref.code}]: {process_text(ref.text)}\n"

            md += "\n"

        return md.encode("utf-8")
