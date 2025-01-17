import json
import os
from pathlib import Path
from shutil import rmtree

from hipeac_press.reader import Reader
from hipeac_press.type_definitions import NavItem


PARENT = Path(__file__).parent
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

        for file_format in ["md"]:  # , "pdf"
            with open(destination_path / f"{item.slug}.{file_format}", "wb") as f:
                f.write(item.export(format=file_format, section_name=section["text"]))

        if item.errors:  # Write errors to a txt file if there are any
            vision_parent_path = VISION_PATH / item._docx_path.parent.relative_to(origin_path)
            with open(vision_parent_path / "errors.txt", "w") as error_file:
                error_file.write("\n".join(item.errors))


for file in {"index.md", "cover.png"}:
    os.system(f"cp {origin_path / file} {destination_path / file}")
    os.system(f"cp {origin_path / file} {PARENT / 'public'}")

with open(destination_path / "sidebar.json", "w") as navigation_file:
    submenu = []
    for section in tree:
        section["items"] = [{"text": docx.title, "link": docx.slug} for docx in section["items"]]
        submenu.append(section)
    navigation_file.write(json.dumps(submenu))

# Copy public folder to .md folder
os.system(f"cp -r {PARENT / 'public'} {destination_path / 'public'}")
