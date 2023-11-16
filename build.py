import json
import os
from pathlib import Path
from shutil import rmtree

from hipeac_press.reader import Reader
from hipeac_press.transformers import MarkdownTransformer, PdfTransformer


PARENT = Path(__file__).parent
ORIGIN_FOLDER = os.environ.get("VISION_SOURCE_FOLDER", "./.source")
DESTINATION_FOLDER = "./.build"

origin_path = PARENT / ORIGIN_FOLDER
destination_path = PARENT / DESTINATION_FOLDER

reader = Reader(origin_path)

rmtree(destination_path, ignore_errors=True)
destination_path.mkdir(exist_ok=True)

for section in reader.tree:
    items = section["items"]

    for i, item in enumerate(items):
        if i > 0:
            item.prev = {
                "text": items[i - 1].title,
                "link": f"/{items[i - 1].slug}",
            }
        if i < len(items) - 1:
            item.next = {
                "text": items[i + 1].title,
                "link": f"/{items[i + 1].slug}",
            }

    for docx in items:
        # pdf
        pdf = PdfTransformer(docx.document).get()
        with open(f"{DESTINATION_FOLDER}/{docx.slug}.pdf", "wb") as pdf_file:
            pdf_file.write(pdf)

        md = MarkdownTransformer(docx.document).get(
            with_badges=True, with_frontmatter=True, prev=docx.prev, next=docx.next, slug=docx.slug
        )
        with open(f"{DESTINATION_FOLDER}/{docx.slug}.md", "w") as md_file:
            md_file.write(md)

        docx.copy_images(destination_path)

with open(f"{DESTINATION_FOLDER}/index.md", "w") as index_file, open(f"{ORIGIN_FOLDER}/index.md") as index_file_source:
    index_file.write(index_file_source.read())

with open(f"{DESTINATION_FOLDER}/sidebar.json", "w") as navigation_file:
    submenu = []
    for section in reader.tree:
        section["items"] = [{"text": docx.title, "link": docx.slug} for docx in section["items"]]
        submenu.append(section)
    navigation_file.write(json.dumps(submenu))

# copy public folder to .md folder
os.system(f"cp -r {PARENT}/public {DESTINATION_FOLDER}/public")
