#!/usr/bin/env python3
"""Independent integrity and generation-record inspection for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_manifest(root: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        directory = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = directory / name
            st = path.lstat()
            rel = path.relative_to(root).as_posix()
            if stat.S_ISLNK(st.st_mode):
                kind = "symlink"
            elif stat.S_ISDIR(st.st_mode):
                kind = "directory"
            elif stat.S_ISREG(st.st_mode):
                kind = "file"
            else:
                kind = "other"
            record: dict[str, object] = {
                "path": rel,
                "kind": kind,
                "mode": stat.S_IMODE(st.st_mode),
                "size": st.st_size,
            }
            if kind == "file":
                record["sha256"] = sha256_file(path)
            elif kind == "symlink":
                record["target"] = os.readlink(path)
            entries.append(record)
    return sorted(entries, key=lambda item: str(item["path"]))


def length_delimited_tree_sha256(root: Path) -> str:
    """Recompute the launcher's documented path/kind/size/content tree digest."""
    manifest = tree_manifest(root)
    digest = hashlib.sha256()
    for entry in manifest:
        rel = str(entry["path"]).encode()
        kind = str(entry["kind"])
        digest.update(len(rel).to_bytes(4, "big"))
        digest.update(rel)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(int(entry["size"]).to_bytes(8, "big"))
            path = root / str(entry["path"])
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def load_object(path: Path) -> dict[str, object]:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"not a real regular file: {path}")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise RuntimeError(f"not a JSON object: {path}")
    return value


def main() -> None:
    audit = load_object(AUDIT_INPUT)
    lock_path = Path(str(audit["container_paths"]["audit_campaign_lock"]))
    lock = load_object(lock_path)
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_block_equals_lock={audit['audit_campaign'] == lock}")
    print(f"campaign_lock_sha256={sha256_file(lock_path)}")
    print(
        "campaign_lock_hash_matches="
        f"{sha256_file(lock_path) == audit['hashes']['audit_campaign_lock_sha256']}"
    )

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    print("required_records:")
    for path in required:
        kind_ok = path.is_file() and not path.is_symlink()
        print(
            f"  {path}: regular_non_symlink={kind_ok} "
            f"sha256={sha256_file(path) if kind_ok else 'N/A'}"
        )

    recorded_hash_paths = {
        "audit_campaign_lock_sha256": lock_path,
        "canonical_sha256": Path(str(audit["container_paths"]["canonical"])),
        "trusted_prompt_sha256": Path(
            str(audit["container_paths"]["trusted_prompt"])
        ),
        "trusted_translator_sha256": Path(
            str(audit["container_paths"]["translator"])
        ),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path(
            str(audit["container_paths"]["generation_last"])
        ),
        "generation_codex_output_sha256": Path(
            str(audit["container_paths"]["generation_output"])
        ),
        "generation_metrics_sha256": Path(
            str(audit["container_paths"]["generation_metrics"])
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path(str(audit["container_paths"]["run_manifest"])),
        "task_manifest_sha256": Path(
            str(audit["container_paths"]["task_manifest"])
        ),
        "stage1_result_sha256": Path(
            str(audit["container_paths"]["stage1_result"])
        ),
        "stage1_invocation_sha256": Path(
            str(audit["container_paths"]["generation_manifest"])
        ),
    }
    print("recorded_file_hash_comparisons:")
    for key, path in recorded_hash_paths.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        print(
            f"  {key}: matches={actual == expected} "
            f"expected={expected} actual={actual} path={path}"
        )

    candidate_manifest = tree_manifest(Path("/candidate"))
    trace_root = Path(str(audit["container_paths"]["generation_trace"]))
    trace_manifest = tree_manifest(trace_root)
    print("candidate_manifest:")
    print(json.dumps(candidate_manifest, indent=2, sort_keys=True))
    print("trace_manifest:")
    print(json.dumps(trace_manifest, indent=2, sort_keys=True))
    print(
        "candidate_has_unsupported_entries="
        f"{any(e['kind'] not in ('file', 'directory') for e in candidate_manifest)}"
    )
    print(
        "trace_has_unsupported_entries="
        f"{any(e['kind'] not in ('file', 'directory') for e in trace_manifest)}"
    )
    candidate_tree_actual = length_delimited_tree_sha256(Path("/candidate"))
    trace_tree_actual = length_delimited_tree_sha256(trace_root)
    print(
        "candidate_tree_hash: "
        f"matches={candidate_tree_actual == audit['hashes']['candidate_tree_sha256']} "
        f"expected={audit['hashes']['candidate_tree_sha256']} "
        f"actual={candidate_tree_actual}"
    )
    print(
        "generation_trace_tree_hash: "
        f"matches={trace_tree_actual == audit['hashes']['generation_codex_trace_sha256']} "
        f"expected={audit['hashes']['generation_codex_trace_sha256']} "
        f"actual={trace_tree_actual}"
    )

    trace_files = [e for e in trace_manifest if e["kind"] == "file"]
    generation_result = load_object(Path("/generation-result.json"))
    declared_evidence = generation_result["outputs"]["evidence"]
    print("generation_result_evidence_hash_comparisons:")
    for rel, expected in sorted(declared_evidence.items()):
        path = Path("/generation-evidence") / rel
        actual = sha256_file(path)
        print(
            f"  {rel}: matches={actual == expected} "
            f"expected={expected} actual={actual}"
        )
    print(f"trace_file_count={len(trace_files)}")

    event_counts: Counter[tuple[str, str]] = Counter()
    tool_calls: list[tuple[int, str, str]] = []
    final_messages: list[str] = []
    for trace_entry in trace_files:
        trace_path = trace_root / str(trace_entry["path"])
        with trace_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                item = json.loads(line)
                outer = str(item.get("type", ""))
                payload = item.get("payload")
                inner = str(payload.get("type", "")) if isinstance(payload, dict) else ""
                event_counts[(outer, inner)] += 1
                if inner in ("custom_tool_call", "function_call"):
                    tool_calls.append(
                        (
                            line_number,
                            str(payload.get("name", "")),
                            str(payload.get("input", payload.get("arguments", ""))),
                        )
                    )
                if outer == "event_msg" and inner == "agent_message":
                    final_messages.append(str(payload.get("message", "")))
    print("trace_event_counts:")
    for key, count in sorted(event_counts.items()):
        print(f"  {key}: {count}")
    print(f"trace_tool_call_count={len(tool_calls)}")
    for line_number, name, input_text in tool_calls:
        compact = " ".join(input_text.split())
        print(f"  line={line_number} name={name} input={compact[:500]}")
    print("trace_agent_messages:")
    for message in final_messages:
        print("  " + " ".join(message.split())[:1000])

    output_path = Path("/generation-evidence/codex-output.log")
    output_text = output_path.read_text(errors="replace")
    last_text = Path("/generation-evidence/codex-last.txt").read_text(
        errors="replace"
    )
    print(f"codex_output_chars_read={len(output_text)}")
    print(f"codex_output_lines={output_text.count(chr(10))}")
    print(f"codex_output_top_occurrences={output_text.count('#Top')}")
    print(f"codex_output_warnstuck_occurrences={output_text.count('WarnStuck')}")
    print(f"codex_output_result_marker_occurrences={output_text.count('KPROVE_PASSED')}")
    print(f"codex_last_chars_read={len(last_text)}")
    print(f"codex_last={' '.join(last_text.split())}")


if __name__ == "__main__":
    main()
