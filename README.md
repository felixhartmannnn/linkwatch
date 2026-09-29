# linkwatch

Local Markdown and HTML link health checker.

## About

`linkwatch` scans local files for `http(s)://` links, fetches each target, and reports status, content size, and failures. It works across Markdown and HTML, with threaded fetching for speed.

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
linkwatch /path/to/docs --format text
linkwatch README.md --format json --output report.json
linkwatch ./wiki --fail-on-error --timeout 5 --concurrency 4
```

## Project structure

```
linkwatch/
  linkwatch/
    __init__.py
    cli.py
    checker.py
    models.py
    parser.py
    reporter.py
  tests/
    test_cli.py
    test_checker.py
    test_models.py
    test_parser.py
    test_reporter.py
  pyproject.toml
  README.md
  .gitignore
```

## Repository

https://github.com/felixhartmannnn/linkwatch

## License

MIT
