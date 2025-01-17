"""Type definitions for the hipeac_press package."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NavItem:
    """Represents a navigation item in the document."""

    text: str
    link: str


@dataclass
class Author:
    """Represents an author of the document."""

    name: str
    bio: str | None = None


@dataclass
class Paragraph:
    """Represents a paragraph in the document."""

    text: str


@dataclass
class Header:
    """Represents a header in the document."""

    level: int
    text: str


@dataclass
class BulletList:
    """Represents a bullet list in the document."""

    items: list[str]


@dataclass
class OrderedList:
    """Represents an ordered list in the document."""

    items: list[str]


@dataclass
class Quote:
    """Represents a quote in the document."""

    text: str
    ref: Paragraph | None = None


@dataclass
class Reference:
    """Represents a reference in the document."""

    code: str
    text: str


@dataclass
class InfoBox:
    """Represents an info box in the document."""

    text: str


@dataclass
class Image:
    """Represents an image in the document."""

    path: str
    caption: str | None = None


@dataclass
class Table:
    """Represents a table in the document."""

    headers: list[str]
    rows: list[list[str]]


@dataclass
class Document:
    """Represents the entire document."""

    slug: str
    title: str
    description: str | None = None
    authors: list[Author] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    elements: list[Paragraph | Header | BulletList | OrderedList | Quote | Reference | InfoBox | Image | Table] = field(
        default_factory=list
    )
    references: list[Reference] = field(default_factory=list)
    updated_at: datetime | None = None

    prev: NavItem | None = None
    next: NavItem | None = None
