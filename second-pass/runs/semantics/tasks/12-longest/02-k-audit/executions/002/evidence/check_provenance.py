#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T21-17-17-019f8cc3-4c6e-76b2-92ed-caa84f89bfad.jsonl"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")
    list(path.iterdir())


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("unsupported", f"mode={mode:o}")
    return result


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256(path)
    outcome = "OK" if actual == expected else "MISMATCH"
    print(f"{outcome} {label}: expected={expected} actual={actual}")
    if actual != expected:
        raise AssertionError(f"{label} hash mismatch")


def main() -> None:
    audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert lock == audit_input["audit_campaign"]
    print("OK campaign lock object equals audit-input audit_campaign")

    hashes = audit_input["hashes"]
    direct_hashes = {
        "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "stage1_result_sha256": Path("/generation-result.json"),
    }
    for label, path in direct_hashes.items():
        require_regular(path)
        check_hash(label, path, hashes[label])

    audit_prompt_hash = audit_input["audit_campaign"]["audit_prompt_sha256"]
    require_regular(Path("/audit-prompt.md"))
    check_hash("audit_prompt_sha256", Path("/audit-prompt.md"), audit_prompt_hash)

    required_files = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
        TRACE,
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    for path in required_files:
        require_regular(path)
    for path in (
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
    ):
        require_directory(path)
    print("OK all required records and provenance mounts are real/readable")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("OK candidate prompt and translator are byte-identical to trusted mounts")

    candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
    assert candidate_semantics == trusted_semantics
    assert all(
        entry_type in {"directory", "file"}
        for entry_type, _ in candidate_semantics.values()
    )
    print(
        "OK candidate reference-semantics recursively matches trusted tree "
        f"({sum(t == 'file' for t, _ in candidate_semantics.values())} files, "
        f"{sum(t == 'directory' for t, _ in candidate_semantics.values())} dirs)"
    )

    candidate_manifest = tree_manifest(Path("/candidate"))
    bad_candidate_entries = {
        path: value
        for path, value in candidate_manifest.items()
        if value[0] not in {"directory", "file"}
    }
    assert not bad_candidate_entries
    print(
        "OK candidate mount has no symlink/unsupported entries "
        f"({sum(t == 'file' for t, _ in candidate_manifest.values())} files)"
    )

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    evidence_paths = {
        "codex-last.txt": Path("/generation-evidence/codex-last.txt"),
        "codex-output.log": Path("/generation-evidence/codex-output.log"),
        "codex-trace/2026/07/22/"
        "rollout-2026-07-22T21-17-17-019f8cc3-4c6e-76b2-92ed-caa84f89bfad.jsonl": TRACE,
        "legacy-metrics.json": Path("/generation-evidence/legacy-metrics.json"),
        "legacy-run-input.json": Path("/generation-evidence/legacy-run-input.json"),
        "prompt.txt": Path("/generation-evidence/prompt.txt"),
        "usage.json": Path("/generation-evidence/usage.json"),
    }
    for record_name, record in (
        ("invocation", invocation),
        ("generation-result", result),
    ):
        expected_evidence = record["outputs"]["evidence"]
        assert set(expected_evidence) == set(evidence_paths)
        for relative, path in evidence_paths.items():
            require_regular(path)
            check_hash(f"{record_name}:{relative}", path, expected_evidence[relative])
    print("OK invocation and generation-result evidence hashes")

    counts: Counter[str] = Counter()
    parsed_lines: list[dict[str, object]] = []
    with TRACE.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            event = json.loads(line)
            parsed_lines.append(event)
            counts[str(event.get("type", "<missing>"))] += 1
    print(f"OK parsed all {len(parsed_lines)} trace JSON lines")
    print("TRACE TYPES " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    selected = usage["selected_event"]
    assert selected["line_number"] == 733
    selected_event = parsed_lines[selected["line_number"] - 1]
    assert selected_event["type"] == "event_msg"
    payload = selected_event["payload"]
    assert isinstance(payload, dict) and payload["type"] == "token_count"
    print("OK usage selected_event points to trace token_count at line 733")

    print("PROVENANCE_CHECK: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"PROVENANCE_CHECK: FAIL: {error}", file=sys.stderr)
        raise
