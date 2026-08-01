from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LinkResult:
    url: str
    source: str
    ok: bool
    status: Optional[int]
    length: Optional[int]
    error: Optional[str] = None


@dataclass
class ParseResult:
    links: list[str]
    source: str
    error: Optional[str] = None
