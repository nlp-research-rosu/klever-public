#!/usr/bin/env python3
"""Bounded summary of all required pipeline-v3 generation records."""

from __future__ import annotations

import json
from pathlib import Path


def load(path: str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    audit = load("/audit-input.json")
    run = load("/run.json")
    task = load("/task.json")
    result = load("/generation-result.json")
    invocation = load("/generation-evidence/invocation.json")
    metrics = load("/generation-evidence/metrics.json")
    runtime = load("/generation-evidence/runtime-metrics.json")
    usage = load("/generation-evidence/usage.json")

    assert isinstance(audit, dict)
    assert isinstance(run, dict)
    assert isinstance(task, dict)
    assert isinstance(result, dict)
    assert isinstance(invocation, dict)
    assert isinstance(metrics, dict)
    assert isinstance(runtime, dict)
    assert isinstance(usage, dict)

    summary = {
        "audit_input": {
            "problem_id": audit["problem_id"],
            "condition": audit["condition"],
            "record_layout": audit["record_layout"],
            "semantics_mode": audit["semantics_mode"],
            "mount_reference_semantics": audit["mount_reference_semantics"],
            "container_paths": audit["container_paths"],
            "integrity_claims": audit["integrity"],
        },
        "run": {
            "schema_version": run["schema_version"],
            "run_id": run["run_id"],
            "config": run["config"],
            "condition": run["condition"],
            "runtime": run["runtime"],
            "kit": run["kit"],
        },
        "task": task,
        "generation_result": result,
        "invocation": invocation,
        "metrics": metrics,
        "runtime_metrics": runtime,
        "usage": usage,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
