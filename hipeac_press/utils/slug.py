import re
import unicodedata


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Convert a string to a slug.

    :param value: The string to slugify.
    :param allow_unicode: Whether to allow unicode characters. Defaults to False.
    :returns: The slugified string.
    """
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")

    value = re.sub(r"[^\w\s-]", "", value.lower())

    return re.sub(r"[-\s]+", "-", value).strip("-_")
