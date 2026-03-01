# mcp-repo-hygiene-guardian — V1 Contract (Tier 1)

Status: V1 frozen (effective at tag v0.1.0)

This repository is a deterministic, network-free, read-only MCP guardian that performs basic repository hygiene checks.

V1 is intentionally narrow: one tool, stable schema, fail-closed semantics, deterministic output.

---

## 1. Tool Surface (V1)

V1 exposes exactly one tool:

- `check_repo_hygiene(repo_path: string) -> object`

No other tools are part of V1.

---

## 2. V1 Scope (Hard Boundary)

### 2.1 What V1 does

`check_repo_hygiene(repo_path)`:

- Validates inputs deterministically (fail-closed).
- Performs deterministic, read-only checks:
  - Required files exist in repo root: `LICENSE`, `README.md`, `pyproject.toml`
  - Build artifacts are not tracked by git:
    - no tracked paths under `build/` or `dist/`
    - no tracked `*.egg-info/` paths
- Produces an output object with:
  - `tool`, `repo_path`, `ok`, `fail_closed`, `details`, `output`.

### 2.2 What V1 explicitly does NOT do (Non-Goals)

V1 does not:

- make network calls
- call external MCP servers
- execute repository code
- write to disk or mutate repo state
- include timestamps, randomness, or environment-dependent metadata
- normalize, rewrite, or reserialize embedded outputs
- score, rank, infer, or recommend

If a capability is not explicitly listed in “What V1 does,” it is out of scope.

---

## 3. Determinism and Fail-Closed Semantics

### 3.1 Determinism requirements (Frozen)

For identical inputs, output must be identical:

- stable keys and types
- stable ordering under deterministic JSON serialization (sorted keys)
- stable `details` strings
- no timestamps, randomness, or environment-dependent text

### 3.2 Fail-closed requirements (Frozen)

- If `repo_path` is invalid or empty: `ok=false`, `fail_closed=true`.
- Any internal error must fail-closed with a stable error code in `details`.

V1 never downgrades failures.

### 3.3 Deterministic failure codes (V1)

| Code | Trigger |
|---|---|
| `fail-closed: invalid_repo_path` | `repo_path` is invalid or empty |
| `fail-closed: git_ls_files_failed` | `git ls-files` failed |
| `fail-closed: required_files_missing` | One or more required files missing |
| `fail-closed: build_artifacts_tracked` | One or more build artifacts are tracked by git |

---

## 4. Output Schema (V1)

Top-level JSON object contains exactly:

- `tool` (string) — always `"check_repo_hygiene"`
- `repo_path` (string)
- `ok` (boolean)
- `fail_closed` (boolean)
- `details` (string)
- `output` (object | null)

Inside `output` (when not null), keys are:

- `missing_required_files` (list[string])
- `tracked_build_artifacts` (list[string])
- `notes` (list[string])

No additional keys are part of V1.

---

## 5. Backward Compatibility Rule

After tag v0.1.0:

- Tool name and signature are frozen.
- Top-level schema is frozen.
- Output subkeys are frozen.
- Determinism and fail-closed guarantees are frozen.

Any breaking change requires V2 and an explicit contract document.

---

## 6. Canonical Examples

Canonical example outputs are defined in `docs/EXAMPLE_OUTPUTS.md` and are part of the V1 contract.
