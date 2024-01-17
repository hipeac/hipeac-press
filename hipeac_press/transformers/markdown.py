import re

from ..type_definitions import AuthorBio, BulletList, Header, Image, OrderedList, Paragraph, Quote
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
  text: >
    {prev['text']}
  link: {prev['link']}
"""
                if prev
                else "prev: false\n"
            )
            md += (
                f"""next:
  text: >
    {next['text']}
  link: {next['link']}
"""
                if next
                else "next: false\n"
            )
            md += "---\n\n\n"

        if with_badges:
            md += "<Badge type='info' text='DOI 2122 323' />&nbsp;"
            # md += f"<a href='./{slug}.pdf' target='_blank'><Badge type='danger' text='PDF' /></a>&nbsp;"
            md += "\n\n"

        figure_count = 0

        for element in self.document.elements:
            if isinstance(element, Header | Paragraph | Quote | BulletList | OrderedList):
                tom = element.to_markdown()
                if "### References" in tom:
                    continue
                md += tom + "\n"

            elif isinstance(element, Image):
                md += f"![]({element.path})"
                if element.caption:
                    figure_count += 1
                    caption = element.caption.to_markdown()
                    caption = caption[:-1] if caption.endswith("\n") else caption
                    md += f"\n*{caption}*"
                md += "\n\n"

        # Authors

        authors = []

        for element in self.document.elements:
            if isinstance(element, AuthorBio):
                authors.append(element)

        if authors:
            title = "Author" if len(authors) == 1 else "Authors"
            md += f"\n::: info {title.upper()}\n\n"

            for element in authors:
                md += element.to_markdown() + "\n"

            md += ":::\n\n"

        # References

        if self.document.references:
            md += "\n::: info REFERENCES\n\n"
            for idx, reference in enumerate(self.document.references):
                if reference.to_string() == "References":
                    continue
                md += f"[^{idx + 1}]: {reference.to_markdown()}"
            md += "\n:::\n\n"

        return md
