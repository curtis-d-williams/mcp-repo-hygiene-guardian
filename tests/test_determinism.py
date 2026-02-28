from mcp_guardian_template.server import evaluate_repo, canonical_json


def test_evaluate_repo_is_deterministic() -> None:
    out1 = evaluate_repo(".")
    out2 = evaluate_repo(".")
    assert canonical_json(out1) == canonical_json(out2)


def test_output_schema_is_stable() -> None:
    out = evaluate_repo(".")
    assert set(out.keys()) == {"tool", "repo_path", "ok", "fail_closed", "details", "output"}
