import json
from linkwatch.cli import main


def test_cli_help_exit_zero():
    assert main(["--help"]) == 0


def test_cli_missing_path():
    assert main(["/nonexistent"]) == 1


def test_cli_text_output(tmp_path, monkeypatch, capsys):
    target = tmp_path / "README.md"
    target.write_text("[x](https://example.com)")
    monkeypatch.setattr(
        "linkwatch.checker._fetch_many",
        lambda *a, **kw: [("https://example.com", True, 200, 5, None)],
    )
    assert main([str(target)]) == 0
    assert "200" in capsys.readouterr().out


def test_cli_json_output(tmp_path):
    out = tmp_path / "out.json"
    target = tmp_path / "README.md"
    target.write_text("[x](https://example.com)")
    assert main([str(target), "--format", "json", "--output", str(out)]) == 0
    assert out.exists()
    data = json.loads(out.read_text())
    assert len(data) == 1


def test_cli_fail_on_error(tmp_path, monkeypatch):
    target = tmp_path / "README.md"
    target.write_text("[x](https://example.com)")
    monkeypatch.setattr(
        "linkwatch.checker._fetch_many",
        lambda *a, **kw: [("https://example.com", False, 500, 0, "err")],
    )
    assert main([str(target), "--fail-on-error"]) == 1
