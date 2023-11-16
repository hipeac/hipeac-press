import re
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

from defusedxml.ElementTree import parse

from .types import Author, Document, Header, Image, InfoBox, ListItem, ListParagraph, Paragraph, Quote, Reference
from .utils import slugify


CP_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"
WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RELS_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/relationships}"
PIC_NAMESPACE = "{http://schemas.openxmlformats.org/drawingml/2006/picture}"
A_NAMESPACE = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
EMBED_NAMESPACE = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

BIBLIOGRAPHY_PATTERN = re.compile(r"\[(\d+)\] ")


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
        document_tree = self._open_xml("word/document.xml")
        metadata_tree = self._open_xml("docProps/core.xml")
        rels_tree = self._open_xml("word/_rels/document.xml.rels")

        document = Document(updated_at=datetime.fromtimestamp(self._docx_path.stat().st_mtime))
        author_bios: list[str] = []

        try:
            title = metadata_tree.find(f"{DC_NAMESPACE}title").text.strip()
        except AttributeError:
            self.errors.append("No title found in metadata (File > Properties... > Summary)")
            title = None

        for rel in rels_tree.iter(f"{RELS_NAMESPACE}Relationship"):
            if "relationships/image" in rel.attrib["Type"]:
                document.images[rel.attrib["Id"]] = rel.attrib["Target"]

        for el in document_tree.find(f"{WORD_NAMESPACE}body").iter():
            if el.find(f"{PIC_NAMESPACE}pic") is not None:
                for pic in el.iter(f"{PIC_NAMESPACE}pic"):
                    for blip in pic.iter(f"{A_NAMESPACE}blip"):
                        if blip.attrib[f"{EMBED_NAMESPACE}embed"] in document.images:
                            img_target = document.images[blip.attrib[f"{EMBED_NAMESPACE}embed"]]
                            document.elements.append(Image(path=f"./{self._img_folder}/word/{img_target}"))

            if el.tag == f"{WORD_NAMESPACE}p":
                paragraph_style = el.find(f"{WORD_NAMESPACE}pPr/{WORD_NAMESPACE}pStyle")
                text = "".join([node.text for node in el.iter(f"{WORD_NAMESPACE}t") if node.text])

                use_class, kwargs = Paragraph, {}  # default

                if paragraph_style is not None:
                    style = paragraph_style.attrib[f"{WORD_NAMESPACE}val"]

                    if style.startswith("Heading"):
                        if text == "References":
                            continue

                        try:
                            level = int(style[len("Heading") :])
                        except ValueError:
                            level = 1
                        use_class, kwargs = Header, {"level": level}

                    elif style == "Quote":
                        use_class = Quote

                    elif style == "InfoBox":
                        use_class = InfoBox

                    elif style == "Bibliography":
                        if BIBLIOGRAPHY_PATTERN.match(text):
                            continue
                        document.references.append(Reference(text=text))
                        continue

                    elif style == "Caption":
                        if isinstance(document.elements[-1], Image):
                            document.elements[-1].caption = text
                            continue

                    elif style in {"ListParagraph", "NumberedListParagraph"}:
                        if not isinstance(document.elements[-1], ListParagraph):
                            document.elements.append(
                                ListParagraph(items=[], numbered=(style == "NumberedListParagraph"))
                            )

                        # check if we are starting a new item, or if this is just another paragraph in the same item
                        if el.find(f"{WORD_NAMESPACE}pPr/{WORD_NAMESPACE}ind") is None:
                            document.elements[-1].items.append(ListItem(paragraphs=[]))

                        try:
                            document.elements[-1].items[-1].paragraphs.append(Paragraph(text=text))
                        except IndexError:
                            document.elements[-1].items.append(ListItem(paragraphs=[Paragraph(text=text)]))
                        continue

                    elif style == "Author":
                        author_bios.append(text)
                        continue

                if text:
                    document.elements.append(use_class(text=text, **kwargs))

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
            for element in document.elements:
                if isinstance(element, Header) and element.level == 1:
                    document.title = element.text

        for element in document.elements:
            if isinstance(element, Quote):
                document.description = element.text

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
                zip_file.extract(f"word/{img_target}", target_path / self._img_folder)

    def set_prev(self, dict):
        """Set the previous document in the tree."""
        self.prev = dict

    def set_next(self, dict):
        """Set the next document in the tree."""
        self.next = dict
