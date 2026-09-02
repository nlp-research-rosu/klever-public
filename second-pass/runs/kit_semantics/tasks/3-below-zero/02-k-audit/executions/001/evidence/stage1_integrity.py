#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import stat


AI = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")


def file_digest(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_digest(root: Path) -> tuple[str, int]:
    """Reimplement the launcher tree format to verify recorded tree digests."""
    digest = sha256()
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest(), len(entries)


def assert_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required record is not regular: {path}"
    assert os.access(path, os.R_OK), f"required record is unreadable: {path}"


def compare_trees(left: Path, right: Path) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        answer: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            mode = path.lstat().st_mode
            rel = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                answer[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                answer[rel] = ("file", file_digest(path))
            else:
                answer[rel] = ("unsupported", None)
        return answer

    lentries = entries(left)
    rentries = entries(right)
    assert lentries == rentries, "candidate and trusted semantics trees differ"
    print(f"semantics_recursive_compare=IDENTICAL entries={len(lentries)}")


def main() -> None:
    ai = json.loads(AI.read_text())
    lock = json.loads(LOCK.read_text())
    assert ai["record_layout"] == "pipeline-v3"
    assert ai["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert ai["audit_campaign"] == lock
    print("campaign_lock_block=MATCH")

    required_directories = [
        Path("/candidate"),
        GEN,
        GEN / "codex-trace",
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]
    for directory in required_directories:
        mode = directory.lstat().st_mode
        assert stat.S_ISDIR(mode), f"required directory is linked/non-directory: {directory}"
        print(f"real_directory={directory}")

    for name in (
        "solution.py", "solution.mpy", "verification.k", "spec.k",
        "prove.sh", "PROOF.md",
    ):
        assert_regular(Path("/candidate") / name)
        print(f"candidate_required_artifact=regular path=/candidate/{name}")

    expected_files = {
        LOCK: "audit_campaign_lock_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        GEN / "invocation.json": "stage1_invocation_sha256",
        GEN / "metrics.json": "generation_metrics_sha256",
        GEN / "runtime-metrics.json": "generation_runtime_metrics_sha256",
        GEN / "usage.json": "generation_usage_sha256",
        GEN / "codex-last.txt": "generation_codex_last_sha256",
        GEN / "codex-output.log": "generation_codex_output_sha256",
        GEN / "prompt.txt": "generation_prompt_sha256",
    }
    for path, key in expected_files.items():
        assert_regular(path)
        actual = file_digest(path)
        expected = ai["hashes"][key]
        assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"
        print(f"hash={actual} path={path}")

    trace_files = sorted((GEN / "codex-trace").rglob("*.jsonl"))
    assert len(trace_files) == 1, f"unexpected trace file count: {len(trace_files)}"
    assert_regular(trace_files[0])
    invocation = json.loads((GEN / "invocation.json").read_text())
    rel = trace_files[0].relative_to(GEN).as_posix()
    assert file_digest(trace_files[0]) == invocation["outputs"]["evidence"][rel]
    trace_hash, trace_entry_count = tree_digest(GEN / "codex-trace")
    # The audit manifest carries a second launcher aggregate produced by the
    # host's audit-record builder.  Its serialization is not exposed in this
    # container.  Independently compute the mounted tree using the pipeline-v3
    # tree format, and verify that digest against usage.json below.
    print(f"trace_pipeline_tree_hash={trace_hash} entries={trace_entry_count}")
    print(
        "trace_audit_record_aggregate="
        + ai["hashes"]["generation_codex_trace_sha256"]
    )

    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    final_messages = 0
    trace_lines = 0
    with trace_files[0].open(encoding="utf-8") as stream:
        for trace_lines, line in enumerate(stream, 1):
            event = json.loads(line)
            event_types[event.get("type", "<missing>")] += 1
            payload = event.get("payload", {})
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<missing>"))] += 1
                if payload.get("type") == "custom_tool_call":
                    tool_names[str(payload.get("name"))] += 1
                if payload.get("type") == "message" and payload.get("role") == "assistant":
                    if payload.get("phase") == "final_answer":
                        final_messages += 1
    print(f"trace_jsonl_lines_parsed={trace_lines}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_tool_names={dict(sorted(tool_names.items()))}")
    print(f"trace_final_assistant_messages={final_messages}")
    usage = json.loads((GEN / "usage.json").read_text())
    assert trace_hash == usage["source_trace_sha256"]
    print("trace_pipeline_tree_vs_usage=MATCH")

    output_text = (GEN / "codex-output.log").read_text(errors="replace")
    print(f"codex_output_chars_scanned={len(output_text)}")
    print(f"codex_output_top_mentions={output_text.count('#Top')}")
    print(f"codex_output_warn_stuck_mentions={output_text.count('WarnStuckClaimState')}")
    assert "RESULT: KPROVE_PASSED" in output_text

    compare_trees(Path("/candidate/reference-semantics"), Path("/reference/reference-semantics"))
    trusted_tree_hash, trusted_count = tree_digest(Path("/reference/reference-semantics"))
    candidate_tree_hash, candidate_count = tree_digest(Path("/candidate/reference-semantics"))
    expected_manifest = ai["hashes"]["trusted_reference_semantics_manifest_sha256"]
    assert trusted_tree_hash == expected_manifest
    assert candidate_tree_hash == expected_manifest
    print(f"semantics_manifest_hash={trusted_tree_hash} entries={trusted_count}/{candidate_count}")
    print(
        "semantics_audit_record_content_aggregate="
        + ai["hashes"]["trusted_reference_semantics_sha256"]
    )

    candidate_workspace_hash, workspace_entries = tree_digest(Path("/candidate"))
    generation_result = json.loads(Path("/generation-result.json").read_text())
    assert candidate_workspace_hash == generation_result["outputs"]["workspace_sha256"]
    print(f"candidate_workspace_tree_hash={candidate_workspace_hash} entries={workspace_entries}")

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate_prompt_vs_trusted=BYTE_IDENTICAL")
    print("candidate_translator_vs_trusted=BYTE_IDENTICAL")


if __name__ == "__main__":
    main()
