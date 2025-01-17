from pathlib import Path

from hipeac_press.docx import DocxConverter


class Reader:
    """A class to represent a reader of a folder structure."""

    def __init__(self, main_folder: Path, img_folder: Path):
        self.main_folder = main_folder
        self.img_folder = img_folder
        self.main_folders = [
            folder for folder in sorted(self.main_folder.iterdir()) if folder.is_dir() and folder.name[0] != "."
        ]

    def _read_folder(self, folder: Path, section_name: str = None):
        items = []

        for content in sorted(folder.iterdir()):
            if content.is_dir():
                if content.name == "tracked":
                    continue
                items.extend(self._read_folder(content, section_name))
            elif content.is_file() and content.suffix == ".docx" and content.name[0] != "~":
                items.append(
                    DocxConverter(
                        content,
                        img_folder=self.img_folder,
                        metadata_path=folder / "metadata.json",
                        section_name=section_name,
                    )
                )

        return items

    def _set_navigation(self, tree):
        all_items = [item for section in tree for item in section["items"]]

        for i, item in enumerate(all_items):
            if i > 0:
                item.set_prev(
                    {
                        "text": all_items[i - 1].title,
                        "link": f"/{all_items[i - 1].slug}",
                    }
                )
            if i < len(all_items) - 1:
                item.set_next(
                    {
                        "text": all_items[i + 1].title,
                        "link": f"/{all_items[i + 1].slug}",
                    }
                )

    def build_tree(self):
        """Build the tree structure and set navigation."""
        tree = []

        for main_folder in self.main_folders:
            section_name = main_folder.name[3:].strip()
            items = self._read_folder(main_folder, section_name)
            tree.append(
                {
                    "text": section_name,
                    "collapsed": main_folder.name.split(" ")[0].endswith("C"),
                    "items": items,
                }
            )

        self._set_navigation(tree)

        return tree

    @property
    def tree(self):
        """Return the simplified tree structure with navigation."""
        return self.build_tree()
