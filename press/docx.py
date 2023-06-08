from datetime import datetime
from defusedxml.ElementTree import parse
from pathlib import Path
from zipfile import ZipFile

from .types import Document, Header, Paragraph, Quote, ListParagraph, ListItem, Author, Image, Reference
from .utils import md_footnote, slugify


CP_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"
WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RELS_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/relationships}"
PIC_NAMESPACE = "{http://schemas.openxmlformats.org/drawingml/2006/picture}"
A_NAMESPACE = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
EMBED_NAMESPACE = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


class Docx:
    def __init__(self, docx_path: Path):
        self._docx_path = docx_path
        self.errors: list[str] = []
        self.filename = docx_path.name
        self.document = self._read_document()
        self._copy_images()

    def __repr__(self):
        return f"Docx({self.filename})"

    def _open_xml(self, path: str):
        with ZipFile(self._docx_path) as file:
            return parse(file.open(path))

    def _copy_images(self):
        pass

    def _read_document(self) -> Document:
        """
        Read the contents of a docx file and generate a Document object.
        """

        document_tree = self._open_xml("word/document.xml")
        metadata_tree = self._open_xml("docProps/core.xml")
        rels_tree = self._open_xml("word/_rels/document.xml.rels")

        try:
            title = metadata_tree.find(f"{DC_NAMESPACE}title").text.strip()
        except AttributeError:
            self.errors.append("No title found in metadata (File > Properties... > Summary)")
            title = None

        document = Document(title=title, updated_at=datetime.fromtimestamp(self._docx_path.stat().st_mtime))
        author_bios: list[str] = []

        for rel in rels_tree.iter(f"{RELS_NAMESPACE}Relationship"):
            if "relationships/image" in rel.attrib["Type"]:
                document.images[rel.attrib["Id"]] = f'./images/word/{rel.attrib["Target"]}'

        for el in document_tree.find(f"{WORD_NAMESPACE}body").iter():
            if el.find(f"{PIC_NAMESPACE}pic") is not None:
                for pic in el.iter(f"{PIC_NAMESPACE}pic"):
                    for blip in pic.iter(f"{A_NAMESPACE}blip"):
                        if blip.attrib[f"{EMBED_NAMESPACE}embed"] in document.images:
                            document.elements.append(Image(path=document.images[blip.attrib[f"{EMBED_NAMESPACE}embed"]]))

            if el.tag == f"{WORD_NAMESPACE}p":
                paragraph_style = el.find(f"{WORD_NAMESPACE}pPr/{WORD_NAMESPACE}pStyle")
                text = "".join([node.text for node in el.iter(f"{WORD_NAMESPACE}t") if node.text])

                use_class, kwargs = Paragraph, {}  # default

                if paragraph_style is not None:
                    style = paragraph_style.attrib[f"{WORD_NAMESPACE}val"]

                    if style.startswith("Heading"):
                        try:
                            level = int(style[len("Heading") :])
                        except ValueError:
                            level = 1
                        use_class, kwargs = Header, {"level": level}

                    elif style == "Quote":
                        use_class = Quote

                    elif style == "Reference":
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

        return document

    @property
    def images(self) -> list[Image]:
        return [element for element in self.document.elements if isinstance(element, Image)]

    @property
    def title(self) -> str:
        return self.document.title or self.long_title or self.filename

    @property
    def long_title(self) -> str | None:
        for element in self.document.elements:
            if isinstance(element, Header) and element.level == 1:
                return element.text
        return None

    @property
    def slug(self) -> str:
        return slugify(self.document.title or self.long_title or self.filename)

    @property
    def description(self) -> str | None:
        for element in self.document.elements:
            if isinstance(element, Quote):
                return element.text
        return None

    def to_markdown(self, *, with_frontmatter: bool = False) -> str:
        """
        Return current document as markdown.
        Add Frontmatter options if with_frontmatter is True.
        """

        md = ""

        if with_frontmatter:
            md += "---\n"
            md += f"title: >\n  {self.title}\n" if self.title else ""
            md += f"description: >\n  {self.description}\n" if self.description else ""
            md += (
                f"authors: {', '.join(author.name for author in self.document.authors)}\n"
                if self.document.authors
                else ""
            )
            md += f"keywords: {', '.join(self.document.keywords)}\n" if self.document.keywords else ""
            md += f"lastUpdated: {self.document.updated_at.isoformat()}\n"
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
                md += f"![{element.path}]({element.path})"
                if element.caption:
                    md += f"  \n*{md_footnote(element.caption)}*"
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
            md += "\n"
            for reference in self.document.references:
                md += f"{md_footnote(reference.text, True)}\n\n"

        return md

    def to_submenu(self, prefix: str = "") -> dict[str, str]:
        return {
            "text": self.title,
            "link": f"{prefix}--{self.slug}.md" if prefix else f"{self.slug}.md",
        }
