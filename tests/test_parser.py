from pathlib import Path
from linkwatch.parser import LinkParser


def test_parse_markdown_links(tmp_path):
    target = tmp_path / "doc.md"
    target.write_text("[x](https://example.com) and https://other.test)")
    result = LinkParser().parse_file(target)
    assert "https://example.com" in result.links
    assert "https://other.test" in result.links


def test_parse_skips_code_fences(tmp_path):
    target = tmp_path / "code.md"
    target.write_text("```\nhttps://inside.code.block\n```\nReal: https://real.com")
    result = LinkParser().parse_file(target)
    assert result.links == ["https://real.com"]


def test_parse_html(tmp_path):
    target = tmp_path / "page.html"
    target.write_text('<a href="https://html.example.com">x</a>')
    result = LinkParser().parse_file(target)
    assert result.links == ["https://html.example.com"]


def test_parse_error_returns_empty():
    parser = LinkParser()
    result = parser.parse_file(Path("/dev/null/doesnotexist.md"))
    assert result.links == []
    assert result.error is not None
