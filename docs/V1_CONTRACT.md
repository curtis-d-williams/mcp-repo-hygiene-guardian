# mcp-guardian-template — V1 Contract (Tier 1 Baseline)

Status: V1 frozen (effective at tag v0.1.0)

This repository is a deterministic, network-free, read-only MCP guardian template designed to produce Tier 1 eligible guardians.

V1 is intentionally narrow: one tool, stable schema, fail-closed semantics, deterministic output.

---

## 1. Tool Surface (V1)

V1 exposes exactly one tool:

- `evaluate_repo(repo_path: string) -> object`

No other tools are part of V1.

---

## 2. V1 Scope (Hard Boundary)

### 2.1 What V1 does

`evaluate_repo(repo_path)`:

- Validates inputs deterministically (fail-closed).
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

### 3.3 Deterministic failure codes (initial set)

| Code | Trigger |
|---|---|
| `fail-closed: invalid_repo_path` | `repo_path` is invalid or empty |

Additional failure codes may be added only in V2.

---

## 4. Output Schema (V1)

Top-level JSON object contains exactly:

- `tool` (string) — always `"evaluate_repo"`
- `repo_path` (string)
- `ok` (boolean)
- `fail_closed` (boolean)
- `details` (string)
- `output` (object | null)

No additional top-level keys are part of V1.

---

## 5. Backward Compatibility Rule

After tag v0.1.0:

- Tool name and signature are frozen.
- Top-level schema is frozen.
- Determinism and fail-closed guarantees are frozen.

Any breaking change requires V2 and an explicit contract document.

---

## 6. Canonical Examples

Canonical example outputs are defined in `docs/EXAMPLE_OUTPUTS.md` and are part of the V1 contract.
