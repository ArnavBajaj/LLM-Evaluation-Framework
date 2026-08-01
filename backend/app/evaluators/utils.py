from __future__ import annotations

import re
from collections.abc import Iterable


TOKEN_PATTERN = re.compile(r"[a-z0-9']+")
STOP_WORDS = {"the", "and", "for", "with", "that", "this", "from", "are", "was", "were", "have", "has", "had"}


def tokenize(text: str) -> set[str]:
    return {token for token in TOKEN_PATTERN.findall(text.lower()) if len(token) > 2 and token not in STOP_WORDS}


def flatten_values(value: object) -> Iterable[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        pieces: list[str] = []
        for item in value.values():
            pieces.extend(flatten_values(item))
        return pieces
    if isinstance(value, Iterable):
        pieces = []
        for item in value:
            pieces.extend(flatten_values(item))
        return pieces
    return [str(value)]


def text_from_context(context: dict[str, object] | None, keys: tuple[str, ...]) -> str:
    if not context:
        return ""
    parts: list[str] = []
    for key in keys:
        parts.extend(flatten_values(context.get(key)))
    return " ".join(parts)