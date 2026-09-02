#!/usr/bin/env python3
"""Read-only provenance checks for the 87-get-row audit."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


AUDIT_INPUT = Path("/audit-input.json")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce the stage-1 workspace tree hash algorithm."""
    root = root.resolve(strict=True)
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise RuntimeError(f"linked or unsupported entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a regular file: {path}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_structural_equal={audit['audit_campaign'] == lock}")

    required = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/semantic.k"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
    ]
    traces = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    required.extend(traces)
    for path in required:
        require_regular(path)
        print(f"sha256 {file_hash(path)} {path}")

    checks = {
        "/audit-campaign-lock.json": audit["hashes"]["audit_campaign_lock_sha256"],
        "/run.json": audit["hashes"]["run_manifest_sha256"],
        "/task.json": audit["hashes"]["task_manifest_sha256"],
        "/generation-result.json": audit["hashes"]["stage1_result_sha256"],
        "/generation-evidence/invocation.json": audit["hashes"]["stage1_invocation_sha256"],
        "/generation-evidence/metrics.json": audit["hashes"]["generation_metrics_sha256"],
        "/generation-evidence/usage.json": audit["hashes"]["generation_usage_sha256"],
        "/generation-evidence/codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
        "/generation-evidence/codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
        "/generation-evidence/prompt.txt": audit["hashes"]["generation_prompt_sha256"],
        "/reference/canonical.py": audit["hashes"]["canonical_sha256"],
        "/reference/prompt.py": audit["hashes"]["trusted_prompt_sha256"],
        "/reference/py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
        "/candidate/prompt.py": audit["hashes"]["candidate_prompt_sha256"],
        "/candidate/py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
    }
    for name, expected in checks.items():
        actual = file_hash(Path(name))
        print(f"recorded_hash_match={actual == expected} path={name}")

    print(
        "candidate_prompt_byte_equal=",
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes(),
        sep="",
    )
    print(
        "candidate_translator_byte_equal=",
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
        sep="",
    )
    print(
        "reference_semantics_absent=",
        not Path("/reference/reference-semantics").exists(),
        sep="",
    )

    links = [
        str(path)
        for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence"))
        for path in root.rglob("*")
        if path.is_symlink()
    ]
    print(f"symlinks={links}")

    candidate_digest = pipeline_tree_hash(Path("/candidate"))
    trace_digest = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
    print(f"candidate_pipeline_tree_sha256={candidate_digest}")
    print(
        "candidate_matches_invocation_workspace=",
        candidate_digest == invocation["retained_workspace_sha256"],
        sep="",
    )
    print(
        "candidate_matches_result_workspace=",
        candidate_digest == result["outputs"]["workspace_sha256"],
        sep="",
    )
    print(f"trace_pipeline_tree_sha256={trace_digest}")

    trace_events: Counter[tuple[str, str]] = Counter()
    custom_calls: Counter[str] = Counter()
    for trace in traces:
        with trace.open() as stream:
            for line in stream:
                event = json.loads(line)
                payload = event.get("payload", {})
                trace_events[(event.get("type", "?"), payload.get("type", "-"))] += 1
                if (
                    event.get("type") == "response_item"
                    and payload.get("type") == "custom_tool_call"
                ):
                    custom_calls[payload.get("name", "?")] += 1
    print(f"trace_files={len(traces)}")
    print("trace_event_inventory:")
    for key, count in sorted(trace_events.items()):
        print(f"  {count} {key[0]} {key[1]}")
    print(f"trace_custom_calls={dict(custom_calls)}")


if __name__ == "__main__":
    main()
