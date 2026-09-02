#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GEN = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def tree_entries(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for parent, dirs, files in os.walk(root, topdown=True, followlinks=False):
        names = sorted(dirs + files)
        for name in names:
            path = Path(parent) / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("dir", "")
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256_file(path))
            else:
                result[rel] = (f"other:{stat.S_IFMT(mode):o}", "")
    return result


def canonical_tree_digest(entries: dict[str, tuple[str, str]]) -> str:
    digest = hashlib.sha256()
    for rel, (kind, payload) in sorted(entries.items()):
        digest.update(f"{kind}\0{rel}\0{payload}\n".encode())
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement pipeline-v3's length-delimited tree digest."""
    entries = tree_entries(root)
    digest = hashlib.sha256()
    for rel, (kind, _) in sorted(entries.items()):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        pipeline_kind = "directory" if kind == "dir" else kind
        digest.update(pipeline_kind.encode() + b"\0")
        if kind == "file":
            path = root / rel
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def status(name: str, ok: bool, detail: str = "") -> bool:
    suffix = f" :: {detail}" if detail else ""
    print(f"{'OK' if ok else 'FAIL'} {name}{suffix}")
    return ok


def main() -> int:
    failures = 0
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())

    failures += not status("record_layout pipeline-v3", audit.get("record_layout") == "pipeline-v3")
    failures += not status(
        "semantics mode SUPPLIED_SEMANTICS",
        audit.get("semantics_mode") == "SUPPLIED_SEMANTICS",
    )
    failures += not status("campaign block equals lock JSON", audit.get("audit_campaign") == lock)
    actual_lock_hash = sha256_file(LOCK)
    failures += not status(
        "campaign lock SHA-256",
        actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"],
        actual_lock_hash,
    )

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GEN / "invocation.json",
        GEN / "metrics.json",
        GEN / "runtime-metrics.json",
        GEN / "usage.json",
        GEN / "codex-last.txt",
        GEN / "codex-output.log",
        GEN / "prompt.txt",
    ]
    trace_files = sorted((GEN / "codex-trace").rglob("*"))
    trace_regular = [p for p in trace_files if regular_file(p)]
    for path in required:
        failures += not status(f"required regular file {path}", regular_file(path))
    failures += not status("structured trace has regular files", bool(trace_regular), str(len(trace_regular)))
    failures += not status(
        "no symlinks in required generation records",
        not any(p.is_symlink() for p in required + trace_files),
    )

    direct_hashes = {
        "/run.json": audit["hashes"]["run_manifest_sha256"],
        "/task.json": audit["hashes"]["task_manifest_sha256"],
        "/generation-result.json": audit["hashes"]["stage1_result_sha256"],
        str(GEN / "invocation.json"): audit["hashes"]["stage1_invocation_sha256"],
        str(GEN / "metrics.json"): audit["hashes"]["generation_metrics_sha256"],
        str(GEN / "runtime-metrics.json"): audit["hashes"]["generation_runtime_metrics_sha256"],
        str(GEN / "usage.json"): audit["hashes"]["generation_usage_sha256"],
        str(GEN / "codex-last.txt"): audit["hashes"]["generation_codex_last_sha256"],
        str(GEN / "codex-output.log"): audit["hashes"]["generation_codex_output_sha256"],
        str(GEN / "prompt.txt"): audit["hashes"]["generation_prompt_sha256"],
        str(REFERENCE / "canonical.py"): audit["hashes"]["canonical_sha256"],
        str(REFERENCE / "prompt.py"): audit["hashes"]["trusted_prompt_sha256"],
        str(REFERENCE / "py2mpy.py"): audit["hashes"]["trusted_translator_sha256"],
        str(CANDIDATE / "prompt.py"): audit["hashes"]["candidate_prompt_sha256"],
        str(CANDIDATE / "py2mpy.py"): audit["hashes"]["candidate_translator_sha256"],
    }
    for raw_path, expected in direct_hashes.items():
        path = Path(raw_path)
        actual = sha256_file(path) if regular_file(path) else "MISSING_OR_NONREGULAR"
        failures += not status(f"declared hash {path}", actual == expected, actual)

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GEN / "invocation.json").read_text())
    for record_name, record in (("generation-result", result), ("invocation", invocation)):
        for rel, expected in sorted(record["outputs"]["evidence"].items()):
            path = GEN / rel
            actual = sha256_file(path) if regular_file(path) else "MISSING_OR_NONREGULAR"
            failures += not status(f"{record_name} output hash {rel}", actual == expected, actual)

    candidate_pipeline_hash = pipeline_tree_digest(CANDIDATE)
    failures += not status(
        "candidate pipeline tree hash matches generation-result workspace",
        candidate_pipeline_hash == result["outputs"]["workspace_sha256"],
        candidate_pipeline_hash,
    )
    failures += not status(
        "candidate pipeline tree hash matches invocation workspace",
        candidate_pipeline_hash == invocation["outputs"]["workspace_sha256"],
        candidate_pipeline_hash,
    )
    semantics_pipeline_hash = pipeline_tree_digest(REFERENCE / "reference-semantics")
    task = json.loads(Path("/task.json").read_text())
    failures += not status(
        "trusted semantics pipeline tree hash matches task input",
        semantics_pipeline_hash == task["inputs"]["reference_semantics_sha256"],
        semantics_pipeline_hash,
    )
    failures += not status(
        "trusted semantics pipeline tree hash matches audit manifest input",
        semantics_pipeline_hash == audit["manifest"]["inputs"]["reference_semantics_sha256"],
        semantics_pipeline_hash,
    )
    failures += not status(
        "trusted semantics pipeline tree hash matches recorded manifest hash",
        semantics_pipeline_hash == audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        semantics_pipeline_hash,
    )
    candidate_semantics_pipeline_hash = pipeline_tree_digest(CANDIDATE / "reference-semantics")
    failures += not status(
        "candidate and trusted semantics pipeline tree hashes equal",
        candidate_semantics_pipeline_hash == semantics_pipeline_hash,
        candidate_semantics_pipeline_hash,
    )
    usage = json.loads((GEN / "usage.json").read_text())
    trace_pipeline_hash = pipeline_tree_digest(GEN / "codex-trace")
    failures += not status(
        "trace pipeline tree hash matches usage source trace",
        trace_pipeline_hash == usage["source_trace_sha256"],
        trace_pipeline_hash,
    )

    candidate_prompt = CANDIDATE / "prompt.py"
    trusted_prompt = REFERENCE / "prompt.py"
    candidate_translator = CANDIDATE / "py2mpy.py"
    trusted_translator = REFERENCE / "py2mpy.py"
    failures += not status(
        "candidate prompt byte-identical to trusted",
        candidate_prompt.read_bytes() == trusted_prompt.read_bytes(),
    )
    failures += not status(
        "candidate translator byte-identical to trusted",
        candidate_translator.read_bytes() == trusted_translator.read_bytes(),
    )

    candidate_semantics = CANDIDATE / "reference-semantics"
    trusted_semantics = REFERENCE / "reference-semantics"
    failures += not status("trusted supplied semantics present", trusted_semantics.is_dir())
    failures += not status("candidate supplied semantics present", candidate_semantics.is_dir())
    cand_entries = tree_entries(candidate_semantics)
    ref_entries = tree_entries(trusted_semantics)
    failures += not status(
        "candidate semantics has no symlink/other entries",
        all(kind in {"dir", "file"} for kind, _ in cand_entries.values()),
    )
    failures += not status(
        "trusted semantics has no symlink/other entries",
        all(kind in {"dir", "file"} for kind, _ in ref_entries.values()),
    )
    only_candidate = sorted(set(cand_entries) - set(ref_entries))
    only_trusted = sorted(set(ref_entries) - set(cand_entries))
    changed = sorted(
        rel
        for rel in set(cand_entries) & set(ref_entries)
        if cand_entries[rel] != ref_entries[rel]
    )
    failures += not status("semantics no additional candidate entries", not only_candidate, repr(only_candidate))
    failures += not status("semantics no missing candidate entries", not only_trusted, repr(only_trusted))
    failures += not status("semantics entry types/content identical", not changed, repr(changed))
    print(f"INFO candidate semantics canonical tree digest {canonical_tree_digest(cand_entries)}")
    print(f"INFO trusted semantics canonical tree digest   {canonical_tree_digest(ref_entries)}")

    candidate_all = tree_entries(CANDIDATE)
    print(f"INFO candidate canonical tree digest {canonical_tree_digest(candidate_all)}")
    print(f"INFO candidate entries {len(candidate_all)}")
    symlinks = sorted(rel for rel, (kind, _) in candidate_all.items() if kind == "symlink")
    failures += not status("candidate tree has no symlink entries", not symlinks, repr(symlinks))

    print(f"SUMMARY failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
