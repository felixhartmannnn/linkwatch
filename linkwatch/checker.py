from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Set, Tuple

from linkwatch.models import LinkResult, ParseResult
from linkwatch.parser import LinkParser


class LinkChecker:
    def __init__(
        self, timeout: int = 10, concurrency: int = 8, user_agent: str = "linkwatch/0.1"
    ) -> None:
        self.timeout = timeout
        self.concurrency = concurrency
        self.user_agent = user_agent
        self._checked: Set[str] = set()

    def discover(self, root: Path, extensions: Set[str]) -> List[Path]:
        if root.is_file():
            return [root]
        out: List[Path] = []
        for path in sorted(root.rglob("*")):
            if path.is_file() and (
                path.suffix.lower() in extensions or path.name.lower() == "readme"
            ):
                out.append(path)
        return out

    def parse(self, root: Path, extensions: Set[str]) -> List[ParseResult]:
        parser = LinkParser()
        return [parser.parse_file(path) for path in self.discover(root, extensions)]

    def check(self, results: List[ParseResult]) -> List[LinkResult]:
        tasks: List[Tuple[str, str]] = []
        source_by_url = {}
        for result in results:
            for url in result.links:
                if url in self._checked:
                    continue
                self._checked.add(url)
                tasks.append((url, result.source))
                source_by_url[url] = result.source
        checked = _fetch_many(tasks, self.timeout, self.concurrency, self.user_agent)
        return [
            LinkResult(
                url=url,
                source=source_by_url[url],
                ok=ok,
                status=status,
                length=length,
                error=error,
            )
            for url, ok, status, length, error in checked
        ]


def _fetch_many(tasks, timeout, concurrency, user_agent) -> List[tuple]:
    try:
        import requests  # noqa: F401
    except ImportError:
        return [_fetch_stdlib(url, timeout, user_agent) for (url, _) in tasks]
    checked: List[tuple] = []
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {
            pool.submit(_fetch_requests, url, timeout, user_agent): url
            for (url, _) in tasks
        }
        for future in as_completed(futures):
            checked.append(future.result())
    return checked


def _fetch_requests(url: str, timeout: int, user_agent: str) -> tuple:
    try:
        import requests
    except ImportError:
        return _fetch_stdlib(url, timeout, user_agent)
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": user_agent},
            allow_redirects=True,
        )
        return (url, response.ok, response.status_code, len(response.content), None)
    except Exception as exc:
        return (url, False, None, None, str(exc))


def _fetch_stdlib(url: str, timeout: int, user_agent: str) -> tuple:
    import urllib.request

    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        response = urllib.request.urlopen(request, timeout=timeout)
        length = len(response.read())
        status = getattr(response, "status", None)
        if status is None:
            status = getattr(response, "code", 200)
        return (url, True, status, length, None)
    except Exception as exc:
        return (url, False, None, None, str(exc))
