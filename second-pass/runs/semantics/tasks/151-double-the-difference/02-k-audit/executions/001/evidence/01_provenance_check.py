#!/usr/bin/env python3
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def regular_nonsymlink(path: Path) -> tuple[bool, str]:
    try:
        st = path.lstat()
    except OSError as err:
        return False, f"unreadable: {err}"
    if stat.S_ISLNK(st.st_mode):
        return False, "symlink"
    if not stat.S_ISREG(st.st_mode):
        return False, f"not regular: mode={oct(st.st_mode)}"
    try:
        with path.open("rb") as stream:
            stream.read(1)
    except OSError as err:
        return False, f"unreadable: {err}"
    return True, f"regular sha256={digest(path)}"


def tree_records(root: Path) -> list[tuple[str, str, int, str]]:
    records = []
    for path in sorted([root, *root.rglob("*")], key=lambda p: str(p.relative_to(root))):
        rel = "." if path == root else str(path.relative_to(root))
        st = path.lstat()
        if stat.S_ISLNK(st.st_mode):
            kind = "symlink"
            content = os.readlink(path)
        elif stat.S_ISDIR(st.st_mode):
            kind = "dir"
            content = ""
        elif stat.S_ISREG(st.st_mode):
            kind = "file"
            content = digest(path)
        else:
            kind = f"other:{stat.S_IFMT(st.st_mode)}"
            content = ""
        records.append((rel, kind, stat.S_IMODE(st.st_mode), content))
    return records


def transparent_tree_digest(records: list[tuple[str, str, int, str]]) -> str:
    encoded = json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def report_check(name: str, ok: bool, detail: str) -> bool:
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    return ok


def main() -> int:
    failures = 0
    data = json.loads(AUDIT_INPUT.read_text())
    hashes = data["hashes"]
    paths = data["container_paths"]

    required_keys = [
        "audit_campaign_lock",
        "candidate",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "generation_root",
        "generation_trace",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    ]
    for key in required_keys:
        p = Path(paths[key])
        exists = p.exists()
        failures += not report_check(f"container path {key}", exists, str(p))

    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    failures += not report_check(
        "campaign lock JSON equals audit campaign block",
        lock == data["audit_campaign"],
        f"lock_keys={len(lock)} block_keys={len(data['audit_campaign'])}",
    )
    actual_lock_hash = digest(lock_path)
    failures += not report_check(
        "campaign lock recorded hash",
        actual_lock_hash == hashes["audit_campaign_lock_sha256"],
        f"actual={actual_lock_hash} recorded={hashes['audit_campaign_lock_sha256']}",
    )

    file_hash_checks = {
        Path(paths["canonical"]): "canonical_sha256",
        Path(paths["trusted_prompt"]): "trusted_prompt_sha256",
        Path(paths["translator"]): "trusted_translator_sha256",
        Path(paths["generation_last"]): "generation_codex_last_sha256",
        Path(paths["generation_manifest"]): "stage1_invocation_sha256",
        Path(paths["generation_metrics"]): "generation_metrics_sha256",
        Path(paths["generation_output"]): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path(paths["run_manifest"]): "run_manifest_sha256",
        Path(paths["stage1_result"]): "stage1_result_sha256",
        Path(paths["task_manifest"]): "task_manifest_sha256",
    }
    for path, key in file_hash_checks.items():
        ok_type, type_detail = regular_nonsymlink(path)
        actual = digest(path) if ok_type else "N/A"
        ok = ok_type and actual == hashes[key]
        failures += not report_check(
            f"record {path}",
            ok,
            f"{type_detail}; recorded_{key}={hashes[key]}",
        )

    required_layout_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_layout_records:
        ok, detail = regular_nonsymlink(path)
        failures += not report_check(f"pipeline-v3 required record {path}", ok, detail)

    trace_root = Path(paths["generation_trace"])
    trace_records = tree_records(trace_root)
    trace_bad = [r for r in trace_records if r[1] not in {"dir", "file"}]
    trace_files = [r for r in trace_records if r[1] == "file"]
    failures += not report_check(
        "structured trace types",
        not trace_bad and bool(trace_files),
        f"files={len(trace_files)} bad_entries={trace_bad}",
    )
    result = json.loads(Path(paths["stage1_result"]).read_text())
    expected_outputs = result["outputs"]["evidence"]
    for rel, expected in expected_outputs.items():
        artifact = Path("/generation-evidence") / rel
        ok, detail = regular_nonsymlink(artifact)
        actual = digest(artifact) if ok else "N/A"
        failures += not report_check(
            f"generation-result artifact {rel}",
            ok and actual == expected,
            f"{detail}; generation-result={expected}",
        )

    candidate_prompt = Path(paths["candidate"]) / "prompt.py"
    candidate_translator = Path(paths["candidate"]) / "py2mpy.py"
    for name, candidate_path, trusted_path in [
        ("candidate prompt byte identity", candidate_prompt, Path(paths["trusted_prompt"])),
        ("candidate translator byte identity", candidate_translator, Path(paths["translator"])),
    ]:
        candidate_ok, candidate_detail = regular_nonsymlink(candidate_path)
        trusted_ok, trusted_detail = regular_nonsymlink(trusted_path)
        same = candidate_ok and trusted_ok and candidate_path.read_bytes() == trusted_path.read_bytes()
        failures += not report_check(
            name,
            same,
            f"candidate={candidate_detail}; trusted={trusted_detail}",
        )

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path(paths["candidate"]) / "reference-semantics"
    trusted_records = tree_records(trusted_semantics)
    candidate_records = tree_records(candidate_semantics)
    same_semantics = trusted_records == candidate_records
    failures += not report_check(
        "supplied semantics recursive exact identity including types/modes/content",
        same_semantics,
        (
            f"trusted_entries={len(trusted_records)} candidate_entries={len(candidate_records)} "
            f"trusted_transparent_digest={transparent_tree_digest(trusted_records)} "
            f"candidate_transparent_digest={transparent_tree_digest(candidate_records)}"
        ),
    )
    if not same_semantics:
        trusted_set = set(trusted_records)
        candidate_set = set(candidate_records)
        print("ONLY_TRUSTED", sorted(trusted_set - candidate_set))
        print("ONLY_CANDIDATE", sorted(candidate_set - trusted_set))

    for root_name, root in [
        ("candidate", Path(paths["candidate"])),
        ("reference", Path("/reference")),
        ("generation-evidence", Path("/generation-evidence")),
    ]:
        records = tree_records(root)
        links = [r for r in records if r[1] == "symlink"]
        others = [r for r in records if not (r[1] in {"dir", "file", "symlink"})]
        failures += not report_check(
            f"{root_name} tree has no symlinks or special entries",
            not links and not others,
            f"entries={len(records)} symlinks={links} other={others}",
        )
        print(
            f"INFO {root_name} transparent_tree_digest={transparent_tree_digest(records)} "
            f"entries={len(records)}"
        )

    print(f"SUMMARY failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
