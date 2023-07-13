import re

from ..types import Header, Paragraph, Quote, ListParagraph, ListItem, Author, Image, Reference
from .base import Transformer


def md_footnote(value: str) -> str:
    """
    Replace all square brackets that contain a number with square brackets with a caret in front.
    If add_colon is True, also add a colon after the number, for the first occurrence only.
    So: [12] becomes [^12]
    """

    return re.sub(r"\[(\d+)\]", r"[^\1]", value)


class MarkdownTransformer(Transformer):
    """
    A transformer that converts a document into Markdown.
    """

    def get(self, *, with_frontmatter: bool = False, prev: dict | None = None, next: dict | None) -> str:
        """
        Transform the document into Markdown.
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
            md += f"""prev:
  text: {prev['text']}
  link: {prev['link']}
""" if prev else "prev: false\n"
            md += f"""next:
  text: {next['text']}
  link: {next['link']}
""" if next else "next: false\n"
            md += "---\n\n\n"

        for element in self.document.elements:
            if isinstance(element, Header):
                if element.text == "References":
                    continue
                md += "#" * element.level + " " + element.text + "\n\n"
            elif isinstance(element, Quote):
                md += "> " + md_footnote(element.text) + "\n\n"
            elif isinstance(element, Paragraph):
                md += md_footnote(element.text) + "\n\n"
            elif isinstance(element, ListParagraph):
                for item in element.items:
                    if element.numbered:
                        bullet = f"{element.items.index(item) + 1}."
                    else:
                        bullet = "-"
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
