#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

echo 'COMMAND: bash /audit-output/evidence/01_provenance.sh'

for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T04-00-45-019f890e-53e2-7f21-9e88-38401bd1ffa8.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
do
  test -f "$path"
  test ! -L "$path"
done

test -d /candidate
test ! -L /candidate
test -d /generation-evidence/codex-trace
test ! -L /generation-evidence/codex-trace
test ! -e /reference/reference-semantics
test ! -L /reference/reference-semantics

if find /candidate /reference /generation-evidence -xdev -type l -print -quit | grep -q .; then
  echo 'ERROR: symlink found in a mounted input tree'
  exit 1
fi

cmp /candidate/prompt.py /reference/prompt.py
cmp /candidate/py2mpy.py /reference/py2mpy.py

sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T04-00-45-019f890e-53e2-7f21-9e88-38401bd1ffa8.jsonl

python3 - <<'PY'
import hashlib
import json
import os
import stat
from pathlib import Path


def file_hash(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root_name: str) -> str:
    root = Path(root_name)
    digest = hashlib.sha256()
    pending = [root]
    entries = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
run = json.loads(Path("/run.json").read_text())
task = json.loads(Path("/task.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["problem_id"] == "11-string-xor"
assert audit["condition"] == "bare"
assert audit["audit_campaign"] == lock
normalized_manifest = dict(audit["manifest"])
assert normalized_manifest.pop("config") == audit["config"]
assert normalized_manifest == task
assert run["run_id"] == audit["run_id"]
assert run["config"] == audit["config"]
assert result["stage"] == "01-k-proof"
assert result["invocation"] == invocation["name"]

expected_files = {
    "/audit-campaign-lock.json": audit["hashes"]["audit_campaign_lock_sha256"],
    "/run.json": audit["hashes"]["run_manifest_sha256"],
    "/task.json": audit["hashes"]["task_manifest_sha256"],
    "/generation-result.json": audit["hashes"]["stage1_result_sha256"],
    "/reference/canonical.py": audit["hashes"]["canonical_sha256"],
    "/reference/prompt.py": audit["hashes"]["trusted_prompt_sha256"],
    "/reference/py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
    "/candidate/prompt.py": audit["hashes"]["candidate_prompt_sha256"],
    "/candidate/py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
    "/generation-evidence/invocation.json": audit["hashes"]["stage1_invocation_sha256"],
    "/generation-evidence/metrics.json": audit["hashes"]["generation_metrics_sha256"],
    "/generation-evidence/usage.json": audit["hashes"]["generation_usage_sha256"],
    "/generation-evidence/codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
    "/generation-evidence/codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
    "/generation-evidence/prompt.txt": audit["hashes"]["generation_prompt_sha256"],
}
for path, expected in expected_files.items():
    actual = file_hash(path)
    assert actual == expected, (path, expected, actual)

trace_file = (
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-00-45-019f890e-53e2-7f21-9e88-38401bd1ffa8.jsonl"
)
trace_file_hash = file_hash(trace_file)
assert (
    result["outputs"]["evidence"][
        "codex-trace/2026/07/22/"
        "rollout-2026-07-22T04-00-45-019f890e-53e2-7f21-9e88-38401bd1ffa8.jsonl"
    ]
    == trace_file_hash
)

candidate_tree = pipeline_tree_hash("/candidate")
trace_tree = pipeline_tree_hash("/generation-evidence/codex-trace")
assert candidate_tree == result["outputs"]["workspace_sha256"]
assert candidate_tree == invocation["outputs"]["workspace_sha256"]
assert trace_tree == usage["source_trace_sha256"]

print("campaign_lock_equal=true")
print(f"candidate_pipeline_tree_sha256={candidate_tree}")
print(f"trace_pipeline_tree_sha256={trace_tree}")
print(f"trace_file_sha256={trace_file_hash}")
print("required_layout_records=present_regular_non_symlink")
print("trusted_prompt_and_translator=byte_identical")
print("generated_semantics_reference_baseline=correctly_absent")
PY
