from datetime import datetime
from pathlib import Path

import orjson
import pypandoc
from pydantic import BaseModel


class PandocElement(BaseModel):
    """A Pandoc element."""

    data: list

    @property
    def json_str(self) -> str:
        """Return the json representation of the element."""
        return orjson.dumps({"pandoc-api-version": [1, 23, 1], "meta": {}, "blocks": self.data}).decode()

    def to_markdown(self) -> str:
        """Return the markdown representation of the element."""
        return pypandoc.convert_text(
            self.json_str,
            format="json",
            to="gfm-raw_attribute-raw_html+subscript+superscript",
            extra_args=["--wrap=none"],
        )

    def to_html(self) -> str:
        """Return the html representation of the element without styles."""
        return pypandoc.convert_text(
            self.json_str,
            format="json",
            to="html",
            extra_args=["--lua-filter", "pandoc_remove_attr.lua"],
        ).replace("<sub>", "<sub rise='2'>")

    def to_string(self) -> str:
        """Return the string representation of the element."""
        return pypandoc.convert_text(self.json_str, format="json", to="plain").strip()


class AuthorBio(PandocElement):
    """A paragraph with info about an author."""

    @property
    def name(self) -> str:
        """Return the name of the author, splitting ... is ..."""
        return self.to_markdown().split(" is ")[0]


class Author(BaseModel):
    """An author of a document."""

    name: str
    bio: str | None = None


class Header(PandocElement):
    """A header element."""

    level: int


class Paragraph(PandocElement):
    """A paragraph element."""


class InfoBox(Paragraph):
    """A custom paragraph element: info box."""


class Quote(PandocElement):
    """A custom paragraph element: quote."""


class BulletList(PandocElement):
    """A bullet list element."""


class OrderedList(PandocElement):
    """An ordered list element."""


class Reference(PandocElement):
    """A reference element."""


class Figure(BaseModel):
    """A figure element."""

    caption: PandocElement | None = None


class Image(Figure):
    """An image element."""

    path: Path


class Document(BaseModel):
    """A document."""

    section: str | None = None
    title: str | None = None
    description: str | None = None
    authors: list[Author] = []
    elements: list[Header | Paragraph | Quote | Image | BulletList | OrderedList] = []
    keywords: list[str] = []
    references: list[Reference] = []
    images: dict[str, str] = {}
    updated_at: datetime | None = None
