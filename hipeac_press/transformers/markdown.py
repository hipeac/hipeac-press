import re

from ..types import Header, Image, ListParagraph, Paragraph, Quote
from .base import Transformer


def md_footnote(value: str) -> str:
    """Replace all square brackets that contain a number with square brackets with a caret in front.

    If add_colon is True, also add a colon after the number, for the first occurrence only.
    So: [12] becomes [^12]

    Args:
        value: The string to transform.

    Returns:
        The transformed string.
    """
    return re.sub(r"\[(\d+)\]", r"[^\1]", value)


class MarkdownTransformer(Transformer):
    """A transformer that converts a Document object into markdown."""

    def get(
        self,
        *,
        with_badges: bool = False,
        with_frontmatter: bool = False,
        prev: dict | None = None,
        next: dict | None,
        slug: str | None = None,
    ) -> str:
        """Return the markdown representation of a Document object.

        Args:
            with_badges: Whether to add badges for PDF and DOI. Defaults to False.
            with_frontmatter: Whether to add extra info as frontmatter. Defaults to False.
            prev: The previous document. Defaults to None.
            next: The next document. Defaults to None.
            slug: The slug of the document. Defaults to None.

        Returns:
            The markdown representation of the document.
        """
        md = ""

        if with_frontmatter:
            md += "---\n"
            md += f"title: >\n  {self.document.title}\n" if self.document.title else ""
            md += f"description: >\n  {self.document.description}\n" if self.document.description else ""
            md += (
                f"authors: {', '.join(author.name for author in self.document.authors)}\n"
                if self.document.authors
                else ""
            )
            md += f"keywords: {', '.join(self.document.keywords)}\n" if self.document.keywords else ""
            md += f"lastUpdated: {self.document.updated_at.isoformat()}\n"
            md += (
                f"""prev:
  text: {prev['text']}
  link: {prev['link']}
"""
                if prev
                else "prev: false\n"
            )
            md += (
                f"""next:
  text: {next['text']}
  link: {next['link']}
"""
                if next
                else "next: false\n"
            )
            md += "---\n\n\n"

        if with_badges:
            md += "<Badge type='info' text='DOI 2122 323' />&nbsp;"
            md += f"<a href='./{slug}.pdf' target='_blank'><Badge type='danger' text='PDF' /></a>\n\n"

        for element in self.document.elements:
            if isinstance(element, Header):
                md += "#" * element.level + " " + element.text + "\n\n"
            elif isinstance(element, Quote):
                md += "> " + md_footnote(element.text) + "\n\n"
            elif isinstance(element, Paragraph):
                if element.text == "References":
                    continue
                md += md_footnote(element.text) + "\n\n"
            elif isinstance(element, ListParagraph):
                for item in element.items:
                    bullet = f"{element.items.index(item) + 1}." if element.numbered else "-"
                    md += f"{bullet} " + md_footnote(item.paragraphs[0].text) + "\n"
                    for paragraph in item.paragraphs[1:]:
                        md += "  " + md_footnote(paragraph.text) + "\n"
                md += "\n"
            elif isinstance(element, Image):
                md += f'<img src="{element.path}" alt="{element.caption}">'
                if element.caption:
                    md += f"\n\n*{md_footnote(element.caption)}*"
                md += "\n\n"

        if self.document.authors:
            title = "Author" if len(self.document.authors) == 1 else "Authors"
            md += f"\n::: info {title}\n\n"

            for author in self.document.authors:
                if author.bio:
                    md += f"{author.bio}\n\n"
                else:
                    md += f"{author.name}\n\n"

            md += ":::\n\n"

        if self.document.references:
            md += "\n### References\n\n"
            for idx, reference in enumerate(self.document.references):
                md += f"[^{idx + 1}]: {reference.text}\n"

        return md
