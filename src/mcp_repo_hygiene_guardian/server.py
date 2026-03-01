from __future__ import annotations

import json
import os
import subprocess
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP


mcp = FastMCP("mcp-repo-hygiene-guardian")


def canonical_json(obj: Any) -> str:
    """
    Deterministic JSON serialization helper for callers and tests.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _repo_path_is_valid(repo_path: str) -> bool:
    if not isinstance(repo_path, str):
        return False
    rp = repo_path.strip()
    if not rp:
        return False
    return os.path.isdir(rp)


def _result(
    *,
    repo_path: str,
    ok: bool,
    fail_closed: bool,
    details: str,
    output: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "tool": "check_repo_hygiene",
        "repo_path": repo_path,
        "ok": ok,
        "fail_closed": fail_closed,
        "details": details,
        "output": output,
    }


def _missing_required_files(repo_path: str) -> List[str]:
    required = ["LICENSE", "README.md", "pyproject.toml"]
    missing: List[str] = []
    for name in required:
        if not os.path.exists(os.path.join(repo_path, name)):
            missing.append(name)
    return missing


def _tracked_build_artifacts(tracked_files: List[str]) -> List[str]:
    hits: List[str] = []
    for p in tracked_files:
        if p.startswith("build/") or p.startswith("dist/") or (".egg-info" in p):
            hits.append(p)
    return sorted(set(hits))


def _git_ls_files(repo_path: str) -> List[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return lines


@mcp.tool()
def check_repo_hygiene(repo_path: str) -> Dict[str, Any]:
    """
    Deterministic, network-free, read-only guardian tool.

    Contract notes:
    - No timestamps, randomness, environment-derived metadata.
    - No disk writes or repo mutation.
    - Fail-closed on all invalid inputs and internal errors.
    """
    if not _repo_path_is_valid(repo_path):
        return _result(
            repo_path=repo_path,
            ok=False,
            fail_closed=True,
            details="fail-closed: invalid_repo_path",
            output=None,
        )

    missing = _missing_required_files(repo_path)

    try:
        tracked = _git_ls_files(repo_path)
    except Exception:
        return _result(
            repo_path=repo_path,
            ok=False,
            fail_closed=True,
            details="fail-closed: git_ls_files_failed",
            output=None,
        )

    tracked_artifacts = _tracked_build_artifacts(tracked)

    output = {
        "missing_required_files": missing,
        "tracked_build_artifacts": tracked_artifacts,
        "notes": [],
    }

    if missing:
        return _result(
            repo_path=repo_path,
            ok=False,
            fail_closed=True,
            details="fail-closed: required_files_missing",
            output=output,
        )

    if tracked_artifacts:
        return _result(
            repo_path=repo_path,
            ok=False,
            fail_closed=True,
            details="fail-closed: build_artifacts_tracked",
            output=output,
        )

    return _result(
        repo_path=repo_path,
        ok=True,
        fail_closed=False,
        details="ok",
        output=output,
    )


def main() -> None:
    mcp.run()
