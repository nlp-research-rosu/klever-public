#!/usr/bin/env python3
"""Transactionally preserve schema-v2 evidence in the six-stage layout."""

from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import uuid
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import legacy_migration, pipeline_contract


class SixStageMigrationError(RuntimeError):
    """Raised when a schema-v2 run cannot be migrated safely."""


SCHEMA_FROM = 2
SCHEMA_TO = pipeline_contract.SCHEMA_VERSION
MOVES = {
    "03-klean-generation": "04-klean-generation/legacy-v2",
    "04-lean-proof": "05-lean-proof/legacy-v2",
    "05-lean-audit": "06-lean-audit/legacy-v2",
}
CREATES = [
    "03-lemma-discovery/workspace",
    "03-lemma-discovery/invocations",
    "04-klean-generation/generations",
    "05-lean-proof/workspace",
    "05-lean-proof/invocations",
    "06-lean-audit/executions",
]
_LEGACY_STAGES = tuple(MOVES)
_ACTIVE_STAGES = {"01-k-proof", "02-k-audit"}
_RENAME_EXCHANGE = 2
_AT_FDCWD = -100
_JOURNAL_NAME = ".six-stage-migration-transaction.json"
_JOURNAL_SCHEMA_VERSION = 1
_JOURNAL_PHASES = {
    "STAGED",
    "PUBLISHING",
    "VALIDATED",
}
_PROCESS_BASENAMES = {
    "pipeline": {"run_pipeline.py"},
    "audit": {
        "audit_contract.py",
        "klean_audit_contract.py",
        "klean_final_gate.py",
    },
    "klean": {
        "klean.py",
        "klean_export.py",
        "klean_preflight.py",
        "stage4_runner.py",
    },
    "codex": {
        "codex",
        "resume_lemma_discovery_task.sh",
        "resume_lean_task.sh",
        "stage1_runner.py",
        "stage3_runner.py",
        "stage5_runner.py",
    },
}
_SESSION_BLOCK = "SESSION_STATE_UNRECOVERABLE"
_SESSION_REASONS = {
    "SESSION_STATE_MISSING",
    "SESSION_STATE_MALFORMED",
    "SESSION_ID_MISMATCH",
}


def _error(message: str, path: Path | None = None) -> SixStageMigrationError:
    suffix = f": {path}" if path is not None else ""
    return SixStageMigrationError(f"{message}{suffix}")


def _validate_component(value: object, label: str) -> str:
    try:
        return pipeline_contract.validate_safe_component(value, label)
    except pipeline_contract.PipelineContractError as error:
        raise SixStageMigrationError(str(error)) from error


def _path_exists(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    except OSError as error:
        raise _error("cannot inspect migration path", path) from error
    return True


def _remove_owned_path(path: Path) -> None:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return
    except OSError as error:
        raise _error("cannot inspect owned migration path", path) from error
    try:
        if stat.S_ISDIR(mode):
            shutil.rmtree(path)
        else:
            path.unlink()
    except OSError as error:
        raise _error("cannot remove owned migration path", path) from error


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        document = pipeline_contract._read_regular_json(path, label)
    except pipeline_contract.PipelineContractError as error:
        raise _error(str(error), path) from error
    return document


def _write_json(path: Path, document: dict[str, Any]) -> None:
    try:
        pipeline_contract.write_json_atomic(path, document)
    except (OSError, pipeline_contract.PipelineContractError) as error:
        raise _error("cannot write migrated manifest", path) from error


def _require_directory(path: Path, label: str) -> Path:
    try:
        return pipeline_contract.require_real_directory(path, label)
    except pipeline_contract.PipelineContractError as error:
        raise _error(str(error), path) from error


def _tree_hash(path: Path, label: str) -> str:
    try:
        return pipeline_contract.sha256_tree(path)
    except pipeline_contract.PipelineContractError as error:
        raise _error(f"cannot hash {label}", path) from error


def _task_ids(run: Path, manifest: Mapping[str, Any]) -> list[str]:
    values = manifest.get("tasks")
    if (
        not isinstance(values, list)
        or not values
        or any(not isinstance(value, str) for value in values)
    ):
        raise _error("schema-v2 run task list is malformed", run / "run.json")
    task_ids: list[str] = []
    seen: set[str] = set()
    for value in values:
        try:
            problem = pipeline_contract.validate_safe_component(
                value,
                "problem ID",
            )
        except pipeline_contract.PipelineContractError as error:
            raise _error(str(error), run / "run.json") from error
        if problem in seen:
            raise _error("schema-v2 run task list contains a duplicate")
        seen.add(problem)
        task_ids.append(problem)
    tasks = _require_directory(run / "tasks", "schema-v2 tasks root")
    try:
        actual = sorted(
            entry.name
            for entry in tasks.iterdir()
            if entry.is_dir() and not entry.is_symlink()
        )
    except OSError as error:
        raise _error("cannot scan schema-v2 tasks", tasks) from error
    if actual != sorted(task_ids):
        raise _error("schema-v2 task directories do not match run manifest")
    return task_ids


def _inspect_task(task: Path, problem: str) -> dict[str, Any]:
    _require_directory(task, "schema-v2 task")
    manifest = _read_json(task / "task.json", "schema-v2 task manifest")
    if manifest.get("schema_version") != SCHEMA_FROM:
        raise _error("task manifest schema version is not 2", task / "task.json")
    if manifest.get("problem_id") != problem:
        raise _error("task manifest problem ID does not match", task / "task.json")
    legacy_trees: dict[str, str] = {}
    for stage in ("01-k-proof", "02-k-audit", *_LEGACY_STAGES):
        legacy_trees[stage] = _tree_hash(task / stage, f"schema-v2 {stage}")
    return {
        "problem_id": problem,
        "source_sha256": _tree_hash(task, "schema-v2 task"),
        "legacy_trees": legacy_trees,
    }


def _optional_regular_bytes(path: Path) -> bytes | None:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return None
    except OSError:
        return None
    if not stat.S_ISREG(mode):
        return None
    try:
        return path.read_bytes()
    except OSError:
        return None


def _canonical_uuid(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = str(uuid.UUID(value))
    except (AttributeError, TypeError, ValueError):
        return None
    return parsed if parsed == value else None


def _json_document(data: bytes | None) -> dict[str, Any] | None:
    if data is None:
        return None
    try:
        document = json.loads(data)
    except (UnicodeError, ValueError):
        return None
    return document if isinstance(document, dict) else None


def _rollout_proof(root: Path) -> tuple[set[str], list[dict[str, str]]] | None:
    try:
        mode = root.lstat().st_mode
    except OSError:
        return None
    if not stat.S_ISDIR(mode):
        return None
    try:
        paths = sorted(root.rglob("*.jsonl"))
    except OSError:
        return None
    if not paths:
        return None
    session_ids: set[str] = set()
    evidence: list[dict[str, str]] = []
    for path in paths:
        data = _optional_regular_bytes(path)
        if data is None:
            return None
        try:
            lines = data.decode().splitlines()
        except UnicodeError:
            return None
        for line in lines:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except ValueError:
                return None
            if not isinstance(event, dict):
                return None
            if event.get("type") != "session_meta":
                continue
            payload = event.get("payload")
            session_id = _canonical_uuid(
                payload.get("id")
                if isinstance(payload, dict)
                else None
            )
            if session_id is None:
                return None
            alternate = (
                payload.get("session_id")
                if isinstance(payload, dict)
                else None
            )
            if alternate is not None and alternate != session_id:
                return None
            session_ids.add(session_id)
        evidence.append(
            {
                "relative_path": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    if not session_ids:
        return None
    return session_ids, evidence


def _unrecoverable_session(
    reason: str,
    *,
    session_bytes: bytes | None,
) -> dict[str, Any]:
    return {
        "status": "UNRECOVERABLE",
        "reason": reason,
        "legacy_session_present": session_bytes is not None,
        "legacy_session_sha256": (
            hashlib.sha256(session_bytes).hexdigest()
            if session_bytes is not None
            else None
        ),
    }


def _inspect_session_provenance(
    task: Path,
    task_state: Path,
) -> dict[str, Any]:
    session_path = task_state / "session.json"
    session_bytes = _optional_regular_bytes(session_path)
    if session_bytes is None:
        return _unrecoverable_session(
            "SESSION_STATE_MISSING",
            session_bytes=None,
        )
    session = _json_document(session_bytes)
    if session is None:
        return _unrecoverable_session(
            "SESSION_STATE_MALFORMED",
            session_bytes=session_bytes,
        )
    session_id = _canonical_uuid(session.get("session_id"))
    if (
        session_id is None
        or session.get("codex_home_relative") != "codex-home"
        or not isinstance(session.get("codex_home_device"), int)
        or isinstance(session.get("codex_home_device"), bool)
        or not isinstance(session.get("codex_home_inode"), int)
        or isinstance(session.get("codex_home_inode"), bool)
        or not isinstance(session.get("source"), str)
    ):
        return _unrecoverable_session(
            "SESSION_STATE_MALFORMED",
            session_bytes=session_bytes,
        )
    home = task_state / "codex-home"
    try:
        home_stat = home.lstat()
    except OSError:
        return _unrecoverable_session(
            "SESSION_STATE_MISSING",
            session_bytes=session_bytes,
        )
    if not stat.S_ISDIR(home_stat.st_mode):
        return _unrecoverable_session(
            "SESSION_STATE_MISSING",
            session_bytes=session_bytes,
        )
    persistent = _rollout_proof(home / "sessions")
    if persistent is None:
        return _unrecoverable_session(
            "SESSION_ID_MISMATCH",
            session_bytes=session_bytes,
        )
    persistent_ids, persistent_evidence = persistent

    result_bytes = _optional_regular_bytes(
        task / "01-k-proof/result.json"
    )
    result = _json_document(result_bytes)
    invocation_name = (
        result.get("invocation")
        if isinstance(result, dict)
        else None
    )
    if (
        result_bytes is None
        or result is None
        or result.get("status") != "SUCCEEDED"
        or result.get("session_id") != session_id
        or not isinstance(invocation_name, str)
        or re.fullmatch(
            r"[0-9]{3}-(?:initial|timeout-resume)",
            invocation_name,
        )
        is None
        or session.get("source") != "01-k-proof/001-initial"
    ):
        return _unrecoverable_session(
            "SESSION_ID_MISMATCH",
            session_bytes=session_bytes,
        )
    invocation = task / "01-k-proof/invocations" / invocation_name
    invocation_bytes = _optional_regular_bytes(
        invocation / "invocation.json"
    )
    invocation_document = _json_document(invocation_bytes)
    stage1_rollouts = _rollout_proof(invocation / "codex-trace")
    if (
        invocation_bytes is None
        or invocation_document is None
        or invocation_document.get("stage") != "01-k-proof"
        or invocation_document.get("name") != invocation_name
        or invocation_document.get("status") != "SUCCEEDED"
        or invocation_document.get("session_id") != session_id
        or stage1_rollouts is None
    ):
        return _unrecoverable_session(
            "SESSION_ID_MISMATCH",
            session_bytes=session_bytes,
        )
    stage1_ids, stage1_evidence = stage1_rollouts
    persistent_hashes = sorted(
        item["sha256"] for item in persistent_evidence
    )
    stage1_hashes = sorted(item["sha256"] for item in stage1_evidence)
    if (
        persistent_ids != {session_id}
        or stage1_ids != {session_id}
        or persistent_hashes != stage1_hashes
        or home_stat.st_ino != session["codex_home_inode"]
    ):
        return _unrecoverable_session(
            "SESSION_ID_MISMATCH",
            session_bytes=session_bytes,
        )
    return {
        "status": "RECOVERABLE",
        "reason": None,
        "session_id": session_id,
        "legacy_session_present": True,
        "legacy_session_sha256": hashlib.sha256(
            session_bytes
        ).hexdigest(),
        "persistent_rollouts": persistent_evidence,
        "stage1_result_sha256": hashlib.sha256(
            result_bytes
        ).hexdigest(),
        "stage1_invocation_sha256": hashlib.sha256(
            invocation_bytes
        ).hexdigest(),
        "stage1_rollouts": stage1_evidence,
    }


def _inspect_run(repo: Path, run_id: str) -> dict[str, Any]:
    run = _require_directory(repo / "runs" / run_id, "schema-v2 run")
    manifest = _read_json(run / "run.json", "schema-v2 run manifest")
    if manifest.get("schema_version") != SCHEMA_FROM:
        raise _error("run manifest schema version is not 2", run / "run.json")
    if manifest.get("run_id") != run_id:
        raise _error("run manifest ID does not match run directory", run / "run.json")
    task_ids = _task_ids(run, manifest)
    state = _require_directory(
        repo / "runner-state" / run_id,
        "schema-v2 runner state",
    )
    tasks: list[dict[str, Any]] = []
    for problem in task_ids:
        task_state = _require_directory(
            state / problem,
            "schema-v2 task runner state",
        )
        pipeline_contract.require_regular_file(
            task_state / "stage-ledger.jsonl",
            "schema-v2 stage ledger",
        )
        task = _inspect_task(run / "tasks" / problem, problem)
        task["session_provenance"] = _inspect_session_provenance(
            run / "tasks" / problem,
            task_state,
        )
        tasks.append(task)
    return {
        "run_id": run_id,
        "source": f"runs/{run_id}",
        "source_sha256": _tree_hash(run, "schema-v2 run"),
        "runner_state": f"runner-state/{run_id}",
        "runner_state_sha256": _tree_hash(state, "schema-v2 runner state"),
        "tasks": tasks,
    }


def _candidate_processes() -> tuple[tuple[int, tuple[str, ...]], ...]:
    """Return process command lines; kept as a narrow inspection seam."""

    processes: list[tuple[int, tuple[str, ...]]] = []
    current_pid = os.getpid()
    try:
        entries = tuple(Path("/proc").iterdir())
    except OSError as error:
        raise _error(f"cannot scan active processes: {error}") from error
    for entry in entries:
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        if pid == current_pid:
            continue
        try:
            raw = (entry / "cmdline").read_bytes()
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
        except OSError as error:
            raise _error(
                "cannot inspect active process",
                entry / "cmdline",
            ) from error
        arguments = tuple(
            item.decode("utf-8", errors="surrogateescape")
            for item in raw.split(b"\0")
            if item
        )
        if arguments:
            processes.append((pid, arguments))
    return tuple(processes)


def _process_kind(
    arguments: Sequence[str],
    run_ids: Sequence[str],
) -> str | None:
    names = {Path(argument).name.lower() for argument in arguments}
    for kind in ("pipeline", "audit", "klean", "codex"):
        if names & _PROCESS_BASENAMES[kind]:
            return kind
    marker_arguments = [
        argument
        for argument in arguments
        if argument not in run_ids
    ]
    markers = "\0".join(marker_arguments).lower()
    if (
        "/audit/" in markers
        or "/klean-audit/" in markers
        or "klean-audit" in markers
    ):
        return "audit"
    if "/klean/" in markers:
        return "klean"
    if "/codex/" in markers:
        return "codex"
    return None


def _argument_names_run(argument: str, run_id: str) -> bool:
    if argument == run_id:
        return True
    try:
        return run_id in Path(argument).parts
    except (TypeError, ValueError):
        return False


def _active_process_blockers(run_ids: Sequence[str]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    for pid, arguments in _candidate_processes():
        named = [
            run_id
            for run_id in run_ids
            if any(
                _argument_names_run(argument, run_id)
                for argument in arguments
            )
        ]
        if not named:
            continue
        kind = _process_kind(arguments, run_ids)
        if kind is None:
            continue
        blockers.append(
            {
                "kind": "active_process",
                "process_kind": kind,
                "pid": pid,
                "run_ids": named,
                "cmdline": list(arguments),
            }
        )
    return blockers


def _refuse_active_processes(run_ids: Sequence[str]) -> None:
    blockers = _active_process_blockers(run_ids)
    if not blockers:
        return
    first = blockers[0]
    raise SixStageMigrationError(
        "active "
        f"{first['process_kind']} process names migration run "
        f"{first['run_ids']!r}: pid={first['pid']}"
    )


def _validate_run_ids(run_ids: object) -> list[str]:
    if not isinstance(run_ids, list) or not run_ids:
        raise SixStageMigrationError("at least one run ID is required")
    validated: list[str] = []
    seen: set[str] = set()
    for value in run_ids:
        run_id = _validate_component(value, "run ID")
        if run_id in seen:
            raise SixStageMigrationError(f"duplicate run ID: {run_id}")
        seen.add(run_id)
        validated.append(run_id)
    return validated


def plan_migration(repo: Path, run_ids: list[str]) -> dict[str, Any]:
    """Return a read-only, hash-bound schema-v2 migration plan."""

    repo = _require_directory(Path(repo), "repository")
    validated = _validate_run_ids(run_ids)
    _require_directory(repo / "runs", "runs root")
    _require_directory(repo / "runner-state", "runner-state root")
    runs = [_inspect_run(repo, run_id) for run_id in validated]
    return {
        "schema_from": SCHEMA_FROM,
        "schema_to": SCHEMA_TO,
        "moves": dict(MOVES),
        "creates": list(CREATES),
        "runs": runs,
        "blockers": _active_process_blockers(validated),
    }


def _copy_tree(source: Path, destination: Path, expected_hash: str) -> None:
    if _tree_hash(source, "migration source") != expected_hash:
        raise _error("migration source changed after planning", source)
    if _path_exists(destination):
        raise _error("migration staging destination already exists", destination)
    try:
        shutil.copytree(source, destination, copy_function=shutil.copy2)
    except BaseException as error:
        _remove_owned_path(destination)
        if isinstance(error, OSError):
            raise _error("cannot copy migration source", source) from error
        raise
    try:
        if _tree_hash(destination, "staged source copy") != expected_hash:
            raise _error(
                "staged source copy does not preserve bytes",
                destination,
            )
        if _tree_hash(source, "migration source") != expected_hash:
            raise _error(
                "migration source changed while being copied",
                source,
            )
    except BaseException:
        _remove_owned_path(destination)
        raise


def _update_run_manifest(staged_run: Path) -> None:
    path = staged_run / "run.json"
    document = _read_json(path, "staged run manifest")
    if document.get("schema_version") != SCHEMA_FROM:
        raise _error("staged run manifest schema version changed", path)
    document["schema_version"] = SCHEMA_TO
    timeouts = document.get("timeouts")
    if not isinstance(timeouts, dict):
        raise _error("staged run timeout policy is malformed", path)
    timeouts["lemma_initial_s"] = 1200
    timeouts["lemma_total_s"] = 1200
    import_tooling = document.get("import_tooling")
    if isinstance(import_tooling, dict):
        import_tooling["pipeline_schema_version"] = SCHEMA_TO
    _write_json(path, document)


def _update_task_manifest(
    staged_task: Path,
    task_plan: Mapping[str, Any],
) -> None:
    path = staged_task / "task.json"
    document = _read_json(path, "staged task manifest")
    if document.get("schema_version") != SCHEMA_FROM:
        raise _error("staged task manifest schema version changed", path)
    document["schema_version"] = SCHEMA_TO
    if document.get("current_stage") in _LEGACY_STAGES:
        document["current_stage"] = "03-lemma-discovery"
    provenance = task_plan.get("session_provenance")
    if not isinstance(provenance, dict):
        raise SixStageMigrationError(
            "migration task session provenance is malformed"
        )
    document["session_provenance"] = provenance
    if provenance.get("status") == "UNRECOVERABLE":
        document["pipeline_block"] = _SESSION_BLOCK
    elif provenance.get("status") == "RECOVERABLE":
        if document.get("pipeline_block") == _SESSION_BLOCK:
            document.pop("pipeline_block")
    else:
        raise SixStageMigrationError(
            "migration task session provenance is malformed"
        )
    _write_json(path, document)


def _transform_task(
    staged_task: Path,
    task_plan: Mapping[str, Any],
) -> None:
    temporary: dict[str, Path] = {}
    for index, source in enumerate(_LEGACY_STAGES, 3):
        source_path = staged_task / source
        temporary_path = staged_task / f".schema-v2-stage-{index}"
        if temporary_path.exists() or temporary_path.is_symlink():
            raise _error("reserved migration path already exists", temporary_path)
        try:
            source_path.rename(temporary_path)
        except OSError as error:
            raise _error("cannot stage legacy evidence", source_path) from error
        temporary[source] = temporary_path

    for relative in CREATES:
        try:
            (staged_task / relative).mkdir(parents=True, exist_ok=False)
        except OSError as error:
            raise _error(
                "cannot create canonical stage directory",
                staged_task / relative,
            ) from error

    legacy_trees = task_plan.get("legacy_trees")
    if not isinstance(legacy_trees, dict):
        raise SixStageMigrationError("migration task plan is malformed")
    for source, destination in MOVES.items():
        destination_path = staged_task / destination
        try:
            temporary[source].rename(destination_path)
        except OSError as error:
            raise _error(
                "cannot preserve legacy stage evidence",
                destination_path,
            ) from error
        if _tree_hash(destination_path, "preserved legacy stage") != legacy_trees.get(
            source
        ):
            raise _error("legacy stage hash changed during migration", destination_path)

    _update_task_manifest(staged_task, task_plan)


def _filter_legacy_ledger(source: bytes, path: Path) -> bytes:
    retained: list[bytes] = []
    for line_number, line in enumerate(source.splitlines(keepends=True), 1):
        if not line.strip():
            retained.append(line)
            continue
        try:
            document = json.loads(line)
        except json.JSONDecodeError as error:
            raise _error(
                f"schema-v2 stage ledger is malformed at line {line_number}",
                path,
            ) from error
        if not isinstance(document, dict):
            raise _error(
                f"schema-v2 stage ledger line {line_number} is not an object",
                path,
            )
        stage = document.get("stage")
        if stage is None or stage in _ACTIVE_STAGES:
            retained.append(line)
    return b"".join(retained)


def _transform_task_state(
    staged_state: Path,
    session_provenance: Mapping[str, Any],
) -> None:
    legacy = staged_state / "legacy-v2"
    try:
        legacy.mkdir()
    except OSError as error:
        raise _error(
            "cannot create runner-state legacy evidence root",
            legacy,
        ) from error
    session_path = staged_state / "session.json"
    ledger_path = pipeline_contract.require_regular_file(
        staged_state / "stage-ledger.jsonl",
        "staged stage ledger",
    )
    try:
        ledger_bytes = ledger_path.read_bytes()
        (legacy / "stage-ledger.jsonl").write_bytes(ledger_bytes)
        ledger_path.write_bytes(_filter_legacy_ledger(ledger_bytes, ledger_path))
    except OSError as error:
        raise _error("cannot preserve schema-v2 runner state", staged_state) from error

    legacy_session_present = session_provenance.get(
        "legacy_session_present"
    )
    session_bytes = _optional_regular_bytes(session_path)
    if legacy_session_present is True:
        if session_bytes is None:
            raise _error(
                "planned legacy session evidence disappeared",
                session_path,
            )
        if hashlib.sha256(session_bytes).hexdigest() != (
            session_provenance.get("legacy_session_sha256")
        ):
            raise _error(
                "planned legacy session evidence changed",
                session_path,
            )
        try:
            (legacy / "session.json").write_bytes(session_bytes)
        except OSError as error:
            raise _error(
                "cannot preserve schema-v2 session state",
                session_path,
            ) from error
    elif legacy_session_present is not False or session_bytes is not None:
        raise SixStageMigrationError(
            "migration task session provenance is malformed"
        )

    if session_provenance.get("status") == "RECOVERABLE":
        session = _read_json(session_path, "staged session state")
        home = _require_directory(
            staged_state / "codex-home",
            "staged persistent CODEX_HOME",
        )
        home_stat = home.stat()
        session["schema_version"] = SCHEMA_TO
        session["codex_home_device"] = home_stat.st_dev
        session["codex_home_inode"] = home_stat.st_ino
        _write_json(session_path, session)
    elif session_provenance.get("status") == "UNRECOVERABLE":
        if session_bytes is not None:
            try:
                session_path.unlink()
            except OSError as error:
                raise _error(
                    "cannot quarantine unrecoverable session state",
                    session_path,
                ) from error
    else:
        raise SixStageMigrationError(
            "migration task session provenance is malformed"
        )
    try:
        if session_path.exists():
            session_path.chmod(0o600)
        ledger_path.chmod(0o600)
    except OSError as error:
        raise _error("cannot protect migrated runner state", staged_state) from error


def _validate_staged_run(
    staged_run: Path,
    staged_state: Path,
    run_plan: Mapping[str, Any],
) -> None:
    run_manifest = _read_json(staged_run / "run.json", "migrated run manifest")
    if run_manifest.get("schema_version") != SCHEMA_TO:
        raise _error("migrated run manifest schema version is not 3")
    if run_manifest.get("run_id") != run_plan.get("run_id"):
        raise _error("migrated run manifest ID changed")
    timeouts = run_manifest.get("timeouts")
    if not isinstance(timeouts, dict) or (
        timeouts.get("lemma_initial_s"),
        timeouts.get("lemma_total_s"),
    ) != (1200, 1200):
        raise _error("migrated run lemma timeout policy is invalid")
    tasks = run_plan.get("tasks")
    if not isinstance(tasks, list):
        raise SixStageMigrationError("migration run plan is malformed")
    for task_plan in tasks:
        if not isinstance(task_plan, dict):
            raise SixStageMigrationError("migration task plan is malformed")
        problem = task_plan.get("problem_id")
        if not isinstance(problem, str):
            raise SixStageMigrationError("migration problem ID is malformed")
        task = _require_directory(
            staged_run / "tasks" / problem,
            "migrated task",
        )
        state = _require_directory(
            staged_state / problem,
            "migrated task state",
        )
        manifest = _read_json(task / "task.json", "migrated task manifest")
        if manifest.get("schema_version") != SCHEMA_TO:
            raise _error("migrated task manifest schema version is not 3")
        session_provenance = task_plan.get("session_provenance")
        if (
            not isinstance(session_provenance, dict)
            or manifest.get("session_provenance") != session_provenance
        ):
            raise _error(
                "migrated task session provenance changed",
                task / "task.json",
            )
        legacy_trees = task_plan.get("legacy_trees")
        if not isinstance(legacy_trees, dict):
            raise SixStageMigrationError("migration task plan is malformed")
        for stage in _ACTIVE_STAGES:
            if _tree_hash(task / stage, f"migrated {stage}") != legacy_trees.get(
                stage
            ):
                raise _error("Stage 1/2 evidence changed", task / stage)
        for source, destination in MOVES.items():
            if _tree_hash(
                task / destination,
                f"migrated {source}",
            ) != legacy_trees.get(source):
                raise _error("legacy stage evidence changed", task / destination)
        for relative in CREATES:
            directory = _require_directory(
                task / relative,
                "empty canonical stage directory",
            )
            try:
                if any(directory.iterdir()):
                    raise _error(
                        "canonical migrated stage directory is not empty",
                        directory,
                    )
            except OSError as error:
                raise _error(
                    "cannot inspect canonical stage directory",
                    directory,
                ) from error
        if (task / "04-klean-generation/selected.json").exists():
            raise _error(
                "legacy Klean generation became canonical selected evidence",
                task / "04-klean-generation/selected.json",
            )
        if any(task.rglob("auth.json")) or any(task.rglob("codex-home")):
            raise _error("credential state was copied into the run", task)
        legacy_state = _require_directory(
            state / "legacy-v2",
            "legacy runner-state evidence",
        )
        pipeline_contract.require_regular_file(
            legacy_state / "stage-ledger.jsonl",
            "legacy schema-v2 stage ledger",
        )
        if session_provenance.get("legacy_session_present") is True:
            legacy_session = pipeline_contract.require_regular_file(
                legacy_state / "session.json",
                "legacy schema-v2 session manifest",
            )
            if hashlib.sha256(legacy_session.read_bytes()).hexdigest() != (
                session_provenance.get("legacy_session_sha256")
            ):
                raise _error(
                    "legacy schema-v2 session bytes changed",
                    legacy_session,
                )
        elif (legacy_state / "session.json").exists():
            raise _error(
                "unexpected legacy schema-v2 session manifest",
                legacy_state / "session.json",
            )
        if session_provenance.get("status") == "RECOVERABLE":
            session = _read_json(
                state / "session.json", "migrated session state"
            )
            if (
                session.get("schema_version") != SCHEMA_TO
                or session.get("session_id")
                != session_provenance.get("session_id")
                or manifest.get("pipeline_block") == _SESSION_BLOCK
            ):
                raise _error(
                    "migrated recoverable session binding is invalid",
                    state,
                )
            try:
                pipeline_contract._read_session_state(state)
            except pipeline_contract.PipelineContractError as error:
                raise _error(
                    "migrated session binding is invalid", state
                ) from error
        elif session_provenance.get("status") == "UNRECOVERABLE":
            if (state / "session.json").exists():
                raise _error(
                    "unrecoverable session remained canonically resumable",
                    state / "session.json",
                )
            try:
                block = pipeline_contract.task_pipeline_block(task)
            except pipeline_contract.PipelineContractError as error:
                raise _error(
                    "migrated session blocker is invalid",
                    task / "task.json",
                ) from error
            if block != _SESSION_BLOCK:
                raise _error(
                    "migrated unrecoverable session is not blocked",
                    task / "task.json",
                )
        else:
            raise _error(
                "migrated task session provenance is malformed",
                task / "task.json",
            )


def _stage_run(
    repo: Path,
    run_plan: Mapping[str, Any],
    transaction_id: str,
) -> tuple[Path, Path]:
    run_id = run_plan.get("run_id")
    if not isinstance(run_id, str):
        raise SixStageMigrationError("migration run plan is malformed")
    source_run = repo / "runs" / run_id
    source_state = repo / "runner-state" / run_id
    staged_run = repo / "runs" / (
        f".six-stage-migration-{transaction_id}-{run_id}"
    )
    staged_state = repo / "runner-state" / (
        f".six-stage-migration-{transaction_id}-{run_id}"
    )
    source_hash = run_plan.get("source_sha256")
    state_hash = run_plan.get("runner_state_sha256")
    if not isinstance(source_hash, str) or not isinstance(state_hash, str):
        raise SixStageMigrationError("migration source hashes are malformed")
    try:
        _copy_tree(source_run, staged_run, source_hash)
        _copy_tree(source_state, staged_state, state_hash)
        _update_run_manifest(staged_run)
        tasks = run_plan.get("tasks")
        if not isinstance(tasks, list):
            raise SixStageMigrationError("migration run tasks are malformed")
        for task_plan in tasks:
            if not isinstance(task_plan, dict):
                raise SixStageMigrationError("migration task plan is malformed")
            problem = task_plan.get("problem_id")
            if not isinstance(problem, str):
                raise SixStageMigrationError("migration problem ID is malformed")
            _transform_task(staged_run / "tasks" / problem, task_plan)
            session_provenance = task_plan.get("session_provenance")
            if not isinstance(session_provenance, dict):
                raise SixStageMigrationError(
                    "migration task session provenance is malformed"
                )
            _transform_task_state(
                staged_state / problem,
                session_provenance,
            )
        _validate_staged_run(staged_run, staged_state, run_plan)
    except BaseException:
        _remove_owned_path(staged_run)
        _remove_owned_path(staged_state)
        raise
    return staged_run, staged_state


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_regular_file(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise _error("staged tree entry is not a regular file", path)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_tree(root: Path) -> None:
    """Recursively make every staged file and directory durable."""

    root = _require_directory(root, "staged migration tree")
    pending = [root]
    directories: list[Path] = []
    files: list[Path] = []
    try:
        while pending:
            directory = pending.pop()
            directories.append(directory)
            entries = sorted(
                os.scandir(directory),
                key=lambda entry: entry.name,
            )
            for entry in entries:
                path = Path(entry.path)
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    files.append(path)
                else:
                    raise _error(
                        "staged tree contains linked or unsupported entry",
                        path,
                    )
        for path in sorted(files):
            _fsync_regular_file(path)
        for path in sorted(
            directories,
            key=lambda directory: len(directory.parts),
            reverse=True,
        ):
            _fsync_directory(path)
    except OSError as error:
        raise _error("cannot fsync staged tree", root) from error


def _atomic_exchange(first: Path, second: Path) -> None:
    """Exchange paths atomically; the caller owns durability bookkeeping."""

    libc = ctypes.CDLL(None, use_errno=True)
    try:
        renameat2 = libc.renameat2
    except AttributeError as error:
        raise _error("atomic path exchange is unavailable") from error
    renameat2.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    renameat2.restype = ctypes.c_int
    result = renameat2(
        _AT_FDCWD,
        os.fsencode(first),
        _AT_FDCWD,
        os.fsencode(second),
        _RENAME_EXCHANGE,
    )
    if result != 0:
        error_number = ctypes.get_errno()
        detail = os.strerror(error_number or errno.EIO)
        raise _error(f"atomic path exchange failed: {detail}", first)


def _fsync_exchange_parents(first: Path, second: Path) -> None:
    """Make a completed exchange durable only after it is recoverable."""

    _fsync_directory(first.parent)
    if second.parent != first.parent:
        _fsync_directory(second.parent)


def _publication_boundary(_name: str) -> None:
    """Failure-injection seam around complete-run publication."""


def _validate_plan_shape(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    if (
        plan.get("schema_from") != SCHEMA_FROM
        or plan.get("schema_to") != SCHEMA_TO
        or plan.get("moves") != MOVES
        or plan.get("creates") != CREATES
    ):
        raise SixStageMigrationError("migration plan layout is malformed")
    runs = plan.get("runs")
    if (
        not isinstance(runs, list)
        or not runs
        or any(not isinstance(run, dict) for run in runs)
    ):
        raise SixStageMigrationError("migration plan run list is malformed")
    seen_runs: set[str] = set()
    for run in runs:
        run_id = _validate_component(run.get("run_id"), "planned run ID")
        if run_id in seen_runs:
            raise SixStageMigrationError(
                f"duplicate run ID in migration plan: {run_id}"
            )
        seen_runs.add(run_id)
        tasks = run.get("tasks")
        if not isinstance(tasks, list) or any(
            not isinstance(task, dict) for task in tasks
        ):
            raise SixStageMigrationError(
                f"migration plan tasks are malformed for run {run_id}"
            )
        seen_problems: set[str] = set()
        for task in tasks:
            problem = _validate_component(
                task.get("problem_id"),
                "planned problem ID",
            )
            if problem in seen_problems:
                raise SixStageMigrationError(
                    "duplicate problem ID in migration plan "
                    f"for run {run_id}: {problem}"
                )
            seen_problems.add(problem)
            provenance = task.get("session_provenance")
            if not isinstance(provenance, dict):
                raise SixStageMigrationError(
                    "migration task session provenance is malformed"
                )
            status = provenance.get("status")
            if status == "RECOVERABLE":
                if (
                    provenance.get("reason") is not None
                    or _canonical_uuid(provenance.get("session_id"))
                    != provenance.get("session_id")
                    or provenance.get("legacy_session_present") is not True
                ):
                    raise SixStageMigrationError(
                        "recoverable migration session proof is malformed"
                    )
            elif status == "UNRECOVERABLE":
                if provenance.get("reason") not in _SESSION_REASONS:
                    raise SixStageMigrationError(
                        "unrecoverable migration session proof is malformed"
                    )
            else:
                raise SixStageMigrationError(
                    "migration task session provenance is malformed"
                )
    return runs


def _assert_sources_match_plan(repo: Path, runs: Sequence[Mapping[str, Any]]) -> None:
    for run in runs:
        run_id = _validate_component(run.get("run_id"), "planned run ID")
        source = repo / "runs" / run_id
        manifest = _read_json(
            source / "run.json",
            "planned source run manifest",
        )
        if manifest.get("schema_version") != SCHEMA_FROM:
            raise _error("planned source run schema version is not 2", source)
        source_tasks = _task_ids(source, manifest)
        planned_tasks = run.get("tasks")
        if not isinstance(planned_tasks, list):
            raise SixStageMigrationError("migration plan tasks are malformed")
        planned_problem_ids = [
            _validate_component(
                task.get("problem_id"),
                "planned problem ID",
            )
            for task in planned_tasks
        ]
        if planned_problem_ids != source_tasks:
            raise SixStageMigrationError(
                f"planned tasks do not match source manifest for run {run_id}"
            )
        source_state = _require_directory(
            repo / "runner-state" / run_id,
            "planned schema-v2 runner state",
        )
        for task_plan in planned_tasks:
            problem = _validate_component(
                task_plan.get("problem_id"),
                "planned problem ID",
            )
            current_provenance = _inspect_session_provenance(
                source / "tasks" / problem,
                _require_directory(
                    source_state / problem,
                    "planned schema-v2 task runner state",
                ),
            )
            if current_provenance != task_plan.get(
                "session_provenance"
            ):
                raise _error(
                    "migration session evidence changed after planning",
                    source_state / problem,
                )
        if _tree_hash(
            source,
            "planned schema-v2 run",
        ) != run.get("source_sha256"):
            raise _error(
                "migration run changed after planning",
                source,
            )
        if _tree_hash(
            repo / "runner-state" / run_id,
            "planned schema-v2 runner state",
        ) != run.get("runner_state_sha256"):
            raise _error(
                "migration runner state changed after planning",
                repo / "runner-state" / run_id,
            )


def _journal_path(repo: Path) -> Path:
    return repo / "runner-state" / _JOURNAL_NAME


def _valid_digest(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _write_journal(repo: Path, journal: dict[str, Any]) -> None:
    path = _journal_path(repo)
    _write_json(path, journal)
    _fsync_directory(path.parent)


def _remove_journal(repo: Path) -> None:
    path = _journal_path(repo)
    try:
        path.unlink()
    except FileNotFoundError:
        return
    except OSError as error:
        raise _error("cannot remove migration transaction journal", path) from error
    _fsync_directory(path.parent)


def _validate_journal(
    repo: Path,
    journal: dict[str, Any],
) -> dict[str, Any]:
    if journal.get("schema_version") != _JOURNAL_SCHEMA_VERSION:
        raise _error("migration transaction journal schema is invalid")
    transaction_id = _validate_component(
        journal.get("transaction_id"),
        "migration transaction ID",
    )
    phase = journal.get("phase")
    if phase not in _JOURNAL_PHASES:
        raise _error("migration transaction journal phase is invalid")
    entries = journal.get("entries")
    if (
        not isinstance(entries, list)
        or not entries
        or any(not isinstance(entry, dict) for entry in entries)
    ):
        raise _error("migration transaction journal entries are malformed")
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        kind = entry.get("kind")
        if kind not in {"run", "state"}:
            raise _error("migration transaction journal kind is invalid")
        run_id = _validate_component(
            entry.get("run_id"),
            "journal run ID",
        )
        key = (str(kind), run_id)
        if key in seen:
            raise _error("migration transaction journal contains duplicates")
        seen.add(key)
        parent = repo / ("runs" if kind == "run" else "runner-state")
        final = parent / run_id
        backup = parent / (
            f".six-stage-migration-{transaction_id}-{run_id}"
        )
        tombstone = backup.with_name(f"{backup.name}.tombstone")
        if entry.get("final") != str(final) or entry.get("backup") != str(
            backup
        ) or entry.get("tombstone") != str(tombstone):
            raise _error("migration transaction journal path is invalid")
        if not _valid_digest(entry.get("original_sha256")) or not _valid_digest(
            entry.get("migrated_sha256")
        ):
            raise _error("migration transaction journal hash is invalid")
    return journal


def _read_journal(repo: Path) -> dict[str, Any] | None:
    path = _journal_path(repo)
    if not _path_exists(path):
        return None
    return _validate_journal(
        repo,
        _read_json(path, "migration transaction journal"),
    )


def _journal_run_ids(journal: Mapping[str, Any]) -> list[str]:
    return list(
        dict.fromkeys(
            str(entry["run_id"])
            for entry in journal["entries"]
        )
    )


def _entry_state(entry: Mapping[str, Any]) -> str:
    final = Path(str(entry["final"]))
    backup = Path(str(entry["backup"]))
    tombstone = Path(str(entry["tombstone"]))
    final_exists = _path_exists(final)
    backup_exists = _path_exists(backup)
    tombstone_exists = _path_exists(tombstone)
    if not final_exists:
        raise _error("migration final path is missing during recovery", final)
    if backup_exists and tombstone_exists:
        raise _error(
            "migration backup and tombstone both exist during recovery",
            backup,
        )
    final_hash = _tree_hash(final, "migration recovery final")
    original = entry["original_sha256"]
    migrated = entry["migrated_sha256"]
    if not backup_exists:
        if final_hash == migrated:
            return "COMMITTED"
        if final_hash == original:
            return "ROLLED_BACK"
        raise _error("migration final hash is unknown during recovery", final)
    backup_hash = _tree_hash(backup, "migration recovery backup")
    if final_hash == original and backup_hash == migrated:
        return "UNEXCHANGED"
    if final_hash == migrated and backup_hash == original:
        return "EXCHANGED"
    raise _error("migration exchange state is ambiguous during recovery", final)


def _discard_verified_backup(
    entry: Mapping[str, Any],
    expected_hash: object,
) -> None:
    backup = Path(str(entry["backup"]))
    tombstone = Path(str(entry["tombstone"]))
    backup_exists = _path_exists(backup)
    tombstone_exists = _path_exists(tombstone)
    if backup_exists and tombstone_exists:
        raise _error(
            "migration backup and tombstone both exist during cleanup",
            backup,
        )
    if backup_exists:
        if _tree_hash(backup, "migration cleanup backup") != expected_hash:
            raise _error("migration cleanup backup hash changed", backup)
        try:
            backup.rename(tombstone)
        except OSError as error:
            raise _error(
                "cannot rename migration backup to tombstone",
                backup,
            ) from error
        _publication_boundary("after-backup-tombstone-rename")
        _fsync_directory(backup.parent)
        tombstone_exists = True
    if tombstone_exists:
        _remove_owned_path(tombstone)
        _publication_boundary("after-tombstone-deletion")
    _fsync_directory(tombstone.parent)


def _rollback_incomplete_locked(
    repo: Path,
    journal: dict[str, Any],
) -> None:
    entries = list(journal["entries"])
    for entry in reversed(entries):
        state = _entry_state(entry)
        final = Path(entry["final"])
        backup = Path(entry["backup"])
        if state == "EXCHANGED":
            _atomic_exchange(final, backup)
            _fsync_exchange_parents(final, backup)
            state = _entry_state(entry)
        if state not in {"UNEXCHANGED", "ROLLED_BACK"}:
            raise _error(
                "cannot roll back committed migration transaction",
                final,
            )
        if _tree_hash(final, "rolled-back migration final") != entry.get(
            "original_sha256"
        ):
            raise _error("rolled-back migration hash changed", final)
        _discard_verified_backup(entry, entry.get("migrated_sha256"))
    _remove_journal(repo)


def _finish_validated_locked(
    repo: Path,
    journal: dict[str, Any],
) -> None:
    for entry in journal["entries"]:
        state = _entry_state(entry)
        final = Path(entry["final"])
        if state not in {"EXCHANGED", "COMMITTED"}:
            raise _error(
                "validated migration transaction is not fully published",
                final,
            )
        if _tree_hash(final, "validated migration final") != entry.get(
            "migrated_sha256"
        ):
            raise _error("validated migration hash changed", final)
        _discard_verified_backup(entry, entry.get("original_sha256"))
    _remove_journal(repo)


def _recover_transaction_locked(
    repo: Path,
    requested_run_ids: Sequence[str] = (),
) -> dict[str, Any] | None:
    journal = _read_journal(repo)
    result: dict[str, Any] | None = None
    if journal is not None:
        journal_run_ids = _journal_run_ids(journal)
        _refuse_active_processes(journal_run_ids)
        if journal["phase"] == "VALIDATED":
            _finish_validated_locked(repo, journal)
            status = "COMPLETED"
        else:
            _rollback_incomplete_locked(repo, journal)
            status = "ROLLED_BACK"
        result = {
            "status": status,
            "runs": journal_run_ids,
        }
    _refuse_active_processes(requested_run_ids)
    return result


def recover_transaction(
    repo: Path,
    requested_run_ids: Sequence[str] = (),
) -> dict[str, Any] | None:
    """Recover an interrupted publication under the repository lock."""

    repo = _require_directory(Path(repo), "repository")
    with legacy_migration.migration_lock(repo):
        return _recover_transaction_locked(repo, requested_run_ids)


def _begin_transaction(
    repo: Path,
    transaction_id: str,
    staged: Sequence[tuple[dict[str, Any], Path, Path]],
) -> dict[str, Any]:
    if _read_journal(repo) is not None:
        raise _error(
            "migration transaction journal already exists",
            _journal_path(repo),
        )
    for _run, staged_run, staged_state in staged:
        for staged_tree in (staged_run, staged_state):
            try:
                _fsync_tree(staged_tree)
                _fsync_directory(staged_tree.parent)
            except OSError as error:
                raise _error(
                    "cannot fsync staged tree",
                    staged_tree,
                ) from error
    entries: list[dict[str, Any]] = []
    for run, staged_run, staged_state in staged:
        run_id = _validate_component(run.get("run_id"), "planned run ID")
        staged_run_tombstone = staged_run.with_name(
            f"{staged_run.name}.tombstone"
        )
        staged_state_tombstone = staged_state.with_name(
            f"{staged_state.name}.tombstone"
        )
        for tombstone in (staged_run_tombstone, staged_state_tombstone):
            if _path_exists(tombstone):
                raise _error(
                    "migration cleanup tombstone already exists",
                    tombstone,
                )
        entries.extend(
            (
                {
                    "kind": "run",
                    "run_id": run_id,
                    "final": str(repo / "runs" / run_id),
                    "backup": str(staged_run),
                    "tombstone": str(staged_run_tombstone),
                    "original_sha256": run["source_sha256"],
                    "migrated_sha256": _tree_hash(
                        staged_run,
                        "staged migrated run",
                    ),
                },
                {
                    "kind": "state",
                    "run_id": run_id,
                    "final": str(repo / "runner-state" / run_id),
                    "backup": str(staged_state),
                    "tombstone": str(staged_state_tombstone),
                    "original_sha256": run["runner_state_sha256"],
                    "migrated_sha256": _tree_hash(
                        staged_state,
                        "staged migrated runner state",
                    ),
                },
            )
        )
    journal = {
        "schema_version": _JOURNAL_SCHEMA_VERSION,
        "transaction_id": transaction_id,
        "phase": "STAGED",
        "entries": entries,
    }
    _validate_journal(repo, journal)
    _write_journal(repo, journal)
    return journal


def apply_migration(repo: Path, plan: dict[str, Any]) -> dict[str, Any]:
    """Stage, validate, and atomically exchange every selected complete run."""

    repo = _require_directory(Path(repo), "repository")
    if not isinstance(plan, dict):
        raise SixStageMigrationError("migration plan must be an object")
    runs = _validate_plan_shape(plan)
    run_ids = [
        _validate_component(run.get("run_id"), "planned run ID")
        for run in runs
    ]
    with legacy_migration.migration_lock(repo):
        _recover_transaction_locked(repo, run_ids)
        _assert_sources_match_plan(repo, runs)
        transaction_id = str(uuid.uuid4())
        staged: list[tuple[dict[str, Any], Path, Path]] = []
        try:
            for run in runs:
                staged_run, staged_state = _stage_run(
                    repo,
                    run,
                    transaction_id,
                )
                staged.append((run, staged_run, staged_state))
            _assert_sources_match_plan(repo, runs)
        except BaseException:
            for _run, staged_run, staged_state in staged:
                _remove_owned_path(staged_run)
                _remove_owned_path(staged_state)
            raise

        journal: dict[str, Any] | None = None
        try:
            journal = _begin_transaction(
                repo,
                transaction_id,
                staged,
            )
            journal["phase"] = "PUBLISHING"
            _write_journal(repo, journal)
            for entry in journal["entries"]:
                final = Path(entry["final"])
                backup = Path(entry["backup"])
                _atomic_exchange(final, backup)
                entry["exchange_observed"] = True
                _write_journal(repo, journal)
                _fsync_exchange_parents(final, backup)
                boundary = (
                    "after-run-exchange"
                    if entry["kind"] == "run"
                    else "after-state-exchange"
                )
                _publication_boundary(boundary)
            for run, _staged_run, _staged_state in staged:
                run_id = _validate_component(
                    run.get("run_id"),
                    "planned run ID",
                )
                _validate_staged_run(
                    repo / "runs" / run_id,
                    repo / "runner-state" / run_id,
                    run,
                )
            journal["phase"] = "VALIDATED"
            _write_journal(repo, journal)
            _publication_boundary("after-publication-validation")
        except BaseException as error:
            if journal is None:
                for _run, staged_run, staged_state in staged:
                    _remove_owned_path(staged_run)
                    _remove_owned_path(staged_state)
                raise
            try:
                _recover_transaction_locked(repo)
            except BaseException as rollback_error:
                raise SixStageMigrationError(
                    "six-stage migration rollback failed; "
                    "manual recovery is required"
                ) from rollback_error
            raise error

        if journal is None:
            raise SixStageMigrationError("migration transaction was not started")
        _finish_validated_locked(repo, journal)
        return {
            "status": "COMPLETE",
            "schema_from": SCHEMA_FROM,
            "schema_to": SCHEMA_TO,
            "runs": run_ids,
        }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("run_ids", nargs="+")
    parser.add_argument("--report", type=Path)
    return parser


def _emit(document: dict[str, Any], report: Path | None) -> None:
    if report is not None:
        pipeline_contract.write_json_atomic(report, document)
    print(json.dumps(document, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        requested_run_ids = _validate_run_ids(list(arguments.run_ids))
        if arguments.apply:
            recovery = recover_transaction(
                arguments.repo,
                requested_run_ids,
            )
            if (
                recovery is not None
                and recovery["status"] == "COMPLETED"
                and set(requested_run_ids).issubset(recovery["runs"])
            ):
                _emit(
                    {
                        "mode": "apply",
                        "status": "COMPLETE",
                        "schema_from": SCHEMA_FROM,
                        "schema_to": SCHEMA_TO,
                        "runs": requested_run_ids,
                        "recovery": "COMPLETED",
                    },
                    arguments.report,
                )
                return 0
        plan = plan_migration(arguments.repo, requested_run_ids)
        if arguments.dry_run:
            _emit({"mode": "dry-run", **plan}, arguments.report)
            return 0
        result = apply_migration(arguments.repo, plan)
        _emit({"mode": "apply", **result}, arguments.report)
        return 0
    except (
        SixStageMigrationError,
        pipeline_contract.PipelineContractError,
        OSError,
        ValueError,
    ) as error:
        print(f"six-stage migration error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
