#!/usr/bin/env python3
"""Launch Stage 1 and its single same-session timeout continuation."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import pipeline_contract


class Stage1RunnerError(RuntimeError):
    pass


PROMPTS = {
    "bare": "bare.md",
    "semantics": "with-semantics.md",
    "kit": "kit-bare.md",
    "kit-semantics": "kit-semantics.md",
}

STAGE1_RESULT_PATTERN = re.compile(
    r"RESULT: (KPROVE_PASSED|PARTIAL|BLOCKED) — (\S(?:.*\S)?)"
)


def parse_stage1_result(path: Path) -> str:
    path = pipeline_contract.require_regular_file(
        Path(path), "Stage 1 final message"
    )
    try:
        lines = path.read_text().splitlines()
    except OSError as error:
        raise Stage1RunnerError(
            f"cannot read Stage 1 final message: {path}"
        ) from error
    result_lines = [line for line in lines if line.startswith("RESULT:")]
    if len(result_lines) != 1:
        raise Stage1RunnerError(
            "Stage 1 final message must contain exactly one RESULT marker"
        )
    match = STAGE1_RESULT_PATTERN.fullmatch(result_lines[0])
    if match is None:
        raise Stage1RunnerError("Stage 1 RESULT marker is malformed")
    return match.group(1)


def _container_name(run_id: str, problem: str, invocation: str) -> str:
    readable = f"he-{run_id}-{problem}-{invocation}"
    suffix = sha256(readable.encode()).hexdigest()[:12]
    return f"{readable[:48]}-{suffix}"


def _inspect_container(docker: str, name: str) -> dict[str, Any]:
    result = subprocess.run(
        [docker, "inspect", name],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise Stage1RunnerError(
            f"cannot inspect completed container {name}: {result.stderr.strip()}"
        )
    try:
        documents = json.loads(result.stdout)
        document = documents[0]
        state = document["State"]
        return {
            "exit_code": int(state["ExitCode"]),
            "oom_killed": bool(state["OOMKilled"]),
            "image_id": str(document["Image"]),
        }
    except (ValueError, TypeError, KeyError, IndexError) as error:
        raise Stage1RunnerError(
            f"container inspection for {name} is malformed"
        ) from error


def _read_entry_metrics(path: Path) -> dict[str, Any]:
    document = pipeline_contract._read_regular_json(path, "entrypoint metrics")
    required = {
        "model_exit_code": int,
        "harness_exit_code": int,
        "final_exit_code": int,
        "duration_s": int,
        "timeout_marker": bool,
        "oom_killed": bool,
    }
    for key, expected in required.items():
        value = document.get(key)
        if not isinstance(value, expected):
            raise Stage1RunnerError(f"entrypoint metrics field {key} is malformed")
    if document["duration_s"] < 0:
        raise Stage1RunnerError("entrypoint duration is negative")
    return document


def _run_one(
    repo: Path,
    run_id: str,
    problem: str,
    invocation: pipeline_contract.Invocation,
    run_manifest: dict[str, Any],
    state: Path,
    *,
    docker: str,
) -> dict[str, Any]:
    condition = run_manifest["condition"]["name"]
    if invocation.kind == "initial":
        prompt = repo / "prompts" / PROMPTS[condition]
    elif invocation.kind == "oom-resume":
        prompt = repo / "prompts/oom-resume.md"
    elif invocation.kind == "terminal-resume":
        prompt = repo / "prompts/terminal-resume.md"
    elif invocation.kind == "infrastructure-retry":
        prompt = repo / "prompts/infrastructure-resume.md"
    else:
        prompt = repo / "prompts/timeout-resume.md"
    pipeline_contract.record_invocation_prompt(invocation.path, prompt)

    task = repo / f"runs/{run_id}/tasks/{problem}"
    workspace = task / "01-k-proof/workspace"
    codex_home = state / "codex-home"
    compose = repo / "docker/codex/docker-compose.yml"
    command = [docker, "compose", "-f", str(compose)]
    kit = bool(run_manifest["condition"]["kit"])
    if kit:
        command.extend(
            ["-f", str(repo / "docker/codex/docker-compose.kit.yml")]
        )
    container_name = _container_name(run_id, problem, invocation.name)
    command.extend(["run", "--name", container_name, "-T", "runner"])
    environment = os.environ.copy()
    environment.update(
        {
            "WORKSPACE_DIR": str(workspace),
            "INVOCATION_DIR": str(invocation.path),
            "CODEX_HOME_DIR": str(codex_home),
            "PROMPT_PATH": str(prompt),
            "INVOCATION_KIND": (
                "timeout-resume"
                if invocation.kind in {"oom-resume", "terminal-resume"}
                else invocation.kind
            ),
            "SESSION_ID": invocation.session_id or "",
            "MODEL": str(run_manifest["model"]),
            "EFFORT": str(run_manifest["effort"]),
            "TIMEOUT_S": str(invocation.allocation_s),
            "KIT": "1" if kit else "0",
        }
    )
    if invocation.kind == "oom-resume":
        environment["MEMORY_LIMIT"] = os.environ.get(
            "STAGE1_OOM_MEMORY", "16g"
        )
    elif invocation.kind == "terminal-resume":
        environment["MEMORY_LIMIT"] = os.environ.get(
            "STAGE1_TERMINAL_MEMORY", "8g"
        )
    run_result = subprocess.run(command, env=environment)
    try:
        try:
            inspection = _inspect_container(docker, container_name)
        except Stage1RunnerError:
            return pipeline_contract.finalize_invocation(
                repo,
                run_id,
                problem,
                "01-k-proof",
                invocation.name,
                exit_code=(
                    run_result.returncode
                    if run_result.returncode != 0
                    else 70
                ),
                duration_s=0,
                timeout_marker=False,
                oom_killed=False,
                image_id="UNAVAILABLE",
            )
    finally:
        subprocess.run(
            [docker, "rm", "-f", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    try:
        metrics = _read_entry_metrics(invocation.path / "metrics.json")
    except (pipeline_contract.PipelineContractError, Stage1RunnerError):
        return pipeline_contract.finalize_invocation(
            repo,
            run_id,
            problem,
            "01-k-proof",
            invocation.name,
            exit_code=inspection["exit_code"] or 70,
            duration_s=0,
            timeout_marker=False,
            oom_killed=inspection["oom_killed"],
            image_id=inspection["image_id"],
        )
    consistent = (
        inspection["exit_code"] == run_result.returncode
        and metrics["final_exit_code"] == inspection["exit_code"]
    )
    exit_code = inspection["exit_code"] if consistent else 70
    if (
        consistent
        and exit_code == 0
        and not metrics["timeout_marker"]
        and not (inspection["oom_killed"] or metrics["oom_killed"])
    ):
        try:
            result_marker = parse_stage1_result(
                invocation.path / "codex-last.txt"
            )
        except Stage1RunnerError:
            exit_code = 1
        else:
            if result_marker != "KPROVE_PASSED":
                exit_code = 1
    return pipeline_contract.finalize_invocation(
        repo,
        run_id,
        problem,
        "01-k-proof",
        invocation.name,
        exit_code=exit_code,
        duration_s=metrics["duration_s"],
        timeout_marker=metrics["timeout_marker"] if consistent else False,
        oom_killed=inspection["oom_killed"] or metrics["oom_killed"],
        image_id=inspection["image_id"],
    )


def inspect_stage1(repo: Path, run_id: str, problem: str) -> dict[str, Any]:
    task, state, run_manifest = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    condition = run_manifest.get("condition", {})
    name = condition.get("name")
    if name not in PROMPTS:
        raise Stage1RunnerError("run condition is unsupported")
    return {
        "run_id": run_id,
        "problem": problem,
        "config": run_manifest["config"],
        "model": run_manifest["model"],
        "effort": run_manifest["effort"],
        "condition": name,
        "kit": int(bool(condition.get("kit"))),
        "workspace": str(task / "01-k-proof/workspace"),
        "state": str(state),
        "prompt": PROMPTS[name],
        "compose_files": [
            "docker-compose.yml",
            *(["docker-compose.kit.yml"] if condition.get("kit") else []),
        ],
    }


def run_stage1(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    docker: str = "docker",
    infrastructure_retry: bool = False,
    oom_resume: bool = False,
    terminal_resume: bool = False,
) -> dict[str, Any]:
    repo = pipeline_contract.require_real_directory(Path(repo), "repository")
    _task, state, run_manifest = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    if sum((infrastructure_retry, oom_resume, terminal_resume)) > 1:
        raise Stage1RunnerError("retry modes are mutually exclusive")
    if infrastructure_retry:
        invocation = pipeline_contract.prepare_infrastructure_retry(
            repo, run_id, problem, "01-k-proof"
        )
        return _run_one(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            docker=docker,
        )
    if oom_resume:
        invocation = pipeline_contract.prepare_oom_resume(
            repo, run_id, problem
        )
        return _run_one(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            docker=docker,
        )
    if terminal_resume:
        invocation = pipeline_contract.prepare_terminal_resume(
            repo, run_id, problem
        )
        return _run_one(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            docker=docker,
        )
    while True:
        invocation = pipeline_contract.prepare_invocation(
            repo, run_id, problem, "01-k-proof"
        )
        result = _run_one(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            docker=docker,
        )
        if (
            result["status"] == "TIMEOUT"
            and result.get("resumable") is True
            and invocation.name == "001-initial"
        ):
            continue
        return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--print-config", action="store_true")
    retries = parser.add_mutually_exclusive_group()
    retries.add_argument("--infrastructure-retry", action="store_true")
    retries.add_argument("--oom-resume", action="store_true")
    retries.add_argument("--terminal-resume", action="store_true")
    parser.add_argument("run_id")
    parser.add_argument("problem")
    arguments = parser.parse_args(argv)
    try:
        if arguments.print_config:
            document = inspect_stage1(
                arguments.repo, arguments.run_id, arguments.problem
            )
            for key in (
                "run_id",
                "problem",
                "config",
                "model",
                "effort",
                "condition",
                "kit",
                "workspace",
                "state",
                "prompt",
            ):
                print(f"{key}={document[key]}")
            for compose_file in document["compose_files"]:
                print(f"compose_file={compose_file}")
            return 0
        result = run_stage1(
            arguments.repo,
            arguments.run_id,
            arguments.problem,
            infrastructure_retry=arguments.infrastructure_retry,
            oom_resume=arguments.oom_resume,
            terminal_resume=arguments.terminal_resume,
        )
    except (pipeline_contract.PipelineContractError, Stage1RunnerError) as error:
        print(f"Stage 1 failed: {error}", file=sys.stderr)
        return 2
    return 0 if result["status"] == "SUCCEEDED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
