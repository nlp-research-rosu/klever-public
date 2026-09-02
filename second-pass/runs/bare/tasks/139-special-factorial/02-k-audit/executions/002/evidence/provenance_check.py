#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

The output is intentionally line-oriented so the terminal transcript is a
bounded, reviewer-readable record of every comparison.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_sha256_tree(root: Path) -> str:
    """Reproduce the pipeline workspace/trace tree format from first principles.

    Each sorted entry contributes its relative path, kind, and (for files)
    size/content. Symlinks and special entries are rejected.
    """

    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
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


def audit_sha256_tree(root: Path) -> str:
    """Reproduce the audit-input tree format from first principles."""

    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def check(label: str, actual: object, expected: object) -> bool:
    ok = actual == expected
    print(
        f"{'PASS' if ok else 'FAIL'} {label}\n"
        f"  actual:   {actual}\n"
        f"  expected: {expected}"
    )
    return ok


def require_regular(label: str, path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        print(f"FAIL {label}: unreadable/missing {path}: {error}")
        return False
    ok = stat.S_ISREG(mode) and not path.is_symlink() and os.access(path, os.R_OK)
    print(
        f"{'PASS' if ok else 'FAIL'} {label}: "
        f"path={path} type={'regular' if stat.S_ISREG(mode) else oct(mode)} "
        f"symlink={path.is_symlink()} readable={os.access(path, os.R_OK)}"
    )
    return ok


def require_directory(label: str, path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        print(f"FAIL {label}: unreadable/missing {path}: {error}")
        return False
    ok = stat.S_ISDIR(mode) and not path.is_symlink() and os.access(path, os.R_OK)
    print(
        f"{'PASS' if ok else 'FAIL'} {label}: "
        f"path={path} type={'directory' if stat.S_ISDIR(mode) else oct(mode)} "
        f"symlink={path.is_symlink()} readable={os.access(path, os.R_OK)}"
    )
    return ok


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text())
    expected = document["hashes"]
    paths = document["container_paths"]
    failures = 0

    print(f"record_layout={document['record_layout']}")
    print(f"semantics_mode={document['semantics_mode']}")
    failures += not check(
        "record layout", document["record_layout"], "legacy-selected-stage1"
    )
    failures += not check(
        "rendered semantics mode",
        document["semantics_mode"],
        "GENERATED_SEMANTICS",
    )

    required_regular = {
        "audit input": AUDIT_INPUT,
        "campaign lock": Path(paths["audit_campaign_lock"]),
        "run manifest": Path(paths["run_manifest"]),
        "task manifest": Path(paths["task_manifest"]),
        "stage-1 result": Path(paths["stage1_result"]),
        "generation invocation": Path(paths["generation_manifest"]),
        "generation metrics": Path(paths["generation_metrics"]),
        "generation usage": Path("/generation-evidence/usage.json"),
        "generation last": Path(paths["generation_last"]),
        "generation output": Path(paths["generation_output"]),
        "generation prompt": Path("/generation-evidence/prompt.txt"),
        "canonical": Path(paths["canonical"]),
        "trusted prompt": Path(paths["trusted_prompt"]),
        "translator": Path(paths["translator"]),
        "candidate prompt": Path(paths["candidate"]) / "prompt.py",
        "candidate translator": Path(paths["candidate"]) / "py2mpy.py",
    }
    for label, path in required_regular.items():
        failures += not require_regular(label, path)

    required_directories = {
        "candidate tree": Path(paths["candidate"]),
        "generation root": Path(paths["generation_root"]),
        "generation trace": Path(paths["generation_trace"]),
    }
    for label, path in required_directories.items():
        failures += not require_directory(label, path)

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path(paths["candidate"]) / "reference-semantics"
    failures += not check(
        "trusted reference semantics absent",
        trusted_semantics.exists() or trusted_semantics.is_symlink(),
        False,
    )
    failures += not check(
        "candidate reference semantics absent",
        candidate_semantics.exists() or candidate_semantics.is_symlink(),
        False,
    )

    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    failures += not check("campaign block equals campaign lock", lock, document["audit_campaign"])
    failures += not check(
        "campaign lock sha256",
        sha256_file(lock_path),
        expected["audit_campaign_lock_sha256"],
    )

    file_hash_checks = {
        "candidate prompt sha256": (
            Path(paths["candidate"]) / "prompt.py",
            expected["candidate_prompt_sha256"],
        ),
        "candidate translator sha256": (
            Path(paths["candidate"]) / "py2mpy.py",
            expected["candidate_translator_sha256"],
        ),
        "trusted canonical sha256": (
            Path(paths["canonical"]),
            expected["canonical_sha256"],
        ),
        "trusted prompt sha256": (
            Path(paths["trusted_prompt"]),
            expected["trusted_prompt_sha256"],
        ),
        "trusted translator sha256": (
            Path(paths["translator"]),
            expected["trusted_translator_sha256"],
        ),
        "run manifest sha256": (
            Path(paths["run_manifest"]),
            expected["run_manifest_sha256"],
        ),
        "task manifest sha256": (
            Path(paths["task_manifest"]),
            expected["task_manifest_sha256"],
        ),
        "stage-1 result sha256": (
            Path(paths["stage1_result"]),
            expected["stage1_result_sha256"],
        ),
        "generation invocation sha256": (
            Path(paths["generation_manifest"]),
            expected["stage1_invocation_sha256"],
        ),
        "generation metrics sha256": (
            Path(paths["generation_metrics"]),
            expected["generation_metrics_sha256"],
        ),
        "generation usage sha256": (
            Path("/generation-evidence/usage.json"),
            expected["generation_usage_sha256"],
        ),
        "generation last sha256": (
            Path(paths["generation_last"]),
            expected["generation_codex_last_sha256"],
        ),
        "generation output sha256": (
            Path(paths["generation_output"]),
            expected["generation_codex_output_sha256"],
        ),
        "generation prompt sha256": (
            Path("/generation-evidence/prompt.txt"),
            expected["generation_prompt_sha256"],
        ),
    }
    for label, (path, digest) in file_hash_checks.items():
        failures += not check(label, sha256_file(path), digest)

    failures += not check(
        "manifest sha256 aliases task manifest",
        sha256_file(Path(paths["task_manifest"])),
        expected["manifest_sha256"],
    )
    # audit-input does not declare the serialization used by its two aggregate
    # "*_tree_sha256" convenience fields. Record them and an independent
    # content/tree digest without pretending that a different serialization is
    # a byte-integrity failure. The constituent file hashes and the separately
    # recorded pipeline tree hashes below are directly reproducible.
    print(
        "INFO candidate audit aggregate "
        f"recorded={expected['candidate_tree_sha256']} "
        f"independent_content_tree={audit_sha256_tree(Path(paths['candidate']))}"
    )
    print(
        "INFO generation trace audit aggregate "
        f"recorded={expected['generation_codex_trace_sha256']} "
        "independent_content_tree="
        f"{audit_sha256_tree(Path(paths['generation_trace']))}"
    )
    result = json.loads(Path(paths["stage1_result"]).read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    failures += not check(
        "candidate pipeline workspace sha256",
        pipeline_sha256_tree(Path(paths["candidate"])),
        result["outputs"]["workspace_sha256"],
    )
    failures += not check(
        "generation trace pipeline sha256",
        pipeline_sha256_tree(Path(paths["generation_trace"])),
        usage["source_trace_sha256"],
    )

    failures += not check(
        "candidate prompt byte identity",
        (Path(paths["candidate"]) / "prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes(),
        True,
    )
    failures += not check(
        "candidate translator byte identity",
        (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes(),
        True,
    )

    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    for record_name, recorded_hash in sorted(
        invocation["outputs"]["evidence"].items()
    ):
        record_path = Path(paths["generation_root"]) / record_name
        failures += not require_regular(f"invocation output {record_name}", record_path)
        failures += not check(
            f"invocation output hash {record_name}",
            sha256_file(record_path),
            recorded_hash,
        )
    for record_name, recorded_hash in sorted(result["outputs"]["evidence"].items()):
        record_path = Path(paths["generation_root"]) / record_name
        failures += not require_regular(f"result output {record_name}", record_path)
        failures += not check(
            f"result output hash {record_name}",
            sha256_file(record_path),
            recorded_hash,
        )

    print("CANDIDATE_FILE_MANIFEST")
    for path in sorted(Path(paths["candidate"]).rglob("*")):
        relative = path.relative_to(Path(paths["candidate"])).as_posix()
        if path.is_symlink():
            print(f"  SYMLINK {relative} -> {os.readlink(path)}")
            failures += 1
        elif path.is_dir():
            print(f"  DIR {relative}")
        elif path.is_file():
            print(
                f"  FILE {relative} size={path.stat().st_size} "
                f"sha256={sha256_file(path)}"
            )
        else:
            print(f"  UNSUPPORTED {relative}")
            failures += 1

    print(f"SUMMARY failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
