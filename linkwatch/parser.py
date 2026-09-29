from __future__ import annotations

import re
from pathlib import Path
from typing import List

from linkwatch.models import ParseResult


ILLEGAL_CHARS = re.compile(r"[^\w\-._~:/?#\[\]@!$&'()*+,;=%]")


class LinkParser:
    def parse_file(self, path: Path) -> ParseResult:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            return ParseResult(links=[], source=str(path), error=str(exc))
        links = (
            self._parse_markdown(text)
            if path.suffix.lower() in {".md", ".markdown"}
            else self._parse_html(text)
        )
        return ParseResult(links=links, source=str(path))

    def _parse_markdown(self, text: str) -> List[str]:
        out: List[str] = []
        in_code = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code = not in_code
                continue
            if in_code or stripped.startswith("#"):
                continue
            for raw_url in re.findall(r"https?://[^\s)>\]\']+", line):
                clean = self._clean_url(raw_url)
                if clean:
                    out.append(clean)
        return out

    def _parse_html(self, text: str) -> List[str]:
        out = []
        for raw_url in re.findall(r"https?://[^\s)>\]\']+", text):
            clean = self._clean_url(raw_url)
            if clean:
                out.append(clean)
        return out

    @staticmethod
    def _clean_url(url: str) -> str:
        return ILLEGAL_CHARS.sub("", url).strip()
