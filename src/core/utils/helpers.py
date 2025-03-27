import re
import unicodedata
from datetime import datetime
from typing import Any
from uuid import uuid4


def datetime_now() -> datetime:
    return datetime.now()


def randomized_name() -> str:
    """Random UUID4 name with date"""
    today = datetime_now()
    today_str = today.strftime("%Y%m%d")
    return f"{str(uuid4())[:12].replace('-', '')}-{today_str}"


def pluralize(noun: str) -> str:
    """Pluralize a word"""
    if re.search("[sxz]$", noun) or re.search("[^aeioudgkprt]h$", noun):
        return re.sub("$", "es", noun)
    if re.search("[^aeiou]y$", noun):
        return re.sub("y$", "ies", noun)

    return noun + "s"


def strip_accents(s: str) -> str:
    """
    Remove accents from string

    `Reference:` https://stackoverflow.com/a/518232/15441507
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def is_hashable(obj: Any) -> bool:
    """Return if an object is hashable"""
    try:
        hash(obj)
    except TypeError:
        return False
    else:
        return True


def to_snake(camel: str) -> str:
    """Convert a PascalCase or camelCase string to snake_case"""
    snake = re.sub(r"([a-zA-Z])([0-9])", lambda m: f"{m.group(1)}_{m.group(2)}", camel)
    snake = re.sub(r"([a-z0-9])([A-Z])", lambda m: f"{m.group(1)}_{m.group(2)}", snake)
    return snake.lower()


def get_authorization_scheme_param(
    authorization_header_value: str | None,
) -> tuple[str, str]:
    if not authorization_header_value:
        return "", ""

    scheme, _, param = authorization_header_value.partition(" ")

    return scheme, param
