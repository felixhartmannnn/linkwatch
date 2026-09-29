from __future__ import annotations

import json
from typing import List

from linkwatch.models import LinkResult


class TextReporter:
    def render(self, results: List[LinkResult]) -> str:
        lines = ["Link Report", f"Total: {len(results)}", ""]
        lines.extend(
            f"[{'OK' if r.ok else 'FAIL'}] {r.url} ({r.status}) <- {r.source}"
            for r in results
        )
        lines.append("")
        failed = [r for r in results if not r.ok]
        lines.append(f"Failed: {len(failed)}/{len(results)}")
        return "\n".join(lines)


class JsonReporter:
    def render(self, results: List[LinkResult]) -> str:
        payload = [
            {
                "url": r.url,
                "source": r.source,
                "ok": r.ok,
                "status": r.status,
                "length": r.length,
                "error": r.error,
            }
            for r in results
        ]
        return json.dumps(payload, indent=2)
