#!/usr/bin/env python3
"""Inspect and orchestrate the six-stage resumable proof pipeline."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import pipeline_contract


STAGES = pipeline_contract.STAGE_NAMES
STAGE_SCRIPTS = {
    "01-k-proof": "docker/codex/run_task.sh",
    "02-k-audit": "docker/audit/run_task.sh",
    "03-lemma-discovery": "docker/codex/resume_lemma_discovery_task.sh",
    "04-klean-generation": "docker/klean/generate_task.sh",
    "05-lean-proof": "docker/codex/resume_lean_task.sh",
    "06-lean-audit": "docker/klean-audit/run_task.sh",
}
_STAGE_ALIASES = {
    "1": "01-k-proof",
    "2": "02-k-audit",
    "3": "03-lemma-discovery",
    "4": "04-klean-generation",
    "5": "05-lean-proof",
    "6": "06-lean-audit",
    **{stage: stage for stage in STAGES},
}


class PipelineOrchestrationError(RuntimeError):
    pass


def _load_run(repo: Path, run_id: str) -> tuple[Path, dict[str, Any]]:
    repo = pipeline_contract.require_real_directory(repo, "repository")
    run_id = pipeline_contract.validate_safe_component(run_id, "run ID")
    runs = pipeline_contract.require_real_directory(repo / "runs", "runs root")
    run = pipeline_contract._require_direct_directory(runs, run_id, "run")
    manifest = pipeline_contract._read_regular_json(
        run / "run.json", "run manifest"
    )
    if manifest.get("run_id") != run_id:
        raise PipelineOrchestrationError("run manifest ID does not match")
    tasks = manifest.get("tasks")
    if (
        not isinstance(tasks, list)
        or not tasks
        or any(not isinstance(problem, str) for problem in tasks)
    ):
        raise PipelineOrchestrationError("run task list is malformed")
    for problem in tasks:
        pipeline_contract.validate_safe_component(problem, "problem ID")
    return run, manifest


def command_for_stage(
    repo: Path, run_id: str, problem: str, stage: str
) -> list[str]:
    try:
        stage = _STAGE_ALIASES[stage]
    except KeyError as error:
        raise PipelineOrchestrationError(f"unknown stage: {stage}") from error
    script = pipeline_contract.require_regular_file(
        repo / STAGE_SCRIPTS[stage], f"{stage} launcher"
    )
    return [str(script), run_id, problem]


def stage_from_command(command: list[str]) -> str:
    executable = Path(command[0])
    suffix = executable.as_posix()
    for stage, script in STAGE_SCRIPTS.items():
        if suffix.endswith(script):
            return stage
    raise PipelineOrchestrationError(
        f"command does not name a pipeline stage: {command!r}"
    )


def _result_status(task: Path, stage: str) -> str | None:
    path = task / stage / "result.json"
    if not path.exists() and not path.is_symlink():
        return None
    document = pipeline_contract._read_regular_json(
        path, f"{stage} result"
    )
    status = document.get("status")
    if status not in {"SUCCEEDED", "TIMEOUT", "OOM", "FAILED"}:
        raise PipelineOrchestrationError(f"{stage} result status is invalid")
    return str(status)


def _selected_status(task: Path, stage: str) -> str | None:
    root = task / stage
    path = root / "selected.json"
    if not path.exists() and not path.is_symlink():
        return None
    selected = pipeline_contract._read_regular_json(
        path, f"{stage} selection"
    )
    relative = selected.get("relative_path")
    parts = Path(relative).parts if isinstance(relative, str) else ()
    container = pipeline_contract._SELECTION_STAGES[stage][0]
    if len(parts) != 2 or parts[0] != container:
        raise PipelineOrchestrationError(f"{stage} selection path is malformed")
    candidate = pipeline_contract._require_direct_directory(
        root / container, parts[1], f"{stage} selected output"
    )
    status = pipeline_contract._selection_status(stage, candidate)
    if pipeline_contract.sha256_tree(candidate) != selected.get(
        "artifact_sha256"
    ):
        raise PipelineOrchestrationError(
            f"{stage} selected output changed after selection"
        )
    if selected.get("status") != status:
        raise PipelineOrchestrationError(
            f"{stage} selected status disagrees with its output"
        )
    return status


def inspect_problem(
    repo: Path, run_id: str, problem: str
) -> dict[str, Any]:
    try:
        task, _state, _run = pipeline_contract._resolve_task_state(
            repo, run_id, problem
        )
        pipeline_block = pipeline_contract.task_pipeline_block(task)
        if pipeline_block is not None:
            return {
                "state": (
                    "BLOCKED_SESSION_STATE"
                    if pipeline_block == "SESSION_STATE_UNRECOVERABLE"
                    else "BLOCKED_INPUT_PROVENANCE"
                ),
                "next_stage": None,
            }
        k_status = _result_status(task, "01-k-proof")
        if k_status is None:
            return {"state": "PENDING_K_PROOF", "next_stage": "01-k-proof"}
        if k_status != "SUCCEEDED":
            return {
                "state": f"K_PROOF_{k_status}",
                "next_stage": None,
            }

        audit_status = _selected_status(task, "02-k-audit")
        if audit_status is None:
            return {"state": "PENDING_K_AUDIT", "next_stage": "02-k-audit"}
        if audit_status == "AUDIT_ERROR":
            return {
                "state": "K_AUDIT_ERROR_RETRY",
                "next_stage": "02-k-audit",
            }
        if audit_status == "FAIL":
            return {"state": "K_AUDIT_FAIL", "next_stage": None}

        discovery_status = _result_status(task, "03-lemma-discovery")
        if discovery_status is None:
            return {
                "state": "PENDING_LEMMA_DISCOVERY",
                "next_stage": "03-lemma-discovery",
            }
        if discovery_status != "SUCCEEDED":
            return {
                "state": f"LEMMA_DISCOVERY_{discovery_status}",
                "next_stage": None,
            }

        klean_status = _selected_status(task, "04-klean-generation")
        if klean_status is None:
            return {
                "state": "PENDING_KLEAN_GENERATION",
                "next_stage": "04-klean-generation",
            }
        if klean_status == "KLEAN_PREFLIGHT_ERROR":
            return {"state": "KLEAN_PREFLIGHT_ERROR", "next_stage": None}

        if klean_status != "KLEAN_NO_OBLIGATIONS":
            lean_status = _result_status(task, "05-lean-proof")
            if lean_status is None:
                return {
                    "state": "PENDING_LEAN_PROOF",
                    "next_stage": "05-lean-proof",
                }
            if lean_status != "SUCCEEDED":
                return {
                    "state": f"LEAN_PROOF_{lean_status}",
                    "next_stage": None,
                }

        lean_audit_status = _selected_status(task, "06-lean-audit")
        if lean_audit_status is None:
            return {
                "state": "PENDING_LEAN_AUDIT",
                "next_stage": "06-lean-audit",
            }
        if lean_audit_status == "AUDIT_ERROR":
            return {
                "state": "LEAN_AUDIT_ERROR_RETRY",
                "next_stage": "06-lean-audit",
            }
        if lean_audit_status == "FAIL":
            return {"state": "LEAN_AUDIT_FAIL", "next_stage": None}
        return {
            "state": "COMPLETE_LEGIT",
            "next_stage": None,
            "lean_audit_verdict": lean_audit_status,
        }
    except pipeline_contract.PipelineContractError as error:
        raise PipelineOrchestrationError(str(error)) from error


def _default_execute(command: list[str]) -> int:
    return subprocess.run(command).returncode


def run_problem(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    execute: Callable[[list[str]], int] = _default_execute,
) -> dict[str, Any]:
    previous_retry: str | None = None
    status = inspect_problem(repo, run_id, problem)
    while True:
        stage = status.get("next_stage")
        if not isinstance(stage, str):
            return status
        if status["state"].endswith("_ERROR_RETRY"):
            if previous_retry == status["state"]:
                return {
                    "state": f"REPEATED_{status['state']}",
                    "next_stage": None,
                }
            previous_retry = str(status["state"])
        command = command_for_stage(repo, run_id, problem, stage)
        return_code = execute(command)
        updated = inspect_problem(repo, run_id, problem)
        if return_code != 0 and updated == status:
            return {
                "state": "STAGE_LAUNCH_ERROR",
                "failed_stage": stage,
                "exit_code": return_code,
                "next_stage": None,
            }
        status = updated


def run_batch(
    repo: Path,
    run_id: str,
    *,
    jobs: int,
    execute: Callable[[list[str]], int] = _default_execute,
) -> dict[str, dict[str, Any]]:
    _run, manifest = _load_run(repo, run_id)
    if not isinstance(jobs, int) or jobs < 1:
        raise PipelineOrchestrationError("jobs must be a positive integer")
    tasks = list(manifest["tasks"])
    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = {
            executor.submit(
                run_problem,
                repo,
                run_id,
                problem,
                execute=execute,
            ): problem
            for problem in tasks
        }
        for future in as_completed(futures):
            problem = futures[future]
            results[problem] = future.result()
    return {problem: results[problem] for problem in tasks}


def run_status(repo: Path, run_id: str) -> dict[str, Any]:
    _run, manifest = _load_run(repo, run_id)
    tasks = {
        problem: inspect_problem(repo, run_id, problem)
        for problem in manifest["tasks"]
    }
    counts = Counter(item["state"] for item in tasks.values())
    return {
        "run_id": run_id,
        "tasks": tasks,
        "counts": dict(sorted(counts.items())),
    }


def dry_run(repo: Path, run_id: str) -> list[dict[str, Any]]:
    _run, manifest = _load_run(repo, run_id)
    result: list[dict[str, Any]] = []
    for problem in manifest["tasks"]:
        status = inspect_problem(repo, run_id, problem)
        stage = status.get("next_stage")
        result.append(
            {
                "problem": problem,
                **status,
                "command": (
                    command_for_stage(repo, run_id, problem, stage)
                    if isinstance(stage, str)
                    else None
                ),
            }
        )
    return result


def run_one_stage(
    repo: Path,
    run_id: str,
    problem: str,
    stage: str,
    *,
    execute: Callable[[list[str]], int] = _default_execute,
) -> int:
    try:
        stage = _STAGE_ALIASES[stage]
    except KeyError as error:
        raise PipelineOrchestrationError(f"unknown stage: {stage}") from error
    status = inspect_problem(repo, run_id, problem)
    if status.get("next_stage") != stage:
        manual_repair = (
            stage == "04-klean-generation"
            and status.get("state") == "KLEAN_PREFLIGHT_ERROR"
        )
        if not manual_repair:
            raise PipelineOrchestrationError(
                f"{problem} is not eligible for {stage}: {status['state']}"
            )
    return execute(command_for_stage(repo, run_id, problem, stage))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    subparsers = parser.add_subparsers(dest="command", required=True)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("run_id")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("run_id")
    run_parser.add_argument("--jobs", type=int, default=1)
    dry_parser = subparsers.add_parser("dry-run")
    dry_parser.add_argument("run_id")
    stage_parser = subparsers.add_parser("stage")
    stage_parser.add_argument("run_id")
    stage_parser.add_argument("problem")
    stage_parser.add_argument("stage")
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "status":
            document: object = run_status(arguments.repo, arguments.run_id)
        elif arguments.command == "dry-run":
            document = dry_run(arguments.repo, arguments.run_id)
        elif arguments.command == "run":
            tasks = run_batch(
                arguments.repo,
                arguments.run_id,
                jobs=arguments.jobs,
            )
            document = {
                "run_id": arguments.run_id,
                "tasks": tasks,
                "counts": dict(
                    sorted(Counter(item["state"] for item in tasks.values()).items())
                ),
            }
        else:
            return run_one_stage(
                arguments.repo,
                arguments.run_id,
                arguments.problem,
                arguments.stage,
            )
        print(json.dumps(document, indent=2, sort_keys=True))
    except (
        PipelineOrchestrationError,
        pipeline_contract.PipelineContractError,
    ) as error:
        print(f"pipeline error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
