import json
import os

from pathlib import Path
from shutil import rmtree

from press.reader import Reader
from press.transformers.markdown import MarkdownTransformer
from press.utils import slugify


PARENT = Path(__file__).parent
ORIGIN_FOLDER = os.environ.get("VISION_SOURCE_FOLDER", "./.source")
DESTINATION_FOLDER = "./.md"

origin_path = PARENT / ORIGIN_FOLDER
destination_path = PARENT / DESTINATION_FOLDER

reader = Reader(origin_path)

rmtree(destination_path, ignore_errors=True)
destination_path.mkdir(exist_ok=True)

for section in reader.tree:
    for docx in section["items"]:
        md = MarkdownTransformer(docx.document).get(with_frontmatter=True)
        with open(f"{DESTINATION_FOLDER}/{slugify(section['text'])}--{docx.slug}.md", "w") as md_file:
            md_file.write(md)
        docx.copy_images(destination_path)

with open(f"{DESTINATION_FOLDER}/index.md", "w") as index_file:
    with open(f"{ORIGIN_FOLDER}/index.md", "r") as index_file_source:
        index_file.write(index_file_source.read())

with open(f"{DESTINATION_FOLDER}/sidebar.json", "w") as navigation_file:
    submenu = []
    for section in reader.tree:
        section["items"] = [docx.to_submenu(slugify(section["text"])) for docx in section["items"]]
        submenu.append(section)
    navigation_file.write(json.dumps(submenu))