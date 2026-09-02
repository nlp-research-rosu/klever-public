#!/usr/bin/env python3
"""Independent mounted-input checks for the pipeline-v3 audit record."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_not_symlink(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def report_check(name: str, actual: object, expected: object) -> bool:
    ok = actual == expected
    print(f"{name}: {'OK' if ok else 'MISMATCH'}")
    print(f"  actual={actual!r}")
    print(f"  expected={expected!r}")
    return ok


def main() -> int:
    record = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = record["hashes"]
    paths = {key: Path(value) for key, value in record["container_paths"].items()}
    ok = True

    print("record_layout", record["record_layout"])
    print("semantics_mode", record["semantics_mode"])
    ok &= report_check("campaign-block", lock, record["audit_campaign"])
    ok &= report_check(
        "campaign-lock-sha256", sha256(LOCK), hashes["audit_campaign_lock_sha256"]
    )

    required = {
        **paths,
        "generation_runtime_metrics": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage": Path("/generation-evidence/usage.json"),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
    }
    for name, path in required.items():
        if name in {"candidate", "generation_root", "generation_trace"}:
            present = path.is_dir() and not path.is_symlink()
        else:
            present = regular_not_symlink(path)
        print(f"required-{name}: {'OK' if present else 'BAD'} {path}")
        ok &= present

    direct_hashes = {
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path(
            "/generation-evidence/runtime-metrics.json"
        ): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path(
            "/generation-evidence/codex-last.txt"
        ): "generation_codex_last_sha256",
        Path(
            "/generation-evidence/codex-output.log"
        ): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, field in direct_hashes.items():
        actual = sha256(path)
        ok &= report_check(f"sha256-{path}", actual, hashes[field])

    ok &= report_check(
        "prompt-byte-identity",
        sha256(Path("/candidate/prompt.py")),
        sha256(Path("/reference/prompt.py")),
    )
    ok &= report_check(
        "translator-byte-identity",
        sha256(Path("/candidate/py2mpy.py")),
        sha256(Path("/reference/py2mpy.py")),
    )
    task_manifest = json.loads(Path("/task.json").read_text())
    embedded_manifest = record["manifest"]
    # The launcher enriches the embedded view with the run-level config; the
    # task file itself is committed by task_manifest_sha256/manifest_sha256.
    for key, value in task_manifest.items():
        ok &= report_check(
            f"task-manifest-field-{key}", value, embedded_manifest.get(key)
        )
    print(
        "embedded-manifest-extra-fields",
        sorted(set(embedded_manifest) - set(task_manifest)),
    )
    ok &= report_check(
        "manifest-sha256-alias",
        hashes["manifest_sha256"],
        hashes["task_manifest_sha256"],
    )
    ok &= report_check(
        "reference-semantics-absent",
        os.path.lexists("/reference/reference-semantics"),
        False,
    )

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for rel, expected in result["outputs"]["evidence"].items():
        actual = sha256(Path("/generation-evidence") / rel)
        ok &= report_check(f"result-evidence-{rel}", actual, expected)
    ok &= report_check(
        "invocation-evidence-map",
        invocation["outputs"]["evidence"],
        result["outputs"]["evidence"],
    )

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    print("trace-files", len(trace_files))
    for path in trace_files:
        rel = path.relative_to("/generation-evidence").as_posix()
        expected = result["outputs"]["evidence"].get(rel)
        actual = sha256(path)
        ok &= report_check(f"trace-leaf-{rel}", actual, expected)
        valid_lines = 0
        with path.open() as stream:
            for line_no, line in enumerate(stream, 1):
                json.loads(line)
                valid_lines = line_no
        print(f"trace-json-lines-{rel}: {valid_lines}")

    for root in (Path("/candidate"), Path("/generation-evidence"), Path("/reference")):
        symlinks = sorted(path.as_posix() for path in root.rglob("*") if path.is_symlink())
        ok &= report_check(f"symlinks-{root}", symlinks, [])

    # A complete leaf manifest independently commits to every mounted candidate
    # artifact even though the launcher's private tree-hash framing is not
    # specified in audit-input.json.
    candidate_files = sorted(
        path for path in Path("/candidate").rglob("*") if path.is_file()
    )
    print("candidate-leaf-manifest")
    for path in candidate_files:
        print(sha256(path), path.relative_to("/candidate").as_posix())

    # Force a complete read of the large untrusted records and summarize them.
    output_log = Path("/generation-evidence/codex-output.log").read_bytes()
    print("codex-output-bytes", len(output_log))
    print("codex-output-lines", output_log.count(b"\n"))
    print("codex-output-kprove-occurrences", output_log.count(b"kprove"))
    print("codex-output-top-occurrences", output_log.count(b"#Top"))

    print("OVERALL", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
