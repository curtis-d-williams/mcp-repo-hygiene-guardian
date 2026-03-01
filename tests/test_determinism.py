# SPDX-License-Identifier: MIT
from mcp_repo_hygiene_guardian.server import canonical_json, check_repo_hygiene


def test_check_repo_hygiene_is_deterministic() -> None:
    out1 = check_repo_hygiene(".")
    out2 = check_repo_hygiene(".")
    assert canonical_json(out1) == canonical_json(out2)


def test_output_schema_is_stable() -> None:
    out = check_repo_hygiene(".")
    assert set(out.keys()) == {"tool", "repo_path", "ok", "fail_closed", "details", "output"}

    if out["output"] is not None:
        assert set(out["output"].keys()) == {
            "missing_required_files",
            "tracked_build_artifacts",
            "notes",
        }
