from .markdown import MarkdownTransformer


class EpubTransformer(MarkdownTransformer):
    """A transformer that converts a Document object into an EPUB."""

    def get(self):
        """Return the EPUB representation of a Document object."""
        md = super().get()

        return md
