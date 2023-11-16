from datetime import datetime
from pathlib import Path

from pydantic import BaseModel


class Author(BaseModel):
    name: str
    bio: str | None = None


class Header(BaseModel):
    level: int
    text: str


class Paragraph(BaseModel):
    text: str


class InfoBox(Paragraph):
    pass


class Quote(Paragraph):
    pass


class Reference(Paragraph):
    pass


class Figure(BaseModel):
    caption: str | None = None


class Image(Figure):
    path: Path


class ListItem(BaseModel):
    paragraphs: list[Paragraph]


class ListParagraph(BaseModel):
    items: list[ListItem]
    numbered: bool = False


class Document(BaseModel):
    section: str | None = None
    title: str | None = None
    description: str | None = None
    authors: list[Author] = []
    elements: list[Header | Paragraph | Quote | Image | ListParagraph] = []
    keywords: list[str] = []
    references: list[Reference] = []
    images: dict[str, str] = {}
    updated_at: datetime | None = None
