from pathlib import Path

from hipeac_press.docx import Docx


class Reader:
    """A class to represent a reader of a folder structure."""

    def __init__(self, path: Path):
        self.path = path
        self.main_folders = [
            folder for folder in sorted(self.path.iterdir()) if folder.is_dir() and folder.name[0] != "."
        ]

    def read_folder(self, folder: Path, section_name: str = None):
        """Read a folder and its contents."""
        items = []

        for content in sorted(folder.iterdir()):
            if content.is_dir():
                items.extend(self.read_folder(content, section_name))
            elif content.is_file() and content.suffix == ".docx" and content.name[0] != "~":
                items.append(Docx(content, section_name=section_name))

        return items

    @property
    def tree(self):
        """Return the simplified tree structure.

        Folder names are preceded by 01, 02, 03, etc. to keep the order; we can remove that part.
        """
        tree = []

        for main_folder in self.main_folders:
            # skip folders starting with tmp
            if main_folder.name.startswith("tmp"):
                continue

            section_name = main_folder.name[3:].strip()
            tree.append(
                {
                    "text": section_name,
                    "collapsed": not main_folder.name.startswith("00"),
                    "items": self.read_folder(main_folder, section_name),
                }
            )

        return tree
