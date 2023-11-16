import re
import unicodedata


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Convert a string to a slug.

    From: https://github.com/django/django/blob/main/django/utils/text.py

    Args:
        value: The string to slugify.
        allow_unicode: Whether to allow unicode characters. Defaults to False.

    Returns:
        The slugified string.
    """
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")

    value = re.sub(r"[^\w\s-]", "", value.lower())

    return re.sub(r"[-\s]+", "-", value).strip("-_")
