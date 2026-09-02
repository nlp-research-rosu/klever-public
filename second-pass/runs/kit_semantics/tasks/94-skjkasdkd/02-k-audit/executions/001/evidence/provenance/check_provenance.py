#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("campaign_object_matches_lock", audit["audit_campaign"] == lock)
print("campaign_lock_sha256", sha256(Path("/audit-campaign-lock.json")))
print("campaign_lock_expected", audit["hashes"]["audit_campaign_lock_sha256"])

checks = {
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "run_manifest_sha256": Path("/run.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "task_manifest_sha256": Path("/task.json"),
}
for key, path in checks.items():
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(key, "OK" if actual == expected else "MISMATCH", actual, str(path))

result = json.loads(Path("/generation-result.json").read_text())
for relpath, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relpath
    actual = sha256(path)
    print("generation-result", relpath, "OK" if actual == expected else "MISMATCH", actual)

for label, root in [
    ("candidate-semantics", Path("/candidate/reference-semantics")),
    ("trusted-semantics", Path("/reference/reference-semantics")),
]:
    print(label, "entries")
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        kind = "symlink" if path.is_symlink() else ("dir" if path.is_dir() else "file")
        detail = os.readlink(path) if path.is_symlink() else (sha256(path) if path.is_file() else "")
        print(kind, rel, detail)
