#!/usr/bin/env python3
"""Extract and aggregate stable token and runtime usage documents."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Mapping, Sequence


TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)

MONETARY_COST_UNAVAILABLE = {
    "status": "UNAVAILABLE",
    "reason": "No authoritative charge or pricing snapshot was recorded",
}

_HASH_CHUNK_SIZE = 1024 * 1024
# Stages 1/3/5 share a model session, so summaries consume each persisted
# invocation delta rather than recomputing deltas from cumulative counters.
_STAGE_LAYOUTS = (
    ("01-k-proof", "invocations"),
    ("02-k-audit", "executions"),
    ("03-lemma-discovery", "invocations"),
    ("05-lean-proof", "invocations"),
    ("06-lean-audit", "executions"),
)


class UsageAccountingError(RuntimeError):
    """Raised when trace or usage evidence violates the accounting contract."""


def _empty_counters() -> dict[str, int]:
    return dict.fromkeys(TOKEN_FIELDS, 0)


def _normalize_counters(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        raise UsageAccountingError("token counters must be an object")
    counters: dict[str, int] = {}
    for name in TOKEN_FIELDS:
        counter = value.get(name)
        if isinstance(counter, bool) or not isinstance(counter, int) or counter < 0:
            raise UsageAccountingError(f"{name} must be a non-negative integer")
        counters[name] = counter
    if counters["cached_input_tokens"] > counters["input_tokens"]:
        raise UsageAccountingError("cached input exceeds input tokens")
    if counters["reasoning_output_tokens"] > counters["output_tokens"]:
        raise UsageAccountingError("reasoning output exceeds output tokens")
    return counters


def _normalize_delta(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        raise UsageAccountingError("invocation_delta must be an object")
    delta: dict[str, int] = {}
    for name in TOKEN_FIELDS:
        counter = value.get(name)
        if isinstance(counter, bool) or not isinstance(counter, int) or counter < 0:
            raise UsageAccountingError(
                f"invocation_delta.{name} must be a non-negative integer"
            )
        delta[name] = counter
    return delta


def _require_real_directory(path: Path, label: str) -> Path:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        raise UsageAccountingError(
            f"{label} cannot be inspected: {path}: {error}"
        ) from error
    if not stat.S_ISDIR(mode):
        raise UsageAccountingError(f"{label} must be a real directory: {path}")
    return path


def _tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    root = _require_real_directory(root, "tree root")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        try:
            children = list(os.scandir(directory))
        except OSError as error:
            raise UsageAccountingError(
                f"cannot scan tree {directory}: {error}"
            ) from error
        for child in children:
            path = Path(child.path)
            try:
                mode = child.stat(follow_symlinks=False).st_mode
            except OSError as error:
                raise UsageAccountingError(
                    f"cannot inspect tree entry {path}: {error}"
                ) from error
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise UsageAccountingError(
                    f"tree contains linked or unsupported entry: {path}"
                )
    return sorted(entries)


def _hash_tree_entries(entries: Sequence[tuple[str, str, Path]]) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in entries:
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind != "file":
            continue
        try:
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(_HASH_CHUNK_SIZE), b""):
                    digest.update(chunk)
        except OSError as error:
            raise UsageAccountingError(
                f"cannot hash tree file {path}: {error}"
            ) from error
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Hash a real regular-file tree using the pipeline's framed format."""

    return _hash_tree_entries(_tree_entries(root))


def _read_trace_events(
    entries: Sequence[tuple[str, str, Path]],
) -> tuple[
    dict[str, int] | None,
    dict[str, Any] | None,
    list[dict[str, Any]],
]:
    cumulative: dict[str, int] | None = None
    selected_event: dict[str, Any] | None = None
    session_counters: dict[str, dict[str, int]] = {}
    session_events: dict[str, dict[str, Any]] = {}
    for relative, kind, path in entries:
        if kind != "file":
            continue
        file_session_ids: set[str] = set()
        file_cumulative: dict[str, int] | None = None
        file_selected_event: dict[str, Any] | None = None
        try:
            with path.open("r", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, start=1):
                    if not line.strip():
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError as error:
                        raise UsageAccountingError(
                            f"malformed JSON at {relative}:{line_number}: {error.msg}"
                        ) from error
                    if not isinstance(event, dict):
                        continue
                    if event.get("type") == "session_meta":
                        payload = event.get("payload")
                        value = (
                            payload.get("id")
                            if isinstance(payload, dict)
                            else None
                        )
                        try:
                            file_session_ids.add(str(uuid.UUID(value)))
                        except (AttributeError, TypeError, ValueError) as error:
                            raise UsageAccountingError(
                                f"malformed session UUID at "
                                f"{relative}:{line_number}"
                            ) from error
                        continue
                    if event.get("type") != "event_msg":
                        continue
                    payload = event.get("payload")
                    if (
                        not isinstance(payload, dict)
                        or payload.get("type") != "token_count"
                    ):
                        continue
                    info = payload.get("info")
                    # Codex can emit an initial rate-limit-only token_count
                    # event before any usage counters are available.
                    if info is None:
                        continue
                    value = (
                        info.get("total_token_usage")
                        if isinstance(info, dict)
                        else None
                    )
                    file_cumulative = _normalize_counters(value)
                    file_selected_event = {
                        "relative_path": relative,
                        "line_number": line_number,
                    }
        except UsageAccountingError:
            raise
        except (OSError, UnicodeError) as error:
            raise UsageAccountingError(
                f"cannot read trace file {path}: {error}"
            ) from error
        if len(file_session_ids) > 1:
            raise UsageAccountingError(
                f"rollout names multiple sessions: {relative}"
            )
        if file_cumulative is None:
            continue
        if file_session_ids:
            session_id = next(iter(file_session_ids))
            if session_id in session_counters:
                raise UsageAccountingError(
                    f"session has multiple rollout files: {session_id}"
                )
            session_counters[session_id] = file_cumulative
            session_events[session_id] = {
                "session_id": session_id,
                **file_selected_event,
            }
        else:
            cumulative = file_cumulative
            selected_event = file_selected_event
    if session_counters:
        if cumulative is not None:
            raise UsageAccountingError(
                "trace mixes session-bound and legacy token counters"
            )
        cumulative = _empty_counters()
        for counters in session_counters.values():
            _add_counters(cumulative, counters)
        ordered_events = sorted(
            session_events.values(),
            key=lambda event: (
                event["relative_path"],
                event["line_number"],
                event["session_id"],
            ),
        )
        selected_event = {
            "relative_path": ordered_events[-1]["relative_path"],
            "line_number": ordered_events[-1]["line_number"],
        }
        return cumulative, selected_event, ordered_events
    return cumulative, selected_event, []


def extract_trace_usage(
    trace_root: Path,
    *,
    previous_cumulative: Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """Extract the terminal cumulative token event and its invocation delta."""

    previous = (
        _empty_counters()
        if previous_cumulative is None
        else _normalize_counters(previous_cumulative)
    )
    entries = _tree_entries(trace_root)
    source_hash = _hash_tree_entries(entries)
    cumulative, selected_event, session_events = _read_trace_events(entries)
    if cumulative is None:
        return {
            "schema_version": 2,
            "status": "MISSING",
            "source_trace_sha256": source_hash,
            "selected_event": None,
            "session_events": session_events,
            "cumulative": None,
            "previous_cumulative": previous,
            "invocation_delta": None,
            "monetary_cost": MONETARY_COST_UNAVAILABLE.copy(),
        }

    regressed = [
        name for name in TOKEN_FIELDS if cumulative[name] < previous[name]
    ]
    if regressed:
        raise UsageAccountingError(
            "cumulative token counter regressed: " + ", ".join(regressed)
        )
    delta = {
        name: cumulative[name] - previous[name]
        for name in TOKEN_FIELDS
    }
    return {
        "schema_version": 2,
        "status": "COMPLETE",
        "source_trace_sha256": source_hash,
        "selected_event": selected_event,
        "session_events": session_events,
        "cumulative": cumulative,
        "previous_cumulative": previous,
        "invocation_delta": delta,
        "monetary_cost": MONETARY_COST_UNAVAILABLE.copy(),
    }


def _write_json_atomic(destination: Path, document: dict[str, Any]) -> None:
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            dir=destination.parent,
        )
    except OSError as error:
        raise UsageAccountingError(
            f"cannot prepare output {destination}: {error}"
        ) from error
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except OSError as error:
        raise UsageAccountingError(
            f"cannot write output {destination}: {error}"
        ) from error
    finally:
        try:
            if temporary.exists():
                temporary.unlink()
        except OSError:
            pass


def write_trace_usage(
    trace_root: Path,
    destination: Path,
    *,
    previous_cumulative: Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """Extract and atomically publish one trace's usage document."""

    document = extract_trace_usage(
        trace_root,
        previous_cumulative=previous_cumulative,
    )
    _write_json_atomic(destination, document)
    return document


def _execution_directories(
    run: Path,
) -> list[tuple[str, str, Path]]:
    _require_real_directory(run, "run")
    tasks = run / "tasks"
    if not tasks.exists() and not tasks.is_symlink():
        return []
    _require_real_directory(tasks, "run tasks")
    executions: list[tuple[str, str, Path]] = []
    try:
        task_paths = sorted(tasks.iterdir(), key=lambda path: path.name)
    except OSError as error:
        raise UsageAccountingError(f"cannot scan run tasks: {error}") from error
    for task in task_paths:
        try:
            mode = task.lstat().st_mode
        except OSError as error:
            raise UsageAccountingError(
                f"cannot inspect run task {task}: {error}"
            ) from error
        if not stat.S_ISDIR(mode):
            raise UsageAccountingError(
                f"run contains linked or unsupported task: {task}"
            )
        for stage, collection_name in _STAGE_LAYOUTS:
            stage_root = task / stage
            if not stage_root.exists() and not stage_root.is_symlink():
                continue
            _require_real_directory(stage_root, f"{stage} stage")
            collection = stage_root / collection_name
            if not collection.exists() and not collection.is_symlink():
                continue
            _require_real_directory(
                collection,
                f"{stage} {collection_name}",
            )
            try:
                children = sorted(
                    collection.iterdir(),
                    key=lambda path: path.name,
                )
            except OSError as error:
                raise UsageAccountingError(
                    f"cannot scan execution collection {collection}: {error}"
                ) from error
            for execution in children:
                try:
                    child_mode = execution.lstat().st_mode
                except OSError as error:
                    raise UsageAccountingError(
                        f"cannot inspect execution {execution}: {error}"
                    ) from error
                if stat.S_ISDIR(child_mode):
                    executions.append((task.name, stage, execution))
                else:
                    raise UsageAccountingError(
                        f"run contains linked or unsupported execution: {execution}"
                    )
    return executions


def _relative(path: Path, run: Path) -> str:
    return path.relative_to(run).as_posix()


def _read_regular_json(path: Path, label: str) -> dict[str, Any]:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        raise UsageAccountingError(f"{label} cannot be inspected: {error}") from error
    if not stat.S_ISREG(mode):
        raise UsageAccountingError(f"{label} must be a real regular file")
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise UsageAccountingError(f"{label} is malformed: {error}") from error
    if not isinstance(document, dict):
        raise UsageAccountingError(f"{label} must contain a JSON object")
    return document


def _add_counters(destination: dict[str, int], addition: Mapping[str, int]) -> None:
    for name in TOKEN_FIELDS:
        destination[name] += addition[name]


def _validate_usage_document(document: dict[str, Any]) -> dict[str, int] | None:
    if document.get("schema_version") != 2:
        raise UsageAccountingError("usage document schema_version must be 2")
    source_hash = document.get("source_trace_sha256")
    if (
        not isinstance(source_hash, str)
        or len(source_hash) != 64
        or any(character not in "0123456789abcdef" for character in source_hash)
    ):
        raise UsageAccountingError(
            "usage document source_trace_sha256 must be a lowercase SHA-256"
        )
    if document.get("monetary_cost") != MONETARY_COST_UNAVAILABLE:
        raise UsageAccountingError(
            "usage document monetary_cost must be explicitly UNAVAILABLE"
        )
    previous = _normalize_counters(document.get("previous_cumulative"))
    status_value = document.get("status")
    if status_value == "MISSING":
        if document.get("selected_event") is not None:
            raise UsageAccountingError(
                "MISSING usage document selected_event must be null"
            )
        if document.get("cumulative") is not None:
            raise UsageAccountingError(
                "MISSING usage document cumulative must be null"
            )
        if document.get("invocation_delta") is not None:
            raise UsageAccountingError(
                "MISSING usage document invocation_delta must be null"
            )
        return None
    if status_value != "COMPLETE":
        raise UsageAccountingError(
            "usage document status must be COMPLETE or MISSING"
        )

    selected_event = document.get("selected_event")
    if not isinstance(selected_event, dict):
        raise UsageAccountingError(
            "COMPLETE usage document selected_event must be an object"
        )
    relative_path = selected_event.get("relative_path")
    if (
        not isinstance(relative_path, str)
        or not relative_path
        or relative_path.startswith("/")
        or any(part in {"", ".", ".."} for part in relative_path.split("/"))
    ):
        raise UsageAccountingError(
            "selected_event.relative_path must be a safe relative path"
        )
    line_number = selected_event.get("line_number")
    if (
        isinstance(line_number, bool)
        or not isinstance(line_number, int)
        or line_number < 1
    ):
        raise UsageAccountingError(
            "selected_event.line_number must be a positive integer"
        )

    cumulative = _normalize_counters(document.get("cumulative"))
    delta = _normalize_delta(document.get("invocation_delta"))
    if any(cumulative[name] < previous[name] for name in TOKEN_FIELDS):
        raise UsageAccountingError(
            "usage document cumulative token counter regressed"
        )
    expected_delta = {
        name: cumulative[name] - previous[name]
        for name in TOKEN_FIELDS
    }
    if delta != expected_delta:
        raise UsageAccountingError(
            "usage document invocation_delta does not match cumulative counters"
        )
    return delta


def _number(value: object, label: str) -> int | float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise UsageAccountingError(f"{label} must be a non-negative number")
    return value


def _runtime_observation(
    run: Path,
    execution: Path,
) -> tuple[
    int | float | None,
    int | float | None,
    int | float | None,
    list[dict[str, str]],
    str,
]:
    documents: dict[str, dict[str, Any]] = {}
    malformed: list[dict[str, str]] = []
    observed_paths: list[Path] = []
    for name in ("metrics.json", "runtime-metrics.json", "legacy-metrics.json"):
        path = execution / name
        if not path.exists() and not path.is_symlink():
            continue
        observed_paths.append(path)
        try:
            documents[name] = _read_regular_json(path, name)
        except UsageAccountingError as error:
            malformed.append(
                {
                    "relative_path": _relative(path, run),
                    "error": str(error),
                }
            )

    start: int | float | None = None
    end: int | float | None = None
    for name in ("runtime-metrics.json", "legacy-metrics.json", "metrics.json"):
        document = documents.get(name)
        if (
            document is None
            or "start_epoch" not in document
            or "end_epoch" not in document
        ):
            continue
        try:
            candidate_start = _number(
                document["start_epoch"],
                f"{name} start_epoch",
            )
            candidate_end = _number(
                document["end_epoch"],
                f"{name} end_epoch",
            )
            if candidate_end < candidate_start:
                raise UsageAccountingError(
                    f"{name} end_epoch precedes start_epoch"
                )
        except UsageAccountingError as error:
            malformed.append(
                {
                    "relative_path": _relative(execution / name, run),
                    "error": str(error),
                }
            )
            continue
        start = candidate_start
        end = candidate_end
        break

    duration: int | float | None = None
    for name in ("metrics.json", "runtime-metrics.json", "legacy-metrics.json"):
        document = documents.get(name)
        if document is None or "duration_s" not in document:
            continue
        try:
            duration = _number(document["duration_s"], f"{name} duration_s")
        except UsageAccountingError as error:
            malformed.append(
                {
                    "relative_path": _relative(execution / name, run),
                    "error": str(error),
                }
            )
            continue
        break
    if duration is None and start is not None and end is not None:
        duration = end - start
    if duration is not None:
        runtime_status = "COMPLETE"
    elif observed_paths:
        runtime_status = "MALFORMED"
        if not malformed:
            malformed.append(
                {
                    "relative_path": _relative(observed_paths[0], run),
                    "error": (
                        "runtime metrics do not contain a usable duration_s "
                        "or start/end epoch pair"
                    ),
                }
            )
    else:
        runtime_status = "MISSING"
    return duration, start, end, malformed, runtime_status


def aggregate_usage_documents(run: Path) -> dict[str, Any]:
    """Aggregate exact model and audit invocation deltas under one run."""

    totals = _empty_counters()
    stage_subtotals = {
        stage: _empty_counters()
        for stage, _collection in _STAGE_LAYOUTS
    }
    task_subtotals: dict[str, dict[str, int]] = {}
    stage_agent_seconds: dict[str, int | float] = {
        stage: 0 for stage, _collection in _STAGE_LAYOUTS
    }
    task_agent_seconds: dict[str, int | float] = {}
    agent_seconds: int | float = 0
    starts: list[int | float] = []
    ends: list[int | float] = []
    missing_observations: list[str] = []
    malformed_observations: list[dict[str, str]] = []
    missing_runtime_observations: list[str] = []
    malformed_runtime_observations: list[dict[str, str]] = []

    for task, stage, execution in _execution_directories(run):
        task_subtotals.setdefault(task, _empty_counters())
        task_agent_seconds.setdefault(task, 0)
        usage_path = execution / "usage.json"
        relative_usage = _relative(usage_path, run)
        if not usage_path.exists() and not usage_path.is_symlink():
            missing_observations.append(relative_usage)
        else:
            try:
                usage = _read_regular_json(usage_path, "usage document")
                delta = _validate_usage_document(usage)
                if delta is None:
                    missing_observations.append(relative_usage)
                else:
                    _add_counters(totals, delta)
                    _add_counters(stage_subtotals[stage], delta)
                    _add_counters(task_subtotals[task], delta)
            except UsageAccountingError as error:
                malformed_observations.append(
                    {
                        "relative_path": relative_usage,
                        "error": str(error),
                    }
                )

        duration, start, end, runtime_malformed, runtime_status = (
            _runtime_observation(run, execution)
        )
        malformed_runtime_observations.extend(runtime_malformed)
        if duration is None:
            if runtime_status == "MISSING":
                missing_runtime_observations.append(_relative(execution, run))
        else:
            agent_seconds += duration
            stage_agent_seconds[stage] += duration
            task_agent_seconds[task] += duration
        if start is not None and end is not None:
            starts.append(start)
            ends.append(end)

    earliest = min(starts) if starts else None
    latest = max(ends) if ends else None
    wall_clock_span = (
        latest - earliest
        if earliest is not None and latest is not None
        else None
    )
    return {
        "schema_version": 2,
        "totals": totals,
        "stage_subtotals": stage_subtotals,
        "task_subtotals": dict(sorted(task_subtotals.items())),
        "runtime": {
            "agent_seconds": agent_seconds,
            "earliest_start_epoch": earliest,
            "latest_end_epoch": latest,
            "wall_clock_span_seconds": wall_clock_span,
            "stage_agent_seconds": stage_agent_seconds,
            "task_agent_seconds": dict(sorted(task_agent_seconds.items())),
        },
        "missing_observations": sorted(missing_observations),
        "malformed_observations": sorted(
            malformed_observations,
            key=lambda item: (item["relative_path"], item["error"]),
        ),
        "missing_runtime_observations": sorted(missing_runtime_observations),
        "malformed_runtime_observations": sorted(
            malformed_runtime_observations,
            key=lambda item: (item["relative_path"], item["error"]),
        ),
        "monetary_cost": MONETARY_COST_UNAVAILABLE.copy(),
    }


def write_run_summary(run: Path) -> dict[str, Any]:
    """Aggregate and atomically publish ``run/usage-summary.json``."""

    document = aggregate_usage_documents(run)
    _write_json_atomic(run / "usage-summary.json", document)
    return document


def _previous_cumulative(path: Path) -> dict[str, int]:
    document = _read_regular_json(path, "previous usage document")
    try:
        value = document["cumulative"]
    except KeyError as error:
        raise UsageAccountingError(
            "previous usage document is missing cumulative counters"
        ) from error
    return _normalize_counters(value)


class _UsageArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"usage accounting error: {message}\n")


def _parser() -> argparse.ArgumentParser:
    parser = _UsageArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    write_parser = subparsers.add_parser("write")
    write_parser.add_argument("--trace", type=Path, required=True)
    write_parser.add_argument("--output", type=Path, required=True)
    write_parser.add_argument("--previous", type=Path)

    summary_parser = subparsers.add_parser("summarize")
    summary_parser.add_argument("--run", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "write":
            previous = (
                _previous_cumulative(arguments.previous)
                if arguments.previous is not None
                else None
            )
            document = write_trace_usage(
                arguments.trace,
                arguments.output,
                previous_cumulative=previous,
            )
        else:
            document = write_run_summary(arguments.run)
    except UsageAccountingError as error:
        print(f"usage accounting error: {error}", file=sys.stderr)
        return 2
    json.dump(document, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
