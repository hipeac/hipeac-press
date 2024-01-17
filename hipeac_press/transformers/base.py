from ..docx import Docx


class Transformer:
    """A transformer takes a Document and transforms it into another format."""

    def __init__(self, docx: Docx):
        self.docx = docx
        self.document = docx.document

    def get(self):
        """Get the transformed document on the desired format."""
        raise NotImplementedError
