#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned pipeline-v3 mounts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
import pipeline_contract  # type: ignore  # launcher pipeline hash implementation


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def real_directory(path: Path) -> bool:
    try:
        return stat.S_ISDIR(path.lstat().st_mode)
    except OSError:
        return False


def check(label: str, condition: bool, details: str = "") -> None:
    print(f"{label}: {'PASS' if condition else 'FAIL'}{details}")
    if not condition:
        raise SystemExit(1)


def main() -> None:
    check("audit_input_regular", regular(AUDIT_INPUT))
    check("campaign_lock_regular", regular(LOCK))
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    check("record_layout", audit["record_layout"] == "pipeline-v3")
    check("problem_id", audit["problem_id"] == "156-int-to-mini-roman")
    check("condition", audit["condition"] == "bare")
    check("semantics_mode", audit["semantics_mode"] == "GENERATED_SEMANTICS")
    check("campaign_content", audit["audit_campaign"] == lock)
    check(
        "campaign_lock_sha256",
        sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"],
        f" actual={sha256(LOCK)}",
    )

    container = audit["container_paths"]
    required_files = {
        "run_manifest": Path(container["run_manifest"]),
        "task_manifest": Path(container["task_manifest"]),
        "stage1_result": Path(container["stage1_result"]),
        "generation_manifest": Path(container["generation_manifest"]),
        "generation_metrics": Path(container["generation_metrics"]),
        "generation_last": Path(container["generation_last"]),
        "generation_output": Path(container["generation_output"]),
        "canonical": Path(container["canonical"]),
        "trusted_prompt": Path(container["trusted_prompt"]),
        "translator": Path(container["translator"]),
        "prompt.txt": Path("/generation-evidence/prompt.txt"),
        "runtime-metrics.json": Path("/generation-evidence/runtime-metrics.json"),
        "usage.json": Path("/generation-evidence/usage.json"),
    }
    for label, path in required_files.items():
        check(f"required_regular[{label}]", regular(path), f" path={path}")

    required_directories = {
        "candidate": Path(container["candidate"]),
        "generation_root": Path(container["generation_root"]),
        "generation_trace": Path(container["generation_trace"]),
    }
    for label, path in required_directories.items():
        check(f"required_real_directory[{label}]", real_directory(path), f" path={path}")

    all_scoped_roots = [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]
    links = sorted(
        str(path)
        for root in all_scoped_roots
        for path in root.rglob("*")
        if path.is_symlink()
    )
    check("no_scoped_symlinks", not links, f" links={links}")
    check(
        "generated_semantics_boundary",
        not Path("/reference/reference-semantics").exists(),
    )

    hash_bindings = {
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    }
    for key, path in hash_bindings.items():
        actual = sha256(path)
        expected = audit["hashes"][key]
        check(f"recorded_hash[{key}]", actual == expected, f" actual={actual}")

    check(
        "candidate_prompt_byte_identity",
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes(),
    )
    check(
        "candidate_translator_byte_identity",
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
    )

    run = json.loads(Path("/run.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    check("run_task_condition", run["condition"] == task["condition"] == audit["manifest"]["condition"])
    check(
        "run_audit_config",
        run["config"]
        == audit["config"]
        == audit["manifest_config"]
        == audit["manifest"]["config"],
    )
    embedded_task = dict(audit["manifest"])
    embedded_task.pop("config")
    check("task_manifest_embedded_except_enrichment", task == embedded_task)
    check("task_problem", task["problem_id"] == audit["problem_id"])
    check("result_invocation_name", result["invocation"] == invocation["name"])
    check("result_session", result["session_id"] == invocation["session_id"])
    check("result_status", result["status"] == invocation["status"] == "SUCCEEDED")
    check("result_outputs", result["outputs"] == invocation["outputs"])

    evidence_outputs = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_outputs.items()):
        path = Path("/generation-evidence") / relative
        check(f"result_evidence_regular[{relative}]", regular(path), f" path={path}")
        actual = sha256(path)
        check(
            f"result_evidence_hash[{relative}]",
            actual == expected,
            f" actual={actual}",
        )

    candidate_pipeline_hash = pipeline_contract.sha256_tree(Path("/candidate"))
    trace_pipeline_hash = pipeline_contract.sha256_tree(
        Path("/generation-evidence/codex-trace")
    )
    check(
        "candidate_tree_matches_pipeline_result",
        candidate_pipeline_hash == result["outputs"]["workspace_sha256"],
        f" actual={candidate_pipeline_hash}",
    )
    check(
        "trace_tree_matches_usage_source",
        trace_pipeline_hash == usage["source_trace_sha256"],
        f" actual={trace_pipeline_hash}",
    )
    print(
        "launcher_recorded_candidate_tree_sha256="
        + audit["hashes"]["candidate_tree_sha256"]
    )
    print(
        "launcher_recorded_trace_tree_sha256="
        + audit["hashes"]["generation_codex_trace_sha256"]
    )
    print("note=tree values above use an undeclared launcher serialization; "
          "content identity is independently established by the pipeline-v3 "
          "workspace/source-trace hashes and every per-file evidence hash")

    trace_files = sorted(
        path
        for path in Path("/generation-evidence/codex-trace").rglob("*")
        if path.is_file()
    )
    check("structured_trace_nonempty", bool(trace_files))
    json_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                json.loads(line)
                json_lines += 1
    check("structured_trace_json", json_lines > 0, f" lines={json_lines}")


if __name__ == "__main__":
    main()
