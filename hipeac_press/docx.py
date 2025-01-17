import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from docx import Document as DocxDocument
from docx.oxml.ns import qn

from .transformers.markdown import MarkdownTransformer
from .transformers.pdf import PdfTransformer
from .type_definitions import Author, BulletList, Document, Header, Image, NavItem, OrderedList, Paragraph
from .utils import slugify


class DocxConverter:
    """A class to convert DOCX files to a structured document format."""

    def __init__(
        self,
        docx_path: Path,
        *,
        img_folder: Path,
        metadata_path: Path = None,
        section_name: str = None,
        prev: NavItem | None = None,
        next: NavItem | None = None,
    ):
        """Initialize the DocxConverter with paths and metadata.

        :param docx_path: Path to the DOCX file.
        :param img_folder: Directory to save images.
        :param metadata_path: Path to the metadata JSON file.
        """
        self._docx_path = docx_path
        self._docx = DocxDocument(docx_path)
        self.errors = []  # Add error tracking

        self.img_folder = self._generate_img_folder(img_folder)
        self.metadata = self._read_metadata(metadata_path)
        self.document = self._create_document(prev=prev, next=next)

        self.section_name = section_name

    def _generate_img_folder(self, base_folder: Path) -> Path:
        """Generate a unique image directory based on the DOCX path.

        :param base_folder: Base directory for images.
        :returns: The generated image directory.
        """
        base_folder.mkdir(parents=True, exist_ok=True)  # Ensure the base directory exists
        hash_object = hashlib.md5(str(self._docx_path).encode())
        img_folder = base_folder / hash_object.hexdigest()
        img_folder.mkdir(parents=True, exist_ok=True)

        return img_folder

    def _read_metadata(self, metadata_path: Path) -> dict:
        """Read metadata from a JSON file or the DOCX core properties.

        :param metadata_path: Path to the metadata JSON file.
        :returns: The metadata dictionary.
        """
        core_properties = self._docx.core_properties
        metadata = {
            "title": core_properties.title,
            "authors": core_properties.author.split(",") if core_properties.author else [],
            "keywords": core_properties.keywords.split(",") if core_properties.keywords else [],
        }

        if metadata_path and metadata_path.exists():
            with open(metadata_path) as file:
                json_metadata = json.load(file)
                metadata.update(json_metadata)

        return metadata

    def _save_image(self, run) -> Path | None:
        """Save an image from the DOCX run to the image directory.

        :param run: The DOCX run containing the image.
        :returns: The path to the saved image or None if the image cannot be saved.
        """
        blip = run._element.xpath(".//a:blip")[0]
        rId = blip.get(qn("r:embed"))
        image_part = self._docx.part.related_parts[rId]
        image_filename = Path(image_part.partname).name

        # Skip EMF and WMF files
        for ext in [".emf", ".wmf"]:
            if image_filename.lower().endswith(ext):
                self.errors.append(f"{ext} image format not supported: {image_filename}")
                return None

        img_path = self.img_folder / image_filename

        try:
            with open(img_path.absolute(), "wb") as img_file:
                img_file.write(image_part.blob)
        except Exception as e:
            self.errors.append(f"Failed to save image {image_filename}: {e}")
            return None

        return img_path

    def _convert_run_text(self, run) -> str:
        """Convert a run's text with its formatting.

        :param run: The DOCX run to convert.
        :returns: The formatted text.
        """
        text = run.text
        if text.strip():
            if run.bold and run.italic:
                text = f"**_{text}_**"
            elif run.bold:
                text = f"**{text}**"
            elif run.italic:
                text = f"_{text}_"
        return text

    def _consolidate_formatting(self, text: str) -> str:
        """Consolidate adjacent formatting markers and trim results."""
        # First, consolidate simple adjacent markers
        text = re.sub(r"\*\*([^*]+)\*\*\*\*([^*]+)\*\*", r"**\1\2**", text)
        text = re.sub(r"_([^_]+)__([^_]+)_", r"_\1\2_", text)

        # Then handle more complex patterns
        # Find all bold sections and consolidate them
        while True:
            # Look for adjacent bold sections like "**abc****def**"
            pattern = r"\*\*[^*]+\*\*\*\*[^*]+\*\*"
            match = re.search(pattern, text)
            if not match:
                break

            # Extract the content between ** markers
            section = match.group(0)
            content = re.findall(r"\*\*([^*]+)\*\*", section)
            # Combine the content and wrap in single **
            combined = f"**{''.join(content)}**"
            # Replace the original section with the combined version
            text = text.replace(section, combined)

        # Trim spaces inside formatting markers
        text = re.sub(r"\*\*\s*([^*]+?)\s*\*\*", r"**\1**", text)
        text = re.sub(r"_\s*([^_]+?)\s*_", r"_\1_", text)

        return text

    def _convert_paragraphs(self):
        """Convert paragraphs in the DOCX to structured document elements."""
        elements = []
        references = []
        in_references_section = False
        current_list_items = []
        current_list_type = None

        for i, para in enumerate(self._docx.paragraphs):
            # Check if we're in the references section
            if para.text.strip().lower() == "references":
                in_references_section = True
                continue

            # If we're in references section, collect references
            if in_references_section:
                if para.text.strip():
                    references.append(Paragraph(text=para.text.strip()))
                continue

            # Check for lists using both style name and XML structure
            is_list = (
                para.style.name == "ListParagraph"  # Most common Word style for lists
                or para.style.name.lower().startswith(("list", "bullet"))  # Other list styles
                or (para._p.pPr is not None and para._p.pPr.numPr is not None)  # Check XML structure for numbering
            )

            if is_list:
                # Determine list type from the XML structure
                if not current_list_type:
                    current_list_type = "bullet"  # Default to bullet lists
                current_list_items.append(para.text.strip())
                continue
            else:
                # Not a list item - flush any pending list
                if current_list_items:
                    if current_list_type == "bullet":
                        elements.append(BulletList(items=current_list_items))
                    else:
                        elements.append(OrderedList(items=current_list_items))
                    current_list_items = []
                    current_list_type = None

            # Check for headers
            if para.style.name.startswith("Heading"):
                level = int(para.style.name.replace("Heading ", "")) or 1
                elements.append(Header(level=level, text=para.text.strip()))
                continue

            # Normal paragraph processing
            paragraph_elements = []
            formatted_text = ""

            for run in para.runs:
                if run._element.xpath(".//a:blip"):
                    # Handle image
                    img_path = self._save_image(run)
                    if img_path:
                        if formatted_text.strip():
                            # Consolidate formatting before creating paragraph
                            formatted_text = self._consolidate_formatting(formatted_text.strip())
                            paragraph_elements.append(Paragraph(text=formatted_text))
                            formatted_text = ""
                        caption = None
                        if i + 1 < len(self._docx.paragraphs) and self._docx.paragraphs[i + 1].style.name == "Caption":
                            caption = self._docx.paragraphs[i + 1].text
                        paragraph_elements.append(Image(path=img_path, caption=caption))
                else:
                    # Handle formatted text
                    formatted_text += self._convert_run_text(run)

            if formatted_text.strip() and para.style.name != "Caption":
                # Consolidate formatting before creating paragraph
                formatted_text = self._consolidate_formatting(formatted_text.strip())
                paragraph_elements.append(Paragraph(text=formatted_text))

            elements.extend(paragraph_elements)

        # Flush any remaining list
        if current_list_items:
            if current_list_type == "bullet":
                elements.append(BulletList(items=current_list_items))
            else:
                elements.append(OrderedList(items=current_list_items))

        return elements, references

    def _create_document(self, *, prev: NavItem | None = None, next: NavItem | None = None) -> Document:
        """Create a structured document from the DOCX content."""
        elements, references = self._convert_paragraphs()
        doc = Document(
            title=self.metadata.get("title", ""),
            authors=[Author(name=author) for author in self.metadata.get("authors", [])],
            keywords=self.metadata.get("keywords", []),
            updated_at=datetime.now(),
            prev=prev,
            next=next,
            references=references,  # Add references to the document
        )
        doc.elements.extend(elements)
        return doc

    def export(self, format: str = "md", **kwargs) -> bytes:
        """Export the structured document using the specified transformer.

        :param transformer: The transformer to use for exporting.
        :returns: The transformed document as a string.
        """
        if format == "md":
            return MarkdownTransformer(self.document).get()
        elif format == "pdf":
            return PdfTransformer(self.document).get(section=kwargs.get("section"))
        else:
            raise ValueError(f"Unsupported format: {format}")

    @property
    def title(self) -> str:
        """Return the title of the document, or the filename if no title is found."""
        return self.document.title or self._docx_path.stem

    @property
    def slug(self) -> str:
        """Return a slug based on the section name and the title of the document."""
        return f"{slugify(self.section_name or 'n')}--{slugify(self.title)}"

    def set_prev(self, prev: NavItem):
        """Set the previous document in the tree."""
        self.document.prev = prev

    def set_next(self, next: NavItem):
        """Set the next document in the tree."""
        self.document.next = next
