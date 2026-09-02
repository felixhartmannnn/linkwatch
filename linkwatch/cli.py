from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Set

from linkwatch.checker import LinkChecker
from linkwatch.reporter import TextReporter, JsonReporter


def main(argv: Optional[List[str]] = None) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 0
    target = Path(args.path)
    if not target.exists():
        print(f"error: path not found: {target}", file=sys.stderr)
        return 1
    extensions = {ext.lower() for ext in args.extensions.split(",")}
    for extra in ["", ".md", ".markdown", ".html", ".htm"]:
        extensions.add(extra)
    checker = LinkChecker(timeout=args.timeout, concurrency=args.concurrency)
    parsed = checker.parse(target, extensions)
    link_results = checker.check(parsed)
    reporter = JsonReporter() if args.format == "json" else TextReporter()
    output = reporter.render(link_results)
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)
    failures = sum(1 for r in link_results if not r.ok)
    return 1 if args.fail_on_error and failures else 0


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Link health checker")
    parser.add_argument("path", help="File or directory to inspect")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--output", "-o", help="Write report to a file")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds")
    parser.add_argument("--concurrency", type=int, default=8, help="Max concurrent requests")
    parser.add_argument("--fail-on-error", action="store_true", help="Exit non-zero on any failure")
    parser.add_argument("--extensions", default=".md,.markdown,.html,.htm", help="Extensions to inspect")
    return parser.parse_args(argv)
