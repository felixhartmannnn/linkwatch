from linkwatch.models import LinkResult, ParseResult


def test_link_result_creation():
    result = LinkResult(url="https://example.com", source="x.md", ok=True, status=200, length=123)
    assert result.url == "https://example.com"
    assert result.ok is True


def test_parse_result_creation():
    result = ParseResult(links=["https://example.com"], source="x.md")
    assert result.links == ["https://example.com"]
