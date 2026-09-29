import json
from linkwatch.models import LinkResult
from linkwatch.reporter import TextReporter, JsonReporter


def _results():
    return [
        LinkResult(
            url="https://ok.test", source="a.md", ok=True, status=200, length=10
        ),
        LinkResult(
            url="https://bad.test",
            source="b.md",
            ok=False,
            status=500,
            length=0,
            error="server error",
        ),
    ]


def test_text_reporter_contains_status():
    report = TextReporter().render(_results())
    assert "200" in report
    assert "500" in report


def test_json_reporter_shape():
    report = JsonReporter().render(_results())
    data = json.loads(report)
    assert len(data) == 2
    assert data[0]["ok"] is True
    assert data[1]["status"] == 500
