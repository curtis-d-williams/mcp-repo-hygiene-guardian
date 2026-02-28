from __future__ import annotations

import json
from typing import Any, Dict

from fastmcp import FastMCP


mcp = FastMCP("mcp-guardian-template")


def canonical_json(obj: Any) -> str:
    """
    Deterministic JSON serialization helper for callers and tests.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _repo_path_is_valid(repo_path: str) -> bool:
    # V1 template: deterministic, read-only, network-free. Minimal validation only.
    return isinstance(repo_path, str) and len(repo_path.strip()) > 0


def _fail_closed(details: str, repo_path: str) -> Dict[str, Any]:
    # Top-level schema is intentionally minimal and stable.
    return {
        "tool": "evaluate_repo",
        "repo_path": repo_path,
        "ok": False,
        "fail_closed": True,
        "details": details,
        "output": None,
    }


@mcp.tool()
def evaluate_repo(repo_path: str) -> Dict[str, Any]:
    """
    Deterministic, network-free, read-only guardian template tool.

    Contract notes:
    - No timestamps, randomness, environment-derived metadata.
    - No disk writes or repo mutation.
    - Fail-closed on all invalid inputs and internal errors.
    """
    if not _repo_path_is_valid(repo_path):
        return _fail_closed("fail-closed: invalid_repo_path", repo_path)

    # Template behavior: does not inspect repo by default.
    # Real guardians will replace this section with deterministic checks only.
    return {
        "tool": "evaluate_repo",
        "repo_path": repo_path,
        "ok": True,
        "fail_closed": False,
        "details": "ok",
        "output": {
            "note": "template_guardian_noop",
        },
    }


def main() -> None:
    mcp.run()
