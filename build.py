import os
from pathlib import Path
from shutil import rmtree

import orjson

from hipeac_press.reader import Reader
from hipeac_press.transformers import MarkdownTransformer


PARENT = Path(__file__).parent
VISION_PATH = os.environ.get(
    "VISION_SOURCE_PATH",
    "/Users/eillarra/Nextcloud/hipeac/Vision/2024/HiPEAC_Vision_24/02 Articles/Website",
)
ORIGIN_FOLDER = "./.source"
DESTINATION_FOLDER = "./.build"

origin_path = PARENT / ORIGIN_FOLDER
destination_path = PARENT / DESTINATION_FOLDER

rmtree(origin_path, ignore_errors=True)
origin_path.mkdir(exist_ok=True)
os.system(f'cp -r "{VISION_PATH}"/* "{origin_path}"')

tree = Reader(origin_path).tree

rmtree(destination_path, ignore_errors=True)
destination_path.mkdir(exist_ok=True)

for section in tree:
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
        docx.copy_images(destination_path)
        docx_folder = str(docx._docx_path.parent).replace(str(origin_path), str(VISION_PATH))

        # make markdown file
        md = MarkdownTransformer(docx).get(
            with_badges=False, with_frontmatter=True, prev=docx.prev, next=docx.next, slug=docx.slug
        )
        with open(f"{DESTINATION_FOLDER}/{docx.slug}.md", "w") as md_file:
            md_file.write(md)

        # make pdf file and save it both on the .build folder and the original folder (replacing the old one)
        # original folder is the folder where the processed docx file is located
        """
        pdf = PdfTransformer(docx).get(section=section["text"])
        with open(f"{DESTINATION_FOLDER}/{docx.slug}.pdf", "wb") as pdf_file:
            pdf_file.write(pdf)
        with open(f"{docx_folder}/{docx.slug}.pdf", "wb") as pdf_file:
            pdf_file.write(pdf)
        """

        # print errors in txt
        try:
            os.remove(f"{docx_folder}/ISSUES.txt")
        except FileNotFoundError:
            pass

        if docx.errors:
            with open(f"{docx_folder}/ISSUES.txt", "w") as txt_file:
                txt_file.write("\n".join([f"- {error}" for error in docx.errors]))

for file in {"favicon.ico", "index.md", "cover.png"}:
    os.system(f"cp {ORIGIN_FOLDER}/{file} {DESTINATION_FOLDER}/{file}")

with open(f"{DESTINATION_FOLDER}/sidebar.json", "w") as navigation_file:
    submenu = []
    for section in tree:
        section["items"] = [{"text": docx.title, "link": docx.slug} for docx in section["items"]]
        submenu.append(section)
    navigation_file.write(orjson.dumps(submenu).decode())

# copy public folder to .md folder
os.system(f"cp -r {PARENT}/public {DESTINATION_FOLDER}/public")
