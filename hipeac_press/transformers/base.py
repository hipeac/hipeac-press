"""Base transformer class for the hipeac_press package."""

from abc import ABC, abstractmethod

from ..type_definitions import Document


class Transformer(ABC):
    """Abstract base class for transformers.

    :param document: The document to transform.
    """

    def __init__(self, document: Document):
        """Initialize the transformer with a document.

        :param document: The document to transform.
        """
        self.document = document

    @abstractmethod
    def get(self) -> bytes:
        """Return the transformed document as a byte string.

        :returns: The transformed document as a byte string.
        """
        raise NotImplementedError
