#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the installed pipeline_contract.sha256_tree algorithm."""
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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


def load_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    audit = load_json(AUDIT_INPUT)
    lock = load_json(Path(audit["container_paths"]["audit_campaign_lock"]))
    generation_result = load_json(Path(audit["container_paths"]["stage1_result"]))
    usage = load_json(Path("/generation-evidence/usage.json"))

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_block_equal_lock={audit['audit_campaign'] == lock}")
    print(
        "campaign_lock_hash "
        f"recorded={audit['hashes']['audit_campaign_lock_sha256']} "
        f"actual={file_sha256(Path('/audit-campaign-lock.json'))}"
    )

    declared_files = {
        "canonical": Path(audit["container_paths"]["canonical"]),
        "candidate": Path(audit["container_paths"]["candidate"]),
        "generation_last": Path(audit["container_paths"]["generation_last"]),
        "generation_manifest": Path(audit["container_paths"]["generation_manifest"]),
        "generation_metrics": Path(audit["container_paths"]["generation_metrics"]),
        "generation_output": Path(audit["container_paths"]["generation_output"]),
        "generation_root": Path(audit["container_paths"]["generation_root"]),
        "generation_trace": Path(audit["container_paths"]["generation_trace"]),
        "run_manifest": Path(audit["container_paths"]["run_manifest"]),
        "stage1_result": Path(audit["container_paths"]["stage1_result"]),
        "task_manifest": Path(audit["container_paths"]["task_manifest"]),
        "translator": Path(audit["container_paths"]["translator"]),
        "trusted_prompt": Path(audit["container_paths"]["trusted_prompt"]),
    }
    for label, path in declared_files.items():
        status = "directory" if path.is_dir() else "file" if path.is_file() else "MISSING"
        print(f"declared_mount {label} {status} {path}")

    required_pipeline_v3 = [
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
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_pipeline_v3:
        print(f"required_record {path} exists={path.exists()} symlink={path.is_symlink()}")

    hash_paths = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
    }
    for key, path in hash_paths.items():
        actual = file_sha256(path)
        recorded = audit["hashes"][key]
        print(f"file_hash {key} match={actual == recorded} recorded={recorded} actual={actual}")

    candidate_tree = pipeline_tree_sha256(Path("/candidate"))
    trace_tree = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
    print(
        "candidate_tree "
        f"audit_recorded={audit['hashes']['candidate_tree_sha256']} "
        f"pipeline_computed={candidate_tree} "
        f"generation_result={generation_result['outputs']['workspace_sha256']}"
    )
    print(
        "trace_tree "
        f"audit_recorded={audit['hashes']['generation_codex_trace_sha256']} "
        f"pipeline_computed={trace_tree} "
        f"usage_source_trace={usage['source_trace_sha256']}"
    )

    print(
        "candidate_prompt_byte_equal_trusted="
        f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
    )
    print(
        "candidate_translator_byte_equal_trusted="
        f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
    )
    print(
        "trusted_reference_semantics_absent="
        f"{not Path('/reference/reference-semantics').exists()}"
    )

    roots = [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]
    links = [str(path) for root in roots for path in root.rglob("*") if path.is_symlink()]
    print(f"symlink_count={len(links)}")
    for path in links:
        print(f"symlink={path}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    trace_counts: Counter[str] = Counter()
    invalid_lines: list[str] = []
    trace_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for trace_lines, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as error:
                    invalid_lines.append(f"{path}:{trace_lines}:{error}")
                    continue
                trace_counts[event.get("type", "<missing>")] += 1
        expected = generation_result["outputs"]["evidence"].get(
            str(path.relative_to("/generation-evidence"))
        )
        print(
            f"trace_file {path} lines={trace_lines} "
            f"hash={file_sha256(path)} expected={expected}"
        )
    print(f"trace_type_counts={dict(sorted(trace_counts.items()))}")
    print(f"trace_invalid_lines={invalid_lines}")

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in proof_artifacts:
        path = Path("/candidate") / name
        print(
            f"candidate_artifact {name} regular={path.is_file() and not path.is_symlink()} "
            f"sha256={file_sha256(path) if path.is_file() else 'MISSING'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
