import re
import unicodedata


def md_footnote(value: str, add_colon: bool = False) -> str:
    """
    Replace all square brackets that contain a number with square brackets with a caret in front.
    If add_colon is True, also add a colon after the number, for the first occurrence only.
    So: [12] becomes [^12] or [^12]:
    """

    value = re.sub(r"\[(\d+)\]", r"[^\1]", value)
    if add_colon:
        value = re.sub(r"\[([^\]]+)\]", r"[\1]:", value, 1)
    return value


def slugify(value, allow_unicode=False):
    """
    from: https://github.com/django/django/blob/main/django/utils/text.py

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)

    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")

    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
