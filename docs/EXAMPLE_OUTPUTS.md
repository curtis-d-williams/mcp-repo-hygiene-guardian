# Canonical Example Outputs (V1)

The following output is part of the V1 contract and must remain byte-identical
when serialized deterministically (sorted keys, compact separators).

## Example: check_repo_hygiene(".")

Canonical JSON:

{"details":"ok","fail_closed":false,"ok":true,"output":{"missing_required_files":[],"notes":[],"tracked_build_artifacts":[]},"repo_path":".","tool":"check_repo_hygiene"}
