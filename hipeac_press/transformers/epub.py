from .base import Transformer


class EpubTransformer(Transformer):
    """A transformer that converts a Document object into an EPUB."""

    def get(self):
        """Return the EPUB representation of a Document object."""
        raise NotImplementedError
