from ..types import Document


class Transformer:
    """
    A transformer takes a document and transforms it into another format.
    """

    def __init__(self, document: Document):
        self.document = document

    def get(self):
        """
        Get the transformed document on the desired format.
        """
        raise NotImplementedError
