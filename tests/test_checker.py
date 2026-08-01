from pathlib import Path
from linkwatch.checker import LinkChecker, _fetch_stdlib


def test_discover_single_file(tmp_path):
    target = tmp_path / "README.md"
    target.write_text("[x](https://example.com)")
    checker = LinkChecker(timeout=1, concurrency=1)
    files = checker.discover(target, {".md"})
    assert files == [target]


def test_discover_directory(tmp_path):
    (tmp_path / "a.md").write_text("[a](https://a.test)")
    (tmp_path / "b.html").write_text('<a href="https://b.test">b</a>')
    checker = LinkChecker(timeout=1, concurrency=1)
    files = checker.discover(tmp_path, {".md", ".html"})
    assert [p.name for p in files] == ["a.md", "b.html"]


def test_parse_collects_links(tmp_path):
    root = tmp_path / "docs"
    root.mkdir()
    (root / "1.md").write_text("[x](https://example.com)")
    (root / "2.html").write_text('<a href="https://html.test">x</a>')
    checker = LinkChecker(timeout=1, concurrency=1)
    results = checker.parse(root, {".md", ".html"})
    urls = sorted({url for r in results for url in r.links})
    assert urls == ["https://example.com", "https://html.test"]


def test_check_stdlib_fetches_local_file():
    Path("/tmp/linkwatch-local-ok.txt").write_text("ok")
    result = _fetch_stdlib("file:///tmp/linkwatch-local-ok.txt", timeout=2, user_agent="test")
    assert result[1] is True
    assert result[2] in {200, None}


def test_check_stdlib_fails_bad_scheme():
    result = _fetch_stdlib("ftp://example.com", timeout=1, user_agent="test")
    assert result[1] is False
    assert result[4] is not None


def test_check_deduplicates_requests(tmp_path):
    target = tmp_path / "doc.md"
    target.write_text("[a](https://example.com)\n[b](https://example.com)")
    checker = LinkChecker(timeout=1, concurrency=1)
    results = checker.parse(target, {".md"})
    checker.check(results)
    assert checker._checked == {"https://example.com"}
