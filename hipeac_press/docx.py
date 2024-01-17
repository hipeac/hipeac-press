import re
import subprocess
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

import orjson
from defusedxml.ElementTree import parse
from PIL import Image as PILImage
from PIL import UnidentifiedImageError

from .type_definitions import (
    Author,
    AuthorBio,
    BulletList,
    Document,
    Header,
    Image,
    InfoBox,
    OrderedList,
    PandocElement,
    Paragraph,
    Quote,
    Reference,
)
from .utils import slugify


CP_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"
RELS_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/relationships}"

BIBLIOGRAPHY_PATTERN = re.compile(r"\[(\d+)\] ")


def style_from_div(div: dict) -> str | None:
    """Return a style from a Pandoc Div."""
    if div["t"] == "Div":
        try:
            return div["c"][0][2][0][1]
        except IndexError:
            return None
    return None


class Docx:
    """A class to represent a Word docx file as a Document object wrapper.

    Attributes:
        document (Document): The parsed document object.
        errors (list[str]): A list of errors encountered during parsing.
        filename (str): The filename of the docx file.
        section_name (str | None): The name of the section this document belongs to.
        prev (dict | None): The previous document in the tree.
        next (dict | None): The next document in the tree.
    """

    document: Document

    def __init__(
        self, docx_path: Path, *, section_name: str | None = None, prev: dict | None = None, next: dict | None = None
    ):
        self._docx_path = docx_path
        self._img_folder = uuid4().hex
        self._pandoc_obj: dict = {}
        self.errors: list[str] = []
        self.filename = docx_path.name
        self.section_name = section_name
        self.document = self._read_document()
        self.prev = prev
        self.next = next

    def __repr__(self):
        return f"Docx({self.filename})"

    def _open_xml(self, path: str):
        with ZipFile(self._docx_path) as file:
            return parse(file.open(path))

    def _read_document(self) -> Document:
        try:
            metadata_tree = self._open_xml("docProps/core.xml")
        except KeyError:
            self.errors.append("No metadata found (File > Properties... > Summary)")
            metadata_tree = None
        rels_tree = self._open_xml("word/_rels/document.xml.rels")

        document = Document(updated_at=datetime.fromtimestamp(self._docx_path.stat().st_mtime))
        author_bios: list[str] = []
        pandocjson = subprocess.run(
            ["pandoc", "--from=docx+citations+styles", "--to=json", "--quiet", str(self._docx_path)],
            capture_output=True,
        )

        if pandocjson.returncode == 0:
            self._pandoc_obj = orjson.loads(pandocjson.stdout)

        try:
            title = metadata_tree.find(f"{DC_NAMESPACE}title").text.strip()
        except AttributeError:
            self.errors.append(
                "No title found in metadata (File > Properties... > Summary). "
                "It will be used as shorter title in menus and navigation."
            )
            title = None

        for el in self._pandoc_obj["blocks"]:
            try:
                if el["t"] == "Para" and el["c"][0]["t"] == "Image":
                    document.elements.append(Image(path=f"./{self._img_folder}/word/{el['c'][0]['c'][2][0]}"))
                    continue
            except IndexError:
                pass

            t_classes = {
                "Author": AuthorBio,
                "Author (with title)": Paragraph,
                "Bibliography": Reference,
                "BulletList": BulletList,
                "InfoBox": InfoBox,
                "OrderedList": OrderedList,
                "Para": Paragraph,
                "Quote": Quote,
            }
            div_type = style_from_div(el) if el["t"] == "Div" else None

            if el["t"] == "Header":
                document.elements.append(Header(level=el["c"][0], data=[el]))
            elif div_type == "Author (with title)":
                document.elements.append(t_classes[div_type](data=[el]))
            elif div_type and div_type in {"Author", "Quote"}:
                document.elements.append(t_classes[div_type](data=[el["c"][1][0]]))
            elif div_type and div_type.lower() == "caption":
                if isinstance(document.elements[-1], Image):
                    document.elements[-1].caption = PandocElement(data=[el["c"][1][0]])
                    continue
            elif div_type and div_type == "Bibliography":
                document.references.append(t_classes[div_type](data=[el["c"][1][0]]))
            elif el["t"] in t_classes:
                if el["t"] == "Bibliography":
                    print("Bibliography found:", el["c"][1][0]["c"][0])
                document.elements.append(t_classes[el["t"]](data=[el]))
            continue

        for rel in rels_tree.iter(f"{RELS_NAMESPACE}Relationship"):
            if "relationships/image" in rel.attrib["Type"]:
                document.images[rel.attrib["Id"]] = rel.attrib["Target"]

        # -----
        # check metadata
        # -----

        try:
            for author in metadata_tree.find(f"{DC_NAMESPACE}creator").text.split(","):
                author_name = author.strip()
                try:
                    author_bio = next(author_bio for author_bio in author_bios if author_bio.startswith(author_name))
                except StopIteration:
                    author_bio = None
                document.authors.append(Author(name=author_name, bio=author_bio))
        except AttributeError:
            self.errors.append("No authors found in metadata (File > Properties... > Summary)")

        try:
            for keyword in metadata_tree.find(f"{CP_NAMESPACE}keywords").text.split(","):
                document.keywords.append(keyword.strip())
        except AttributeError:
            self.errors.append("No keywords found in metadata (File > Properties... > Summary)")

        # -----
        # add title and description
        # -----

        if title is not None:
            document.title = title
        else:
            document.title = self.filename
            for element in document.elements:
                if isinstance(element, Header) and element.level == 1:
                    document.title = element.to_string()

        # for element in document.elements:
        # if isinstance(element, Quote):
        # document.description = element.text

        return document

    @property
    def images(self) -> list[Image]:
        """Return a list of all images in the document."""
        return [element for element in self.document.elements if isinstance(element, Image)]

    @property
    def title(self) -> str:
        """Return the title of the document, or the filename if no title is found."""
        return self.document.title or self.filename

    @property
    def slug(self) -> str:
        """Return a slug based on the section name and the title of the document."""
        return f"{slugify(self.section_name or 'n')}--{slugify(self.document.title or self.filename)}"

    def copy_images(self, target_path: Path):
        """Open the docx zip file and move the images to the target path."""
        with ZipFile(self._docx_path) as zip_file:
            for _, img_target in self.document.images.items():
                try:
                    zip_file.extract(f"word/{img_target}", target_path / self._img_folder)
                except KeyError:
                    self.errors.append(f"Image {img_target} not found in docx file")
                    continue

                # check image resolution
                # column is 7.5 cm wide aprox., at 200 dpi that's 590px
                try:
                    img = PILImage.open(target_path / self._img_folder / f"word/{img_target}")

                    if img.width < 590:
                        for image in self.images:
                            if img_target in str(image.path):
                                caption = image.caption
                                caption_text = f" ({caption.to_string()[:15]}...)" if caption else ""
                                self.errors.append(f"Image {img_target} has low resolution{caption_text}")
                            else:
                                continue
                except UnidentifiedImageError:
                    pass

    def set_prev(self, dict):
        """Set the previous document in the tree."""
        self.prev = dict

    def set_next(self, dict):
        """Set the next document in the tree."""
        self.next = dict
