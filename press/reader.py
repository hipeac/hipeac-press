from pathlib import Path

from press.docx import Docx


class Reader:
    def __init__(self, path: Path):
        self.path = path
        self.main_folders = [
            folder for folder in sorted(self.path.iterdir()) if folder.is_dir() and folder.name[0] != "."
        ]

    def read_folder(self, folder: Path):
        """
        Read a folder and its contents.
        """
        items = []

        for content in sorted(folder.iterdir()):
            if content.is_dir():
                items.extend(self.read_folder(content))
            elif content.is_file() and content.suffix == ".docx" and content.name[0] != "~":
                items.append(Docx(content))

        return items

    @property
    def tree(self):
        """
        Return the simplified tree structure.
        Folder names are preceded by 01, 02, 03, etc. to keep the order; we can remove that part.
        """
        tree = []

        for main_folder in self.main_folders:
            tree.append(
                {
                    "text": main_folder.name[3:],
                    "collapsed": not main_folder.name.startswith("00"),
                    "items": self.read_folder(main_folder),
                }
            )

        return tree
