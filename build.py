import copy
import json
import os
from pathlib import Path
from shutil import rmtree

from hipeac_press.reader import Reader
from hipeac_press.recommendations import generate_recommendations
from hipeac_press.type_definitions import NavItem
from hipeac_press.utils.epub import generate_epub
from hipeac_press.utils.pdf import concatenate_pdfs, set_headers_footers


PARENT = Path(__file__).parent
VISION_YEAR = os.environ.get("VISION_YEAR", "2025")
VISION_PATH = Path(os.environ.get("VISION_SOURCE_PATH", "/Users/eillarra/Nextcloud/hipeac/Vision/2025/Website"))

origin_path = PARENT / ".source"
destination_path = PARENT / ".build"
images_path = destination_path / "images"

rmtree(destination_path, ignore_errors=True)
rmtree(origin_path, ignore_errors=True)

destination_path.mkdir(exist_ok=True)
origin_path.mkdir(exist_ok=True)
images_path.mkdir(parents=True, exist_ok=True)

os.system(f'cp -r "{VISION_PATH}"/* "{origin_path}"')

reader = Reader(origin_path, img_folder=images_path)
tree = reader.tree


# generate recommendations

tree = generate_recommendations(tree)


# generate files: md, pdf

for section_index, section in enumerate(tree):
    for i, item in enumerate(section["items"]):
        prev_item = section["items"][i - 1] if i > 0 else None
        next_item = section["items"][i + 1] if i < len(section["items"]) - 1 else None

        if prev_item is None and section_index > 0:
            prev_item = tree[section_index - 1]["items"][-1]
        if next_item is None and section_index < len(tree) - 1:
            next_item = tree[section_index + 1]["items"][0]

        item.set_prev(NavItem(text=prev_item.title, link=f"/{prev_item.slug}") if prev_item else None)
        item.set_next(NavItem(text=next_item.title, link=f"/{next_item.slug}") if next_item else None)

        for file_format in ["md", "pdf"]:
            file_path = destination_path
            if file_format != "md":
                file_path = PARENT / "public" / file_format
                if not file_path.exists():
                    file_path.mkdir(parents=True, exist_ok=True)
            with open(file_path / f"{item.slug}.{file_format}", "wb") as f:
                f.write(item.export(format=file_format, build_path=destination_path, section_name=section["text"]))

        # try removing existing errors.txt file (itmight not be there)
        try:
            os.remove(VISION_PATH / item._docx_path.parent.relative_to(origin_path) / "errors.txt")
        except FileNotFoundError:
            pass

        if item.errors:  # Write errors to a txt file if there are any
            vision_parent_path = VISION_PATH / item._docx_path.parent.relative_to(origin_path)
            with open(vision_parent_path / "errors.txt", "w") as error_file:
                error_file.write("\n".join(item.errors))


# copy general files to the destination folder

for file in {"index.md", "cover.png", "cover.jpg"}:
    os.system(f"cp {origin_path / file} {destination_path / file}")
    os.system(f"cp {origin_path / file} {PARENT / 'public'}")


# generate epub

epub_path = PARENT / "public" / "epub"
epub_path.mkdir(parents=True, exist_ok=True)

epub = generate_epub(
    tree,
    destination_path,
    epub_path / f"hipeac-vision-{VISION_YEAR}.epub",
    title=f"HiPEAC Vision {VISION_YEAR}",
)


# create sibebar.json file

with open(destination_path / "sidebar.json", "w") as navigation_file:
    submenu = []
    for section in copy.deepcopy(tree):
        section["items"] = [{"text": docx.title, "link": docx.slug} for docx in section["items"]]
        submenu.append(section)
    navigation_file.write(json.dumps(submenu))


# concatenate PDFs without headers and footers

concatenate_pdfs(tree, PARENT / "public" / "pdf", VISION_YEAR, cover_pdf=VISION_PATH / "cover.pdf")


# set headers and footers for individual PDFs

logo_path = PARENT / "public" / "hipeac.svg"

for _, section in enumerate(tree):
    for item in section["items"]:
        set_headers_footers(item, PARENT / "public" / "pdf", VISION_YEAR, logo_path)


# copy public folder to .md folder

os.system(f"cp -r {PARENT / 'public'} {destination_path / 'public'}")
