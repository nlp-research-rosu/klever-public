#!/usr/bin/env python3
"""Read-only planning for the two approved flat legacy benchmark runs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator, Mapping, Sequence

import fcntl

from tools import pipeline_contract, stage1_runner, usage_accounting


class LegacyMigrationError(RuntimeError):
    """Raised when legacy source evidence is unsafe or internally inconsistent."""


class LegacyMigrationRollbackError(LegacyMigrationError):
    """Raised when a failed publication cannot be rolled back exactly."""


@dataclass(frozen=True)
class LegacyRunSpec:
    run_id: str
    condition: str
    expected_tasks: int
    audit_run_id: str | None
    expected_audit_distribution: tuple[int, int, int] | None = None


@dataclass(frozen=True)
class OmittedTree:
    relative_path: str
    tree_sha256: str
    file_count: int
    total_bytes: int
    reason: str = "REGENERABLE_K_BUILD_OUTPUT"


@dataclass(frozen=True)
class LegacyTaskPlan:
    run_id: str
    condition: str
    problem_id: str
    source_relative_path: str
    status: str
    input_provenance: str
    session_id: str
    codex_cli_version: str
    rollout_relative_path: str
    result_marker: str | None
    token_usage_status: str
    retained_files: tuple[tuple[str, str], ...]
    retained_directories: tuple[str, ...]
    omitted: tuple[OmittedTree, ...]
    audit_relative_path: str | None
    audit_files: tuple[tuple[str, str], ...]
    audit_directories: tuple[str, ...]
    audit_verdict: str | None
    audit_legitimacy: str | None


@dataclass(frozen=True)
class LegacyRunPlan:
    run_id: str
    condition: str
    audit_run_id: str | None
    counts: Mapping[str, int]
    tasks: tuple[LegacyTaskPlan, ...]


@dataclass(frozen=True)
class MigrationPlan:
    runs: tuple[LegacyRunPlan, ...]


@dataclass(frozen=True)
class StagedMigration:
    repo: Path
    transaction_id: str
    runs_root: Path
    state_root: Path
    imported_at: str
    importer_commit: str

    @property
    def run_staging_root(self) -> Path:
        return self.runs_root

    @property
    def state_staging_root(self) -> Path:
        return self.state_root


SOURCE_SPECS = (
    LegacyRunSpec(
        run_id="codex-gpt-5.6-sol-xhigh-bare",
        condition="bare",
        expected_tasks=164,
        audit_run_id="codex-gpt-5.6-sol-xhigh-bare",
        expected_audit_distribution=(10, 81, 71),
    ),
    LegacyRunSpec(
        run_id="codex-gpt-5.6-sol-xhigh-semantics",
        condition="semantics",
        expected_tasks=164,
        audit_run_id=None,
        expected_audit_distribution=(0, 0, 0),
    ),
)

PROVENANCE_INCOMPLETE = {
    ("codex-gpt-5.6-sol-xhigh-bare", "98-count-upper"),
    ("codex-gpt-5.6-sol-xhigh-bare", "136-largest-smallest-integers"),
    ("codex-gpt-5.6-sol-xhigh-semantics", "117-select-words"),
}

EXPECTED_TIMEOUTS = {
    ("codex-gpt-5.6-sol-xhigh-semantics", "148-bf"),
    ("codex-gpt-5.6-sol-xhigh-semantics", "151-double-the-difference"),
    ("codex-gpt-5.6-sol-xhigh-semantics", "156-int-to-mini-roman"),
    ("codex-gpt-5.6-sol-xhigh-semantics", "162-string-to-md5"),
}

_HASH_PATTERN = re.compile(r"[0-9a-f]{64}")
_SAFE_COMPONENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_COMMON_WORKSPACE_FILES = (
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
)
_AUDIT_FILES = (
    "REVIEW.md",
    "audit-input.json",
    "codex-last.txt",
    "codex-output.log",
    "metrics.json",
    "prompt.txt",
    "verdict.json",
)
_AUDIT_VERDICT_PAIRS = {
    "PASS": "LEGIT",
    "CONCERNS": "LEGIT",
    "FAIL": "NOT_LEGIT",
}
_HASH_CHUNK_SIZE = 1024 * 1024
_SOURCE_LAYOUT_VERSION = "LEGACY_FLAT_V1"
_UNKNOWN_IMAGE = "UNKNOWN_LEGACY_IMAGE"
_UNKNOWN_OBSERVATION = "UNKNOWN"
_LEGACY_PREFLIGHT = "NOT_APPLICABLE_LEGACY"
_PIPELINE_BLOCK = "INPUT_PROVENANCE_INCOMPLETE"
_LOCK_NAME = ".legacy-migration.lock"
_JOURNAL_NAME = ".legacy-migration-transaction.json"
_JOURNAL_SCHEMA_VERSION = 1
_PIPELINE_LAUNCHER_MARKERS = (
    "run_pipeline.py",
    "run_task.sh",
    "stage1_runner.py",
    "stage4_runner.py",
    "audit/run_task.sh",
    "klean/generate_task.sh",
    "klean-audit/run_task.sh",
    "resume_klean_task.sh",
)


def _error(message: str, path: Path | None = None) -> LegacyMigrationError:
    suffix = f": {path}" if path is not None else ""
    return LegacyMigrationError(f"{message}{suffix}")


def _validate_component(value: object, label: str) -> str:
    if not isinstance(value, str) or _SAFE_COMPONENT.fullmatch(value) is None:
        raise _error(f"{label} must be a safe path component")
    if value in {".", ".."}:
        raise _error(f"{label} must be a safe path component")
    return value


def _require_directory(path: Path, label: str) -> Path:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        raise _error(f"cannot inspect {label}", path) from error
    if not stat.S_ISDIR(mode):
        raise _error(f"{label} must be a real directory", path)
    return path


def _require_regular_file(path: Path, label: str, *, nonempty: bool = False) -> Path:
    try:
        file_stat = path.lstat()
    except OSError as error:
        raise _error(f"cannot inspect {label}", path) from error
    if not stat.S_ISREG(file_stat.st_mode):
        raise _error(f"{label} must be a regular file", path)
    if nonempty and file_stat.st_size == 0:
        raise _error(f"{label} must be non-empty", path)
    return path


def _path_exists(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    except OSError as error:
        raise _error("cannot inspect path", path) from error
    return True


def _read_regular_bytes(path: Path, label: str) -> bytes:
    _require_regular_file(path, label)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        with os.fdopen(descriptor, "rb") as stream:
            file_stat = os.fstat(stream.fileno())
            if not stat.S_ISREG(file_stat.st_mode):
                raise _error(f"{label} must be a regular file", path)
            content = stream.read()
    except OSError as error:
        raise _error(f"cannot read {label}", path) from error
    if len(content) != file_stat.st_size:
        raise _error(f"{label} changed while being read", path)
    return content


def _sha256_file(path: Path, label: str = "file") -> str:
    return hashlib.sha256(_read_regular_bytes(path, label)).hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        document = json.loads(_read_regular_bytes(path, label))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise _error(f"{label} is malformed JSON", path) from error
    if not isinstance(document, dict):
        raise _error(f"{label} must contain a JSON object", path)
    return document


def _read_text(path: Path, label: str) -> str:
    try:
        return _read_regular_bytes(path, label).decode()
    except UnicodeDecodeError as error:
        raise _error(f"{label} is not UTF-8", path) from error


def _scan_directories(root: Path, label: str) -> tuple[str, ...]:
    _require_directory(root, label)
    names: list[str] = []
    try:
        entries = list(os.scandir(root))
    except OSError as error:
        raise _error(f"cannot scan {label}", root) from error
    for entry in entries:
        path = Path(entry.path)
        try:
            mode = entry.stat(follow_symlinks=False).st_mode
        except OSError as error:
            raise _error(f"cannot inspect {label} entry", path) from error
        if not stat.S_ISDIR(mode):
            raise _error(f"{label} contains linked or unsupported entry", path)
        names.append(_validate_component(path.name, f"{label} entry"))
    return tuple(sorted(names))


def _tree_entries(root: Path, label: str) -> list[tuple[str, str, Path, int]]:
    _require_directory(root, label)
    entries: list[tuple[str, str, Path, int]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            children = list(os.scandir(directory))
        except OSError as error:
            raise _error(f"cannot scan {label}", directory) from error
        for child in children:
            path = Path(child.path)
            try:
                child_stat = child.stat(follow_symlinks=False)
            except OSError as error:
                raise _error(f"cannot inspect {label} entry", path) from error
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(child_stat.st_mode):
                entries.append((relative, "directory", path, child_stat.st_size))
                pending.append(path)
            elif stat.S_ISREG(child_stat.st_mode):
                entries.append((relative, "file", path, child_stat.st_size))
            else:
                raise _error(f"{label} contains linked or unsupported entry", path)
    return sorted(entries)


def _framed_tree_hash(entries: Sequence[tuple[str, str, Path, int]]) -> str:
    digest = hashlib.sha256()
    for relative, entry_type, path, expected_size in entries:
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(entry_type.encode() + b"\0")
        if entry_type == "file":
            content = _read_regular_bytes(path, "tree file")
            if len(content) != expected_size:
                raise _error("tree file changed size while hashing", path)
            digest.update(expected_size.to_bytes(8, "big"))
            digest.update(content)
    return digest.hexdigest()


def _omitted_tree(path: Path, relative: str) -> OmittedTree:
    entries = _tree_entries(path, "omitted build tree")
    files = [entry for entry in entries if entry[1] == "file"]
    return OmittedTree(
        relative_path=relative,
        tree_sha256=_framed_tree_hash(entries),
        file_count=len(files),
        total_bytes=sum(entry[3] for entry in files),
    )


def _inventory_source_tree(
    root: Path,
    label: str,
) -> tuple[
    tuple[tuple[str, str], ...],
    tuple[str, ...],
    tuple[OmittedTree, ...],
]:
    _require_directory(root, label)
    files: list[tuple[str, str]] = []
    directories: list[str] = []
    omitted: list[OmittedTree] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            children = list(os.scandir(directory))
        except OSError as error:
            raise _error(f"cannot scan {label}", directory) from error
        for child in children:
            path = Path(child.path)
            try:
                mode = child.stat(follow_symlinks=False).st_mode
            except OSError as error:
                raise _error(f"cannot inspect {label} entry", path) from error
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                if path.name.endswith("-kompiled"):
                    omitted.append(_omitted_tree(path, relative))
                else:
                    directories.append(relative)
                    pending.append(path)
            elif stat.S_ISREG(mode):
                files.append((relative, _sha256_file(path)))
            else:
                raise _error(f"{label} contains linked or unsupported entry", path)
    return (
        tuple(sorted(files)),
        tuple(sorted(directories)),
        tuple(sorted(omitted, key=lambda item: item.relative_path)),
    )


def _require_int(document: Mapping[str, Any], name: str, label: str) -> int:
    value = document.get(name)
    if isinstance(value, bool) or not isinstance(value, int):
        raise _error(f"{label} field {name} must be an integer")
    return value


def _require_bool(document: Mapping[str, Any], name: str, label: str) -> bool:
    value = document.get(name)
    if not isinstance(value, bool):
        raise _error(f"{label} field {name} must be a boolean")
    return value


def _validate_metrics(
    path: Path,
    *,
    label: str,
    audit: bool = False,
) -> dict[str, Any]:
    metrics = _read_json(path, label)
    for name in ("agent", "model", "effort"):
        if not isinstance(metrics.get(name), str) or not metrics[name]:
            raise _error(f"{label} field {name} must be a non-empty string", path)
    timeout_s = _require_int(metrics, "timeout_s", label)
    start = _require_int(metrics, "start_epoch", label)
    end = _require_int(metrics, "end_epoch", label)
    duration = _require_int(metrics, "duration_s", label)
    exit_code = _require_int(metrics, "exit_code", label)
    peak = _require_int(metrics, "mem_peak_bytes", label)
    timed_out = _require_bool(metrics, "timed_out", label)
    if timeout_s <= 0 or duration < 0 or peak < 0 or end - start != duration:
        raise _error(f"{label} contains invalid runtime values", path)
    if audit:
        for name in ("model_exit_code", "harness_exit_code"):
            if _require_int(metrics, name, label) != 0:
                raise _error(f"complete {label} has nonzero {name}", path)
        if timed_out or exit_code != 0:
            raise _error(f"complete {label} must exit zero without timeout", path)
    return metrics


def _validate_manifest(
    path: Path,
    spec: LegacyRunSpec,
    problem: str,
) -> None:
    manifest = _read_json(path, "legacy input manifest")
    if manifest.get("schema_version") != 1:
        raise _error("legacy input manifest schema_version must be 1", path)
    if manifest.get("config") != spec.run_id:
        raise _error("legacy input manifest config does not match source", path)
    if manifest.get("problem_id") != problem:
        raise _error("legacy input manifest problem_id does not match source", path)
    expected_condition = {
        "name": spec.condition,
        "kit": False,
        "semantics": spec.condition == "semantics",
    }
    if manifest.get("condition") != expected_condition:
        raise _error("legacy input manifest condition is malformed", path)
    inputs = manifest.get("inputs")
    if not isinstance(inputs, dict):
        raise _error("legacy input manifest inputs must be an object", path)
    expected_prompt = "bare.md" if spec.condition == "bare" else "with-semantics.md"
    if inputs.get("instruction_prompt") != expected_prompt:
        raise _error("legacy input manifest instruction prompt is incorrect", path)
    hash_fields = (
        "instruction_prompt_sha256",
        "problem_prompt_sha256",
        "translator_sha256",
        *(("reference_semantics_sha256",) if spec.condition == "semantics" else ()),
    )
    for name in hash_fields:
        if not isinstance(inputs.get(name), str) or _HASH_PATTERN.fullmatch(
            inputs[name]
        ) is None:
            raise _error(f"legacy input manifest {name} is malformed", path)
    if spec.condition == "bare" and "reference_semantics_sha256" in inputs:
        raise _error(
            "bare legacy input manifest unexpectedly records reference semantics",
            path,
        )


def _read_rollout_identity(
    task: Path,
    retained_files: Sequence[tuple[str, str]],
) -> tuple[str, str, str, str]:
    rollout_paths = [
        relative
        for relative, _digest in retained_files
        if relative.startswith("codex-trace/") and relative.endswith(".jsonl")
    ]
    if len(rollout_paths) != 1:
        raise _error(
            f"legacy task must contain exactly one rollout JSONL; found "
            f"{len(rollout_paths)}",
            task / "codex-trace",
        )
    relative = rollout_paths[0]
    rollout = task / relative
    session_records: list[tuple[str, str]] = []
    try:
        lines = _read_regular_bytes(rollout, "legacy rollout").decode().splitlines()
    except UnicodeDecodeError as error:
        raise _error("legacy rollout is not UTF-8", rollout) from error
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise _error(
                f"malformed rollout JSON at line {line_number}",
                rollout,
            ) from error
        if not isinstance(event, dict):
            raise _error(
                f"rollout event at line {line_number} must be an object",
                rollout,
            )
        if event.get("type") != "session_meta":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict):
            raise _error("rollout session_meta payload is malformed", rollout)
        value = payload.get("id")
        try:
            parsed = str(uuid.UUID(value))
        except (AttributeError, TypeError, ValueError) as error:
            raise _error("rollout session UUID is malformed", rollout) from error
        if parsed != value:
            raise _error("rollout session UUID is not canonical", rollout)
        alternate = payload.get("session_id")
        if alternate is not None and alternate != parsed:
            raise _error("rollout session UUID fields disagree", rollout)
        cli_version = payload.get("cli_version")
        if not isinstance(cli_version, str) or not cli_version:
            raise _error("rollout CLI version is missing or malformed", rollout)
        session_records.append((parsed, cli_version))
    if len(session_records) != 1:
        raise _error(
            f"legacy rollout must contain exactly one session_meta; found "
            f"{len(session_records)}",
            rollout,
        )
    try:
        usage = usage_accounting.extract_trace_usage(task / "codex-trace")
    except usage_accounting.UsageAccountingError as error:
        raise _error(f"legacy token evidence is malformed: {error}", rollout) from error
    return (
        session_records[0][0],
        session_records[0][1],
        relative,
        str(usage["status"]),
    )


def _validate_task_workspace(
    task: Path,
    spec: LegacyRunSpec,
    problem: str,
    timed_out: bool,
) -> None:
    for name in _COMMON_WORKSPACE_FILES:
        _require_regular_file(task / name, f"legacy task {name}", nonempty=True)
    _require_regular_file(
        task / "codex-output.log",
        "legacy task codex-output.log",
        nonempty=True,
    )
    _require_directory(task / "codex-trace", "legacy task codex-trace")
    if spec.condition == "bare":
        _require_regular_file(task / "semantic.k", "legacy task semantic.k", nonempty=True)
        _require_regular_file(task / "prove.sh", "legacy task prove.sh", nonempty=True)
    else:
        _require_directory(
            task / "reference-semantics",
            "legacy reference semantics",
        )
        prove_expected = problem not in {
            "151-double-the-difference",
            "162-string-to-md5",
        }
        if prove_expected:
            _require_regular_file(
                task / "prove.sh",
                "legacy task prove.sh",
                nonempty=True,
            )
        elif _path_exists(task / "prove.sh"):
            raise _error("legacy timeout unexpectedly contains prove.sh", task / "prove.sh")
    if timed_out:
        if _path_exists(task / "codex-last.txt"):
            raise _error(
                "legacy timeout unexpectedly contains codex-last.txt",
                task / "codex-last.txt",
            )
    else:
        _require_regular_file(
            task / "codex-last.txt",
            "legacy task codex-last.txt",
            nonempty=True,
        )


def _validate_audit(
    repo: Path,
    spec: LegacyRunSpec,
    problem: str,
) -> tuple[
    str,
    str,
    str,
    tuple[tuple[str, str], ...],
    tuple[str, ...],
]:
    assert spec.audit_run_id is not None
    audit = repo / "audits" / spec.audit_run_id / problem
    files, directories, omitted = _inventory_source_tree(
        audit,
        "legacy audit task",
    )
    if omitted:
        raise _error("legacy audit unexpectedly contains omitted build output", audit)
    for name in _AUDIT_FILES:
        _require_regular_file(audit / name, f"legacy audit {name}", nonempty=True)
    _require_directory(audit / "codex-trace", "legacy audit codex-trace")
    evidence = _require_directory(audit / "evidence", "legacy audit evidence")
    evidence_files = [
        item for item in _tree_entries(evidence, "legacy audit evidence")
        if item[1] == "file" and item[3] > 0
    ]
    if not evidence_files:
        raise _error("legacy audit evidence must contain a non-empty file", evidence)
    audit_input = _read_json(audit / "audit-input.json", "legacy audit input")
    if (
        audit_input.get("config") != spec.audit_run_id
        or audit_input.get("generation_config") != spec.run_id
        or audit_input.get("problem_id") != problem
        or audit_input.get("condition") != spec.condition
    ):
        raise _error("legacy audit input identity is inconsistent", audit / "audit-input.json")
    _validate_metrics(audit / "metrics.json", label="legacy audit metrics", audit=True)
    verdict = _read_json(audit / "verdict.json", "legacy audit verdict")
    if verdict.get("audit_status") != "COMPLETE" or verdict.get("error") is not None:
        raise _error("legacy audit verdict is not complete", audit / "verdict.json")
    verdict_name = verdict.get("verdict")
    legitimacy = verdict.get("legitimacy")
    if (
        not isinstance(verdict_name, str)
        or _AUDIT_VERDICT_PAIRS.get(verdict_name) != legitimacy
    ):
        raise _error("legacy audit verdict/legitimacy pair is invalid", audit / "verdict.json")
    review_lines = _read_text(audit / "REVIEW.md", "legacy audit review").splitlines()
    expected_tail = [
        f"VERDICT: {verdict_name}",
        f"LEGITIMACY: {legitimacy}",
    ]
    if review_lines[-2:] != expected_tail:
        raise _error("legacy audit review terminal verdict markers disagree", audit / "REVIEW.md")
    return (
        f"audits/{spec.audit_run_id}/{problem}",
        verdict_name,
        legitimacy,
        files,
        directories,
    )


def _scan_task(
    repo: Path,
    spec: LegacyRunSpec,
    problem: str,
) -> LegacyTaskPlan:
    task = repo / "runs" / spec.run_id / problem
    retained_files, retained_directories, omitted = _inventory_source_tree(
        task,
        "legacy task",
    )
    metrics = _validate_metrics(task / "metrics.json", label="legacy metrics")
    timed_out = bool(metrics["timed_out"])
    expected_timeout = (spec.run_id, problem) in EXPECTED_TIMEOUTS
    if timed_out != expected_timeout:
        expectation = "timeout" if expected_timeout else "success"
        raise _error(
            f"legacy task classification is unexpected; expected {expectation}",
            task / "metrics.json",
        )
    if timed_out:
        if metrics["exit_code"] != 124 or metrics["duration_s"] != metrics["timeout_s"]:
            raise _error("legacy timeout metrics are inconsistent", task / "metrics.json")
        status = "TIMEOUT"
        result_marker = None
    else:
        if metrics["exit_code"] != 0:
            raise _error("legacy successful task did not exit zero", task / "metrics.json")
        status = "SUCCEEDED"
        try:
            result_marker = stage1_runner.parse_stage1_result(task / "codex-last.txt")
        except (stage1_runner.Stage1RunnerError, OSError) as error:
            raise _error(f"legacy Stage 1 final marker is invalid: {error}", task) from error
        if result_marker != "KPROVE_PASSED":
            raise _error("legacy successful task lacks KPROVE_PASSED marker", task)
    _validate_task_workspace(task, spec, problem, timed_out)

    incomplete = (spec.run_id, problem) in PROVENANCE_INCOMPLETE
    manifest = task / "run-input.json"
    if incomplete:
        if _path_exists(manifest):
            raise _error("expected incomplete-provenance task has run-input.json", manifest)
        input_provenance = "INCOMPLETE"
    else:
        if not _path_exists(manifest):
            raise _error("unexpected missing legacy run-input.json", manifest)
        _validate_manifest(manifest, spec, problem)
        input_provenance = "COMPLETE"

    session_id, cli_version, rollout, usage_status = _read_rollout_identity(
        task,
        retained_files,
    )
    audit_relative: str | None = None
    audit_files: tuple[tuple[str, str], ...] = ()
    audit_directories: tuple[str, ...] = ()
    audit_verdict: str | None = None
    audit_legitimacy: str | None = None
    if spec.audit_run_id is not None and not incomplete:
        (
            audit_relative,
            audit_verdict,
            audit_legitimacy,
            audit_files,
            audit_directories,
        ) = _validate_audit(repo, spec, problem)

    return LegacyTaskPlan(
        run_id=spec.run_id,
        condition=spec.condition,
        problem_id=problem,
        source_relative_path=f"runs/{spec.run_id}/{problem}",
        status=status,
        input_provenance=input_provenance,
        session_id=session_id,
        codex_cli_version=cli_version,
        rollout_relative_path=rollout,
        result_marker=result_marker,
        token_usage_status=usage_status,
        retained_files=retained_files,
        retained_directories=retained_directories,
        omitted=omitted,
        audit_relative_path=audit_relative,
        audit_files=audit_files,
        audit_directories=audit_directories,
        audit_verdict=audit_verdict,
        audit_legitimacy=audit_legitimacy,
    )


def _expected_real_problem_ids(repo: Path) -> tuple[str, ...]:
    return _scan_directories(repo / "data/questions", "trusted question set")


def _validate_specs(specs: Sequence[LegacyRunSpec]) -> tuple[LegacyRunSpec, ...]:
    result = tuple(specs)
    if not result:
        raise _error("legacy source specifications must not be empty")
    run_ids: set[str] = set()
    for spec in result:
        _validate_component(spec.run_id, "legacy run ID")
        if spec.run_id in run_ids:
            raise _error(f"duplicate legacy run specification: {spec.run_id}")
        run_ids.add(spec.run_id)
        if spec.condition not in {"bare", "semantics"}:
            raise _error(f"unsupported legacy condition: {spec.condition}")
        if isinstance(spec.expected_tasks, bool) or spec.expected_tasks <= 0:
            raise _error("expected legacy task count must be positive")
        if spec.audit_run_id is not None:
            _validate_component(spec.audit_run_id, "legacy audit run ID")
        distribution = spec.expected_audit_distribution
        if distribution is not None and (
            not isinstance(distribution, tuple)
            or len(distribution) != 3
            or any(
                isinstance(count, bool)
                or not isinstance(count, int)
                or count < 0
                for count in distribution
            )
        ):
            raise _error(
                "expected audit distribution must be a tuple of three "
                "non-negative integers"
            )
    return result


def scan_legacy_sources(
    repo: Path,
    *,
    _source_specs: Sequence[LegacyRunSpec] | None = None,
) -> MigrationPlan:
    """Scan fixed legacy sources without creating, moving, or deleting anything."""

    repo = _require_directory(Path(repo), "repository")
    default_scope = _source_specs is None
    specs = _validate_specs(SOURCE_SPECS if default_scope else _source_specs)
    expected_real = _expected_real_problem_ids(repo) if default_scope else None
    runs: list[LegacyRunPlan] = []
    for spec in specs:
        source = repo / "runs" / spec.run_id
        problem_ids = _scan_directories(source, "legacy run")
        if len(problem_ids) != spec.expected_tasks:
            raise _error(
                f"legacy run {spec.run_id} has {len(problem_ids)} tasks; "
                f"expected {spec.expected_tasks}",
                source,
            )
        if expected_real is not None and problem_ids != expected_real:
            missing = sorted(set(expected_real) - set(problem_ids))
            extra = sorted(set(problem_ids) - set(expected_real))
            raise _error(
                f"legacy run task set mismatch; missing={missing}, extra={extra}",
                source,
            )

        incomplete_ids = {
            problem
            for run_id, problem in PROVENANCE_INCOMPLETE
            if run_id == spec.run_id and problem in problem_ids
        }
        if spec.audit_run_id is None:
            unexpected_audit = repo / "audits" / spec.run_id
            if _path_exists(unexpected_audit):
                raise _error("semantics legacy source must not have an audit tree", unexpected_audit)
        else:
            audit_root = repo / "audits" / spec.audit_run_id
            audit_ids = _scan_directories(audit_root, "legacy audit run")
            expected_audits = tuple(
                problem for problem in problem_ids if problem not in incomplete_ids
            )
            if audit_ids != expected_audits:
                missing = sorted(set(expected_audits) - set(audit_ids))
                extra = sorted(set(audit_ids) - set(expected_audits))
                raise _error(
                    f"legacy audit task set mismatch; missing={missing}, extra={extra}",
                    audit_root,
                )

        tasks = tuple(_scan_task(repo, spec, problem) for problem in problem_ids)
        counts = {
            "tasks": len(tasks),
            "succeeded": sum(task.status == "SUCCEEDED" for task in tasks),
            "timeout": sum(task.status == "TIMEOUT" for task in tasks),
            "provenance_incomplete": sum(
                task.input_provenance == "INCOMPLETE" for task in tasks
            ),
            "pass": sum(task.audit_verdict == "PASS" for task in tasks),
            "concerns": sum(task.audit_verdict == "CONCERNS" for task in tasks),
            "fail": sum(task.audit_verdict == "FAIL" for task in tasks),
        }
        expected_distribution = spec.expected_audit_distribution
        observed_distribution = (
            counts["pass"],
            counts["concerns"],
            counts["fail"],
        )
        if (
            expected_distribution is not None
            and observed_distribution != expected_distribution
        ):
            raise _error(
                f"legacy audit distribution mismatch for {spec.run_id}; "
                f"expected PASS={expected_distribution[0]}, "
                f"CONCERNS={expected_distribution[1]}, "
                f"FAIL={expected_distribution[2]}; "
                f"observed PASS={observed_distribution[0]}, "
                f"CONCERNS={observed_distribution[1]}, "
                f"FAIL={observed_distribution[2]}",
                repo / "audits" / (spec.audit_run_id or spec.run_id),
            )
        runs.append(
            LegacyRunPlan(
                run_id=spec.run_id,
                condition=spec.condition,
                audit_run_id=spec.audit_run_id,
                counts=MappingProxyType(counts),
                tasks=tasks,
            )
        )
    return MigrationPlan(runs=tuple(runs))


def _task_document(task: LegacyTaskPlan) -> dict[str, Any]:
    return {
        "problem_id": task.problem_id,
        "source_relative_path": task.source_relative_path,
        "status": task.status,
        "input_provenance": task.input_provenance,
        "session_id": task.session_id,
        "codex_cli_version": task.codex_cli_version,
        "rollout_relative_path": task.rollout_relative_path,
        "result_marker": task.result_marker,
        "token_usage_status": task.token_usage_status,
        "retained_files": [
            {"relative_path": relative, "sha256": digest}
            for relative, digest in task.retained_files
        ],
        "retained_directories": list(task.retained_directories),
        "omitted": [
            {
                "relative_path": item.relative_path,
                "tree_sha256": item.tree_sha256,
                "file_count": item.file_count,
                "total_bytes": item.total_bytes,
                "reason": item.reason,
            }
            for item in task.omitted
        ],
        "audit": (
            None
            if task.audit_relative_path is None
            else {
                "relative_path": task.audit_relative_path,
                "verdict": task.audit_verdict,
                "legitimacy": task.audit_legitimacy,
                "retained_files": [
                    {"relative_path": relative, "sha256": digest}
                    for relative, digest in task.audit_files
                ],
                "retained_directories": list(task.audit_directories),
            }
        ),
    }


def plan_document(plan: MigrationPlan) -> dict[str, Any]:
    """Return a deterministic JSON-compatible representation of a scan plan."""

    runs = [
        {
            "run_id": run.run_id,
            "condition": run.condition,
            "audit_run_id": run.audit_run_id,
            "counts": dict(run.counts),
            "tasks": [_task_document(task) for task in run.tasks],
        }
        for run in plan.runs
    ]
    all_tasks = [task for run in plan.runs for task in run.tasks]
    omitted = [item for task in all_tasks for item in task.omitted]
    totals = {
        "runs": len(plan.runs),
        "tasks": len(all_tasks),
        "sessions": len(all_tasks),
        "succeeded": sum(task.status == "SUCCEEDED" for task in all_tasks),
        "timeout": sum(task.status == "TIMEOUT" for task in all_tasks),
        "provenance_incomplete": sum(
            task.input_provenance == "INCOMPLETE" for task in all_tasks
        ),
        "pass": sum(task.audit_verdict == "PASS" for task in all_tasks),
        "concerns": sum(task.audit_verdict == "CONCERNS" for task in all_tasks),
        "fail": sum(task.audit_verdict == "FAIL" for task in all_tasks),
        "omitted_roots": len(omitted),
        "omitted_files": sum(item.file_count for item in omitted),
        "omitted_bytes": sum(item.total_bytes for item in omitted),
    }
    return {"schema_version": 1, "runs": runs, "totals": totals}


def _historical_unknown_policy() -> dict[str, str]:
    return {
        "container_image_id": _UNKNOWN_IMAGE,
        "container_oom_killed": _UNKNOWN_OBSERVATION,
        "original_runner_state": _UNKNOWN_OBSERVATION,
        "scheduler_created_at": _UNKNOWN_OBSERVATION,
        "preflight": _LEGACY_PREFLIGHT,
    }


def _current_importer_commit() -> str:
    module_repo = Path(__file__).resolve().parent.parent
    try:
        result = subprocess.run(
            ["git", "-C", str(module_repo), "rev-parse", "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise _error("cannot determine current legacy importer commit") from error
    commit = result.stdout.strip()
    if re.fullmatch(r"[0-9a-f]{40,64}", commit) is None:
        raise _error("current legacy importer commit is malformed")
    return commit


def _source_inventory_sha256(task: LegacyTaskPlan) -> str:
    document = {
        "algorithm": "LEGACY_MIGRATION_PLAN_INVENTORY_V1",
        "retained_files": [
            {"relative_path": relative, "sha256": digest}
            for relative, digest in task.retained_files
        ],
        "retained_directories": list(task.retained_directories),
        "omitted": [
            {
                "relative_path": item.relative_path,
                "tree_sha256": item.tree_sha256,
                "file_count": item.file_count,
                "total_bytes": item.total_bytes,
                "reason": item.reason,
            }
            for item in task.omitted
        ],
    }
    encoded = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _invocation_evidence_destination(
    task: Path,
    relative: str,
) -> Path:
    invocation = task / "01-k-proof/invocations/001-initial"
    translations = {
        "metrics.json": "legacy-metrics.json",
        "run-input.json": "legacy-run-input.json",
        "codex-output.log": "codex-output.log",
        "codex-last.txt": "codex-last.txt",
    }
    if relative in translations:
        return invocation / translations[relative]
    if relative == "codex-trace" or relative.startswith("codex-trace/"):
        return invocation / relative
    return task / "01-k-proof/workspace" / relative


def _copy_planned_file(
    source: Path,
    destination: Path,
    expected_sha256: str,
    label: str,
) -> None:
    if _sha256_file(source, label) != expected_sha256:
        raise _error(f"{label} changed after migration planning", source)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination, follow_symlinks=False)
    except OSError as error:
        raise _error(f"cannot copy {label}", source) from error
    if _sha256_file(destination, f"copied {label}") != expected_sha256:
        raise _error(f"copied {label} does not preserve source bytes", destination)


def _create_stage_skeleton(task: Path) -> None:
    for stage in pipeline_contract.STAGE_NAMES:
        (task / stage).mkdir(parents=True, exist_ok=False)
    for relative in (
        "01-k-proof/workspace",
        "01-k-proof/invocations/001-initial",
        "02-k-audit/executions",
        "03-lemma-discovery/workspace",
        "03-lemma-discovery/invocations",
        "04-klean-generation/generations",
        "05-lean-proof/workspace",
        "05-lean-proof/invocations",
        "06-lean-audit/executions",
    ):
        (task / relative).mkdir(parents=True, exist_ok=True)


def _copy_instruction_prompt(
    repo: Path,
    invocation: Path,
    legacy_manifest: dict[str, Any],
) -> str:
    inputs = legacy_manifest.get("inputs")
    if not isinstance(inputs, dict):
        raise _error("legacy input manifest inputs must be an object")
    prompt_name = _validate_component(
        inputs.get("instruction_prompt"),
        "legacy instruction prompt",
    )
    prompt_hash = inputs.get("instruction_prompt_sha256")
    if not isinstance(prompt_hash, str) or _HASH_PATTERN.fullmatch(
        prompt_hash
    ) is None:
        raise _error("legacy instruction prompt hash is malformed")
    source = repo / "prompts" / prompt_name
    _copy_planned_file(
        source,
        invocation / "prompt.txt",
        prompt_hash,
        "legacy instruction prompt",
    )
    return prompt_hash


def _task_inputs(
    legacy_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    if legacy_manifest is None:
        return {}
    source = legacy_manifest.get("inputs")
    if not isinstance(source, dict):
        raise _error("legacy input manifest inputs must be an object")
    names = (
        "problem_prompt_sha256",
        "instruction_prompt_sha256",
        "translator_sha256",
        "reference_semantics_sha256",
    )
    return {name: source[name] for name in names if name in source}


def _task_manifest(
    task: LegacyTaskPlan,
    legacy_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    document: dict[str, Any] = {
        "schema_version": pipeline_contract.SCHEMA_VERSION,
        "problem_id": task.problem_id,
        "condition": {
            "name": task.condition,
            "kit": False,
            "semantics": task.condition == "semantics",
        },
        "current_stage": "01-k-proof",
        "inputs": _task_inputs(legacy_manifest),
        "input_provenance": task.input_provenance,
    }
    if task.input_provenance == "INCOMPLETE":
        document["pipeline_block"] = _PIPELINE_BLOCK
    return document


def _run_manifest(
    run: LegacyRunPlan,
    imported_at: str,
    importer_commit: str,
) -> dict[str, Any]:
    parsed = pipeline_contract.parse_codex_config(run.run_id)
    return {
        "schema_version": pipeline_contract.SCHEMA_VERSION,
        "run_id": run.run_id,
        "created_at": imported_at,
        "created_at_source": "MIGRATION_TIME",
        "config": run.run_id,
        "model": parsed.model,
        "effort": parsed.effort,
        "condition": {
            "name": run.condition,
            "kit": False,
            "semantics": run.condition == "semantics",
        },
        "timeouts": {
            "k_initial_s": 3600,
            "k_total_s": 7200,
            "lemma_initial_s": 1200,
            "lemma_total_s": 1200,
            "lean_initial_s": 3600,
            "lean_total_s": 7200,
        },
        "tasks": [task.problem_id for task in run.tasks],
        "import_tooling": {
            "current_codex_cli_version": pipeline_contract.CODEX_CLI_VERSION,
            "pipeline_schema_version": pipeline_contract.SCHEMA_VERSION,
        },
        "legacy_import": True,
        "imported_at": imported_at,
        "source_layout_version": _SOURCE_LAYOUT_VERSION,
        "importer_commit": importer_commit,
        "historical_unknown_policy": _historical_unknown_policy(),
    }


def _normalized_metrics(
    legacy_metrics: Mapping[str, Any],
    task: LegacyTaskPlan,
) -> dict[str, Any]:
    return {
        "exit_code": legacy_metrics["exit_code"],
        "duration_s": legacy_metrics["duration_s"],
        "timeout_marker": legacy_metrics["timed_out"],
        "oom_killed": _UNKNOWN_OBSERVATION,
        "status": task.status,
        "allocation_s": legacy_metrics["timeout_s"],
        "cumulative_duration_s": legacy_metrics["duration_s"],
        "image_id": _UNKNOWN_IMAGE,
        "preflight": _LEGACY_PREFLIGHT,
        "legacy_import": True,
    }


def _retained_manifest(
    staged_task: Path,
    task: LegacyTaskPlan,
) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for relative, digest in task.retained_files:
        destination = _invocation_evidence_destination(staged_task, relative)
        records.append(
            {
                "original_relative_path": relative,
                "destination_relative_path": destination.relative_to(
                    staged_task
                ).as_posix(),
                "sha256": digest,
            }
        )
    return records


def _audit_import_manifest(
    task: LegacyTaskPlan,
) -> dict[str, Any] | None:
    if task.audit_relative_path is None:
        return None
    return {
        "stage": "02-k-audit",
        "execution": "001",
        "original_path": task.audit_relative_path,
        "verdict": task.audit_verdict,
        "legitimacy": task.audit_legitimacy,
        "retained_files": [
            {"relative_path": relative, "sha256": digest}
            for relative, digest in task.audit_files
        ],
        "retained_directories": list(task.audit_directories),
    }


def _invocation_manifest(
    task: LegacyTaskPlan,
    legacy_metrics: Mapping[str, Any],
    prompt_sha256: str | None,
    source_tree_sha256: str,
    workspace_sha256: str,
    outputs: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": pipeline_contract.SCHEMA_VERSION,
        "stage": "01-k-proof",
        "name": "001-initial",
        "kind": "initial",
        "status": task.status,
        "allocation_s": legacy_metrics["timeout_s"],
        "session_id": task.session_id,
        "prompt_sha256": (
            prompt_sha256
            if prompt_sha256 is not None
            else _UNKNOWN_OBSERVATION
        ),
        "inputs": {
            "source_tree_sha256": source_tree_sha256,
            "workspace_sha256": workspace_sha256,
        },
        "outputs": dict(outputs),
        "exit_code": legacy_metrics["exit_code"],
        "duration_s": legacy_metrics["duration_s"],
        "cumulative_duration_s": legacy_metrics["duration_s"],
        "timeout_marker": legacy_metrics["timed_out"],
        "resumable": True,
        "legacy_import": True,
        "codex_cli_version": task.codex_cli_version,
        "image_id": _UNKNOWN_IMAGE,
        "oom_killed": _UNKNOWN_OBSERVATION,
        "preflight": _LEGACY_PREFLIGHT,
        "result_marker": task.result_marker,
        "source_tree_sha256": source_tree_sha256,
        "retained_workspace_sha256": workspace_sha256,
        "expected_absences": (
            ["codex-last.txt", "result.json"]
            if task.status == "TIMEOUT"
            else []
        ),
    }


def _result_manifest(
    task: LegacyTaskPlan,
    legacy_metrics: Mapping[str, Any],
    outputs: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": pipeline_contract.SCHEMA_VERSION,
        "stage": "01-k-proof",
        "status": "SUCCEEDED",
        "invocation": "001-initial",
        "session_id": task.session_id,
        "resumable": True,
        "cumulative_duration_s": legacy_metrics["duration_s"],
        "outputs": dict(outputs),
        "legacy_import": True,
        "result_marker": task.result_marker,
    }


def _session_manifest(
    staged_state: Path,
    task: LegacyTaskPlan,
) -> dict[str, Any]:
    home = staged_state / "codex-home"
    home_stat = home.stat()
    return {
        "schema_version": pipeline_contract.SCHEMA_VERSION,
        "session_id": task.session_id,
        "codex_home_relative": "codex-home",
        "codex_home_device": home_stat.st_dev,
        "codex_home_inode": home_stat.st_ino,
        "source": "01-k-proof/001-initial",
    }


def _ledger_payload(
    task: LegacyTaskPlan,
    imported_at: str,
) -> dict[str, Any]:
    return {
        "event": "legacy_invocation_imported",
        "stage": "01-k-proof",
        "invocation": "001-initial",
        "status": task.status,
        "source_relative_path": task.source_relative_path,
        "imported_at": imported_at,
    }


def _migration_manifest(
    staged_task: Path,
    task: LegacyTaskPlan,
    imported_at: str,
    importer_commit: str,
    source_tree_sha256: str,
    workspace_sha256: str,
    session: Mapping[str, Any],
) -> dict[str, Any]:
    document: dict[str, Any] = {
        "schema_version": 1,
        "run_id": task.run_id,
        "problem_id": task.problem_id,
        "condition": {
            "name": task.condition,
            "kit": False,
            "semantics": task.condition == "semantics",
        },
        "stage": "01-k-proof",
        "invocation": "001-initial",
        "legacy_import": True,
        "imported_at": imported_at,
        "importer_commit": importer_commit,
        "source_layout_version": _SOURCE_LAYOUT_VERSION,
        "original_path": task.source_relative_path,
        "status": task.status,
        "input_provenance": task.input_provenance,
        "session_id": task.session_id,
        "codex_cli_version": task.codex_cli_version,
        "rollout_relative_path": task.rollout_relative_path,
        "source_tree_hash_algorithm": (
            "LEGACY_MIGRATION_PLAN_INVENTORY_V1"
        ),
        "source_tree_sha256": source_tree_sha256,
        "retained_workspace_sha256": workspace_sha256,
        "retained_files": _retained_manifest(staged_task, task),
        "retained_directories": list(task.retained_directories),
        "audit_import": _audit_import_manifest(task),
        "omitted": [
            {
                "relative_path": item.relative_path,
                "tree_sha256": item.tree_sha256,
                "file_count": item.file_count,
                "total_bytes": item.total_bytes,
                "reason": item.reason,
            }
            for item in task.omitted
        ],
        "unknown_fields": _historical_unknown_policy(),
        "session_state": {
            "source": session["source"],
            "codex_home_relative": session["codex_home_relative"],
        },
    }
    if task.input_provenance == "INCOMPLETE":
        document["pipeline_block"] = _PIPELINE_BLOCK
    return document


def _stage_audit(
    repo: Path,
    staged_task: Path,
    staged_state: Path,
    task_plan: LegacyTaskPlan,
) -> None:
    if task_plan.audit_relative_path is None:
        return
    if "usage.json" in dict(task_plan.audit_files):
        raise _error("legacy audit unexpectedly contains normalized usage")

    source = repo / task_plan.audit_relative_path
    execution = staged_task / "02-k-audit/executions/001"
    execution.mkdir()
    for relative in task_plan.audit_directories:
        (execution / relative).mkdir(parents=True, exist_ok=True)
    for relative, digest in task_plan.audit_files:
        _copy_planned_file(
            source / relative,
            execution / relative,
            digest,
            f"legacy audit file {relative}",
        )

    usage_accounting.write_trace_usage(
        execution / "codex-trace",
        execution / "usage.json",
    )
    selected = pipeline_contract.select_stage_output_at(
        staged_task,
        staged_state,
        "02-k-audit",
        "001",
    )
    if selected.get("status") != task_plan.audit_verdict:
        raise _error("selected audit status changed from legacy verdict")


def _stage_task(
    repo: Path,
    run: LegacyRunPlan,
    task_plan: LegacyTaskPlan,
    staged_task: Path,
    staged_state: Path,
    imported_at: str,
    importer_commit: str,
) -> None:
    _create_stage_skeleton(staged_task)
    staged_state.mkdir(mode=0o700, parents=True)
    codex_home = staged_state / "codex-home"
    codex_home.mkdir(mode=0o700)
    ledger = staged_state / "stage-ledger.jsonl"
    ledger.touch(mode=0o600)

    source_task = repo / task_plan.source_relative_path
    for relative in task_plan.retained_directories:
        _invocation_evidence_destination(staged_task, relative).mkdir(
            parents=True,
            exist_ok=True,
        )
    for relative, digest in task_plan.retained_files:
        _copy_planned_file(
            source_task / relative,
            _invocation_evidence_destination(staged_task, relative),
            digest,
            f"legacy retained file {relative}",
        )

    invocation = staged_task / "01-k-proof/invocations/001-initial"
    legacy_manifest: dict[str, Any] | None = None
    prompt_sha256: str | None = None
    if task_plan.input_provenance == "COMPLETE":
        legacy_manifest = _read_json(
            invocation / "legacy-run-input.json",
            "copied legacy input manifest",
        )
        prompt_sha256 = _copy_instruction_prompt(
            repo,
            invocation,
            legacy_manifest,
        )

    pipeline_contract.write_json_atomic(
        staged_task / "task.json",
        _task_manifest(task_plan, legacy_manifest),
    )

    rollout_source = source_task / task_plan.rollout_relative_path
    rollout_digest = dict(task_plan.retained_files)[
        task_plan.rollout_relative_path
    ]
    rollout_relative = task_plan.rollout_relative_path.removeprefix(
        "codex-trace/"
    )
    state_rollout = codex_home / "sessions" / rollout_relative
    _copy_planned_file(
        rollout_source,
        state_rollout,
        rollout_digest,
        "legacy session rollout",
    )
    session = pipeline_contract.write_session_state(
        staged_state,
        task_plan.session_id,
        "01-k-proof/001-initial",
    )

    trace = invocation / "codex-trace"
    usage_accounting.write_trace_usage(
        trace,
        invocation / "usage.json",
    )
    legacy_metrics = _read_json(
        invocation / "legacy-metrics.json",
        "copied legacy metrics",
    )
    metrics = _normalized_metrics(legacy_metrics, task_plan)
    pipeline_contract.write_json_atomic(
        invocation / "metrics.json",
        metrics,
    )

    workspace = staged_task / "01-k-proof/workspace"
    source_tree_sha256 = _source_inventory_sha256(task_plan)
    workspace_sha256 = pipeline_contract.sha256_tree(workspace)
    outputs = pipeline_contract._invocation_output_hashes(
        invocation,
        workspace,
    )
    pipeline_contract.write_json_atomic(
        invocation / "invocation.json",
        _invocation_manifest(
            task_plan,
            legacy_metrics,
            prompt_sha256,
            source_tree_sha256,
            workspace_sha256,
            outputs,
        ),
    )

    stage = staged_task / "01-k-proof"
    if task_plan.status == "SUCCEEDED":
        pipeline_contract.write_json_atomic(
            stage / "result.json",
            _result_manifest(task_plan, legacy_metrics, outputs),
        )

    pipeline_contract._append_ledger(
        staged_state,
        _ledger_payload(task_plan, imported_at),
    )

    _stage_audit(
        repo,
        staged_task,
        staged_state,
        task_plan,
    )

    pipeline_contract.write_json_atomic(
        staged_task / "migration.json",
        _migration_manifest(
            staged_task,
            task_plan,
            imported_at,
            importer_commit,
            source_tree_sha256,
            workspace_sha256,
            session,
        ),
    )


def _empty_usage_counters() -> dict[str, int]:
    return dict.fromkeys(usage_accounting.TOKEN_FIELDS, 0)


def _add_usage_counters(
    destination: dict[str, int],
    value: object,
    label: str,
) -> None:
    if not isinstance(value, dict):
        raise _error(f"{label} must be an object")
    for name in usage_accounting.TOKEN_FIELDS:
        counter = value.get(name)
        if (
            isinstance(counter, bool)
            or not isinstance(counter, int)
            or counter < 0
        ):
            raise _error(f"{label} field {name} is invalid")
        destination[name] += counter


def _validate_run_usage_summary(
    staged_run: Path,
    run: LegacyRunPlan,
) -> None:
    summary = _read_json(
        staged_run / "usage-summary.json",
        "staged run usage summary",
    )
    stages = (
        "01-k-proof",
        "02-k-audit",
        "03-lemma-discovery",
        "05-lean-proof",
        "06-lean-audit",
    )
    totals = _empty_usage_counters()
    stage_totals = {
        stage: _empty_usage_counters()
        for stage in stages
    }
    task_totals = {
        task.problem_id: _empty_usage_counters()
        for task in run.tasks
    }
    stage_seconds: dict[str, int | float] = {
        stage: 0 for stage in stages
    }
    task_seconds: dict[str, int | float] = {
        task.problem_id: 0 for task in run.tasks
    }
    agent_seconds: int | float = 0

    for task in run.tasks:
        staged_task = staged_run / "tasks" / task.problem_id
        executions = [
            (
                "01-k-proof",
                staged_task / "01-k-proof/invocations/001-initial",
                "legacy-metrics.json",
            )
        ]
        if task.audit_relative_path is not None:
            executions.append(
                (
                    "02-k-audit",
                    staged_task / "02-k-audit/executions/001",
                    "metrics.json",
                )
            )
        for stage, execution, metrics_name in executions:
            usage = _read_json(
                execution / "usage.json",
                "staged usage summary source",
            )
            if usage.get("status") == "COMPLETE":
                delta = usage.get("invocation_delta")
                _add_usage_counters(totals, delta, "usage delta")
                _add_usage_counters(
                    stage_totals[stage],
                    delta,
                    "usage stage delta",
                )
                _add_usage_counters(
                    task_totals[task.problem_id],
                    delta,
                    "usage task delta",
                )
            elif usage.get("status") != "MISSING":
                raise _error("staged usage status is invalid")

            metrics = _read_json(
                execution / metrics_name,
                "staged runtime summary source",
            )
            duration = metrics.get("duration_s")
            if (
                isinstance(duration, bool)
                or not isinstance(duration, (int, float))
                or duration < 0
            ):
                raise _error("staged runtime duration is invalid")
            agent_seconds += duration
            stage_seconds[stage] += duration
            task_seconds[task.problem_id] += duration

    expected_fields = {
        "totals": totals,
        "stage_subtotals": stage_totals,
        "task_subtotals": task_totals,
    }
    for name, expected in expected_fields.items():
        if summary.get(name) != expected:
            raise _error(
                f"staged run usage summary {name} is invalid",
                staged_run / "usage-summary.json",
            )
    runtime = summary.get("runtime")
    if (
        not isinstance(runtime, dict)
        or runtime.get("agent_seconds") != agent_seconds
        or runtime.get("stage_agent_seconds") != stage_seconds
        or runtime.get("task_agent_seconds") != task_seconds
    ):
        raise _error(
            "staged run usage summary runtime totals are invalid",
            staged_run / "usage-summary.json",
        )


def stage_migration(
    repo: Path,
    plan: MigrationPlan,
    transaction_id: str,
) -> StagedMigration:
    """Stage compact structured runs and resumable state under hidden roots."""

    repo = _require_directory(Path(repo), "repository")
    transaction_id = _validate_component(transaction_id, "transaction ID")
    runs = _require_directory(repo / "runs", "runs root")
    state_parent = repo / "runner-state"
    if _path_exists(state_parent):
        _require_directory(state_parent, "runner-state root")
    else:
        state_parent.mkdir(mode=0o700)
    state_parent.chmod(0o700)

    runs_root = runs / f".legacy-migration-{transaction_id}"
    state_root = state_parent / f".legacy-migration-{transaction_id}"
    if _path_exists(runs_root) or _path_exists(state_root):
        raise _error("legacy migration staging root already exists")
    imported_at = datetime.now(timezone.utc).isoformat()
    importer_commit = _current_importer_commit()
    staged = StagedMigration(
        repo=repo,
        transaction_id=transaction_id,
        runs_root=runs_root,
        state_root=state_root,
        imported_at=imported_at,
        importer_commit=importer_commit,
    )

    try:
        runs_root.mkdir(mode=0o700)
        state_root.mkdir(mode=0o700)
        for run in plan.runs:
            staged_run = runs_root / run.run_id
            staged_state = state_root / run.run_id
            staged_run.mkdir(mode=0o700)
            (staged_run / "tasks").mkdir()
            staged_state.mkdir(mode=0o700)
            for task_plan in run.tasks:
                _stage_task(
                    repo,
                    run,
                    task_plan,
                    staged_run / "tasks" / task_plan.problem_id,
                    staged_state / task_plan.problem_id,
                    imported_at,
                    importer_commit,
                )
            pipeline_contract.write_json_atomic(
                staged_run / "run.json",
                _run_manifest(run, imported_at, importer_commit),
            )
            (staged_run / "task-list.txt").write_text(
                "".join(f"{task.problem_id}\n" for task in run.tasks)
            )
            usage_accounting.write_run_summary(staged_run)
        validate_staged_migration(staged, plan)
    except BaseException:
        if runs_root.exists():
            shutil.rmtree(runs_root)
        if state_root.exists():
            shutil.rmtree(state_root)
        raise
    return staged


def _validate_stage_skeleton(task: Path) -> None:
    for stage in pipeline_contract.STAGE_NAMES:
        pipeline_contract._require_direct_directory(task, stage, stage)
    for relative in (
        "01-k-proof/workspace",
        "01-k-proof/invocations",
        "01-k-proof/invocations/001-initial",
        "02-k-audit/executions",
        "03-lemma-discovery/workspace",
        "03-lemma-discovery/invocations",
        "04-klean-generation/generations",
        "05-lean-proof/workspace",
        "05-lean-proof/invocations",
        "06-lean-audit/executions",
    ):
        pipeline_contract.require_real_directory(
            task / relative,
            f"staged {relative}",
        )


def _validate_audit_stage(
    staged_task: Path,
    task_plan: LegacyTaskPlan,
) -> None:
    stage = staged_task / "02-k-audit"
    executions = stage / "executions"
    expected_audit = task_plan.audit_relative_path is not None
    execution_names = _scan_directories(
        executions,
        "staged Stage 2 executions",
    )
    if not expected_audit:
        if execution_names:
            raise _error("task without a legacy audit gained Stage 2 evidence")
        if _path_exists(stage / "selected.json"):
            raise _error("task without a legacy audit gained Stage 2 selection")
        return
    if execution_names != ("001",):
        raise _error("imported Stage 2 must contain exactly execution 001")

    execution = executions / "001"
    entries = _tree_entries(execution, "staged legacy audit")
    actual_directories = tuple(
        relative
        for relative, kind, _path, _size in entries
        if kind == "directory"
    )
    if actual_directories != task_plan.audit_directories:
        raise _error("staged legacy audit directories changed")
    actual_files = {
        relative: path
        for relative, kind, path, _size in entries
        if kind == "file"
    }
    expected_files = dict(task_plan.audit_files)
    if set(actual_files) != set(expected_files) | {"usage.json"}:
        raise _error("staged legacy audit file set changed")
    for relative, expected_hash in expected_files.items():
        if (
            _sha256_file(
                actual_files[relative],
                f"staged legacy audit file {relative}",
            )
            != expected_hash
        ):
            raise _error(
                "staged legacy audit file hash mismatch",
                actual_files[relative],
            )

    usage = _read_json(
        execution / "usage.json",
        "staged legacy audit usage",
    )
    expected_usage = usage_accounting.extract_trace_usage(
        execution / "codex-trace"
    )
    if usage != expected_usage:
        raise _error("staged legacy audit usage does not match retained trace")

    selected = _read_json(
        stage / "selected.json",
        "staged Stage 2 selection",
    )
    selected_at = selected.get("selected_at")
    try:
        parsed_selected_at = datetime.fromisoformat(selected_at)
    except (TypeError, ValueError) as error:
        raise _error("staged Stage 2 selection timestamp is invalid") from error
    expected_selection = {
        "schema_version": pipeline_contract.SCHEMA_VERSION,
        "stage": "02-k-audit",
        "relative_path": "executions/001",
        "artifact_sha256": pipeline_contract.sha256_tree(execution),
        "status": task_plan.audit_verdict,
        "selected_at": selected_at,
        "replaces": None,
    }
    if (
        selected != expected_selection
        or parsed_selected_at.tzinfo is None
        or pipeline_contract._selection_status(
            "02-k-audit",
            execution,
        )
        != task_plan.audit_verdict
    ):
        raise _error("staged Stage 2 selection is invalid")


def _validate_task_stage(
    staged_task: Path,
    staged_state: Path,
    task_plan: LegacyTaskPlan,
    imported_at: str,
    importer_commit: str,
) -> None:
    _validate_stage_skeleton(staged_task)
    _validate_audit_stage(staged_task, task_plan)
    for relative, kind, path, _size in _tree_entries(
        staged_task,
        "staged task",
    ):
        if kind == "directory" and Path(relative).name.endswith("-kompiled"):
            raise _error("staged task contains omitted K build tree", path)

    invocation = staged_task / "01-k-proof/invocations/001-initial"
    workspace = staged_task / "01-k-proof/workspace"
    for relative, expected in task_plan.retained_files:
        destination = _invocation_evidence_destination(
            staged_task,
            relative,
        )
        if _sha256_file(destination, "staged retained file") != expected:
            raise _error("staged retained file hash mismatch", destination)

    source_tree_sha256 = _source_inventory_sha256(task_plan)
    workspace_sha256 = pipeline_contract.sha256_tree(workspace)
    legacy_manifest: dict[str, Any] | None = None
    prompt_sha256: str | None = None
    if task_plan.input_provenance == "COMPLETE":
        legacy_manifest = _read_json(
            invocation / "legacy-run-input.json",
            "staged legacy input manifest",
        )
        inputs = legacy_manifest.get("inputs")
        prompt_sha256 = (
            inputs.get("instruction_prompt_sha256")
            if isinstance(inputs, dict)
            else None
        )
    outputs = pipeline_contract._invocation_output_hashes(
        invocation,
        workspace,
    )
    legacy_metrics = _read_json(
        invocation / "legacy-metrics.json",
        "staged legacy metrics",
    )
    metrics = _read_json(invocation / "metrics.json", "normalized metrics")
    if metrics != _normalized_metrics(legacy_metrics, task_plan):
        raise _error("normalized legacy metrics are invalid")
    invocation_document = _read_json(
        invocation / "invocation.json",
        "staged invocation manifest",
    )
    expected_invocation = _invocation_manifest(
        task_plan,
        legacy_metrics,
        prompt_sha256,
        source_tree_sha256,
        workspace_sha256,
        outputs,
    )
    if invocation_document != expected_invocation:
        raise _error("staged invocation manifest is invalid")

    usage = _read_json(invocation / "usage.json", "staged usage")
    expected_usage = usage_accounting.extract_trace_usage(
        invocation / "codex-trace"
    )
    if usage != expected_usage:
        raise _error("staged usage does not match retained trace")
    if str(usage.get("status")) != task_plan.token_usage_status:
        raise _error("staged usage status changed from migration plan")

    if pipeline_contract.extract_session_uuid(
        invocation / "codex-trace"
    ) != task_plan.session_id:
        raise _error("staged invocation trace session is invalid")
    session = _read_json(
        staged_state / "session.json",
        "staged session state",
    )
    if session != _session_manifest(staged_state, task_plan):
        raise _error("staged session state is invalid")
    if pipeline_contract._read_session_state(staged_state) != session:
        raise _error("staged session state binding is invalid")
    rollout_relative = task_plan.rollout_relative_path.removeprefix(
        "codex-trace/"
    )
    state_rollout = (
        staged_state / "codex-home/sessions" / rollout_relative
    )
    invocation_rollout = invocation / task_plan.rollout_relative_path
    expected_rollout_hash = dict(task_plan.retained_files)[
        task_plan.rollout_relative_path
    ]
    if (
        _sha256_file(state_rollout, "staged state rollout")
        != expected_rollout_hash
        or _sha256_file(invocation_rollout, "staged invocation rollout")
        != expected_rollout_hash
    ):
        raise _error("staged session rollout hash is invalid")
    if (
        state_rollout.stat().st_dev == invocation_rollout.stat().st_dev
        and state_rollout.stat().st_ino == invocation_rollout.stat().st_ino
    ):
        raise _error("runner-state rollout must be a separate copy")

    stage_result = staged_task / "01-k-proof/result.json"
    if task_plan.status == "SUCCEEDED":
        if stage1_runner.parse_stage1_result(
            invocation / "codex-last.txt"
        ) != task_plan.result_marker:
            raise _error("staged Stage 1 result marker changed")
        result = _read_json(stage_result, "staged Stage 1 result")
        if result != _result_manifest(task_plan, legacy_metrics, outputs):
            raise _error("staged Stage 1 result is invalid")
    else:
        if _path_exists(stage_result):
            raise _error("legacy timeout must not have a Stage 1 result")
        if _path_exists(invocation / "codex-last.txt"):
            raise _error("legacy timeout unexpectedly has final output")
        if invocation_document.get("expected_absences") != [
            "codex-last.txt",
            "result.json",
        ]:
            raise _error("legacy timeout expected absences are invalid")

    task_manifest = _read_json(
        staged_task / "task.json",
        "staged task manifest",
    )
    expected_block = (
        _PIPELINE_BLOCK
        if task_plan.input_provenance == "INCOMPLETE"
        else None
    )
    if task_manifest != _task_manifest(task_plan, legacy_manifest):
        raise _error("staged task manifest is invalid")
    if pipeline_contract.task_pipeline_block(staged_task) != expected_block:
        raise _error("staged task manifest block is invalid")
    if task_plan.input_provenance == "COMPLETE":
        if _sha256_file(
            invocation / "prompt.txt",
            "staged prompt",
        ) != prompt_sha256:
            raise _error("staged instruction prompt hash is invalid")
    else:
        if _path_exists(invocation / "legacy-run-input.json"):
            raise _error("incomplete task gained a legacy input manifest")
        if _path_exists(invocation / "prompt.txt"):
            raise _error("incomplete task gained an instruction prompt")

    ledger_lines = [
        line
        for line in _read_text(
            staged_state / "stage-ledger.jsonl",
            "staged stage ledger",
        ).splitlines()
        if line.strip()
    ]
    try:
        ledger_events = [json.loads(line) for line in ledger_lines]
    except json.JSONDecodeError as error:
        raise _error("staged stage ledger is malformed") from error
    expected_count = 2 if task_plan.audit_relative_path is not None else 1
    if len(ledger_events) != expected_count:
        raise _error("staged stage ledger event count is invalid")
    import_event = ledger_events[0]
    recorded_at = (
        import_event.get("recorded_at")
        if isinstance(import_event, dict)
        else None
    )
    try:
        parsed_recorded_at = datetime.fromisoformat(recorded_at)
    except (TypeError, ValueError) as error:
        raise _error("staged stage ledger timestamp is invalid") from error
    expected_ledger = {
        "sequence": 1,
        "recorded_at": recorded_at,
        **_ledger_payload(task_plan, imported_at),
    }
    if (
        import_event != expected_ledger
        or type(import_event.get("sequence")) is not int
        or parsed_recorded_at.tzinfo is None
    ):
        raise _error("staged stage ledger import event is invalid")
    if task_plan.audit_relative_path is not None:
        selection_event = ledger_events[1]
        selected_at = (
            selection_event.get("recorded_at")
            if isinstance(selection_event, dict)
            else None
        )
        try:
            parsed_selected_at = datetime.fromisoformat(selected_at)
        except (TypeError, ValueError) as error:
            raise _error("staged Stage 2 ledger timestamp is invalid") from error
        expected_selection_event = {
            "sequence": 2,
            "recorded_at": selected_at,
            "event": "stage_output_selected",
            "stage": "02-k-audit",
            "relative_path": "executions/001",
            "status": task_plan.audit_verdict,
        }
        if (
            selection_event != expected_selection_event
            or type(selection_event.get("sequence")) is not int
            or parsed_selected_at.tzinfo is None
        ):
            raise _error("staged Stage 2 ledger event is invalid")

    migration = _read_json(
        staged_task / "migration.json",
        "staged migration manifest",
    )
    expected_migration = _migration_manifest(
        staged_task,
        task_plan,
        imported_at,
        importer_commit,
        source_tree_sha256,
        workspace_sha256,
        session,
    )
    if migration != expected_migration:
        raise _error("staged migration manifest is invalid")


def validate_staged_migration(
    staged: StagedMigration,
    plan: MigrationPlan,
    *,
    _published: bool = False,
) -> dict[str, Any]:
    """Validate hidden Stage 1 and state paths without resolving final runs."""

    repo = _require_directory(Path(staged.repo), "repository")
    expected_runs_root = (
        repo / "runs" / f".legacy-migration-{staged.transaction_id}"
    )
    expected_state_root = (
        repo
        / "runner-state"
        / f".legacy-migration-{staged.transaction_id}"
    )
    runs_root = _require_directory(staged.runs_root, "staged runs root")
    state_root = _require_directory(staged.state_root, "staged state root")
    if not _published and (
        runs_root != expected_runs_root or state_root != expected_state_root
    ):
        raise _error("staged migration roots do not match transaction")

    tasks = [task for run in plan.runs for task in run.tasks]
    for run in plan.runs:
        staged_run = runs_root / run.run_id
        staged_run_state = state_root / run.run_id
        _require_directory(staged_run, "staged run")
        _require_directory(staged_run_state, "staged run state")
        if stat.S_IMODE(staged_run.stat().st_mode) != 0o700:
            raise _error("staged run mode must be 0700", staged_run)
        manifest = _read_json(staged_run / "run.json", "staged run manifest")
        expected_manifest = _run_manifest(
            run,
            staged.imported_at,
            staged.importer_commit,
        )
        if manifest != expected_manifest:
            raise _error("staged run manifest is invalid", staged_run / "run.json")
        expected_task_list = "".join(
            f"{task.problem_id}\n" for task in run.tasks
        )
        if _read_text(
            staged_run / "task-list.txt",
            "staged task list",
        ) != expected_task_list:
            raise _error("staged task list is invalid")
        for task_plan in run.tasks:
            _validate_task_stage(
                staged_run / "tasks" / task_plan.problem_id,
                staged_run_state / task_plan.problem_id,
                task_plan,
                staged.imported_at,
                staged.importer_commit,
            )
        _validate_run_usage_summary(staged_run, run)

    return {
        "runs": len(plan.runs),
        "tasks": len(tasks),
        "succeeded": sum(task.status == "SUCCEEDED" for task in tasks),
        "timeout": sum(task.status == "TIMEOUT" for task in tasks),
        "blocked": sum(
            task.input_provenance == "INCOMPLETE" for task in tasks
        ),
        "pass": sum(task.audit_verdict == "PASS" for task in tasks),
        "concerns": sum(
            task.audit_verdict == "CONCERNS" for task in tasks
        ),
        "fail": sum(task.audit_verdict == "FAIL" for task in tasks),
        "eligible": sum(
            task.audit_verdict in {"PASS", "CONCERNS"} for task in tasks
        ),
    }


def _journal_path(repo: Path) -> Path:
    return repo / "runner-state" / _JOURNAL_NAME


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_journal(repo: Path, journal: dict[str, Any]) -> None:
    path = _journal_path(repo)
    parent = _require_directory(path.parent, "runner-state root")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(journal, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(parent)
    except OSError as error:
        raise _error("cannot persist migration transaction journal", path) from error
    finally:
        if temporary.exists():
            temporary.unlink()


def _remove_journal(repo: Path) -> None:
    path = _journal_path(repo)
    try:
        path.unlink()
        _fsync_directory(path.parent)
    except FileNotFoundError:
        return
    except OSError as error:
        raise _error("cannot remove migration transaction journal", path) from error


def _read_journal(repo: Path) -> dict[str, Any] | None:
    path = _journal_path(repo)
    if not _path_exists(path):
        return None
    document = _read_json(path, "migration transaction journal")
    if (
        document.get("schema_version") != _JOURNAL_SCHEMA_VERSION
        or not isinstance(document.get("transaction_id"), str)
        or not isinstance(document.get("phase"), str)
        or not isinstance(document.get("paths"), dict)
        or not isinstance(document.get("renames"), list)
    ):
        raise _error("migration transaction journal is malformed", path)
    return document


@contextmanager
def migration_lock(repo: Path) -> Iterator[None]:
    """Hold the exclusive, no-follow migration lock for one whole operation."""

    repo = _require_directory(Path(repo), "repository")
    repository_flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        repository_descriptor = os.open(repo, repository_flags)
        fcntl.flock(repository_descriptor, fcntl.LOCK_EX)
    except OSError as error:
        raise _error("cannot lock repository for migration", repo) from error
    state_root = repo / "runner-state"
    created_state_root = False
    if _path_exists(state_root):
        _require_directory(state_root, "runner-state root")
    else:
        try:
            state_root.mkdir(mode=0o700)
            _fsync_directory(repo)
            created_state_root = True
        except OSError as error:
            os.close(repository_descriptor)
            raise _error("cannot create runner-state root", state_root) from error
    lock_path = state_root / _LOCK_NAME
    created_lock = not _path_exists(lock_path)
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as error:
        fcntl.flock(repository_descriptor, fcntl.LOCK_UN)
        os.close(repository_descriptor)
        raise _error("cannot open migration lock", lock_path) from error
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise _error("migration lock must be a regular file", lock_path)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
        except OSError as error:
            raise _error("cannot hold migration lock", lock_path) from error
        yield
    finally:
        try:
            if created_lock and _path_exists(lock_path):
                lock_path.unlink()
                _fsync_directory(state_root)
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)
            if created_state_root:
                try:
                    state_root.rmdir()
                    _fsync_directory(repo)
                except OSError:
                    pass
            fcntl.flock(repository_descriptor, fcntl.LOCK_UN)
            os.close(repository_descriptor)


def _docker_bind_mount_sources() -> tuple[Path, ...]:
    try:
        listed = subprocess.run(
            ["docker", "ps", "-q"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except OSError as error:
        raise LegacyMigrationError(
            f"Docker inspection unavailable: {error}"
        ) from error
    if listed.returncode != 0:
        detail = listed.stderr.strip() or f"exit {listed.returncode}"
        raise LegacyMigrationError(f"Docker inspection unavailable: {detail}")
    container_ids = listed.stdout.split()
    if not container_ids:
        return ()
    inspected = subprocess.run(
        ["docker", "inspect", *container_ids],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if inspected.returncode != 0:
        detail = inspected.stderr.strip() or f"exit {inspected.returncode}"
        raise LegacyMigrationError(f"Docker inspection unavailable: {detail}")
    try:
        documents = json.loads(inspected.stdout)
    except json.JSONDecodeError as error:
        raise LegacyMigrationError(
            "Docker inspection returned malformed JSON"
        ) from error
    if not isinstance(documents, list):
        raise LegacyMigrationError("Docker inspection returned malformed JSON")
    sources: list[Path] = []
    for document in documents:
        mounts = document.get("Mounts") if isinstance(document, dict) else None
        if not isinstance(mounts, list):
            raise LegacyMigrationError(
                "Docker inspection returned malformed mount data"
            )
        for mount in mounts:
            if not isinstance(mount, dict) or mount.get("Type") != "bind":
                continue
            source = mount.get("Source")
            if not isinstance(source, str) or not source:
                raise LegacyMigrationError(
                    "Docker inspection returned malformed bind source"
                )
            sources.append(Path(source))
    return tuple(sources)


def _pipeline_processes() -> tuple[tuple[int, tuple[str, ...]], ...]:
    processes: list[tuple[int, tuple[str, ...]]] = []
    current_pid = os.getpid()
    try:
        entries = tuple(Path("/proc").iterdir())
    except OSError as error:
        raise LegacyMigrationError(f"cannot scan /proc: {error}") from error
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
            raise LegacyMigrationError(
                f"cannot inspect process command line: {entry / 'cmdline'}"
            ) from error
        arguments = tuple(
            item.decode("utf-8", errors="surrogateescape")
            for item in raw.split(b"\0")
            if item
        )
        command = "\0".join(arguments)
        if arguments and any(
            marker in command for marker in _PIPELINE_LAUNCHER_MARKERS
        ):
            processes.append((pid, arguments))
    return tuple(processes)


def _absolute_lexical(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _is_within(path: Path, root: Path) -> bool:
    path = _absolute_lexical(path)
    root = _absolute_lexical(root)
    try:
        return os.path.commonpath((path, root)) == os.fspath(root)
    except ValueError:
        return False


def _activity_targets(repo: Path, plan: MigrationPlan) -> tuple[Path, ...]:
    targets: list[Path] = []
    for run in plan.runs:
        targets.extend(
            (
                repo / "runs" / run.run_id,
                repo / "runner-state" / run.run_id,
            )
        )
        if run.audit_run_id is not None:
            targets.append(repo / "audits" / run.audit_run_id)
    return tuple(targets)


def source_activity_report(
    repo: Path,
    plan: MigrationPlan,
    *,
    require_docker: bool,
) -> dict[str, Any]:
    """Inspect containers and launchers without mutating migration sources."""

    repo = _require_directory(Path(repo), "repository")
    targets = _activity_targets(repo, plan)
    try:
        mounts = _docker_bind_mount_sources()
    except LegacyMigrationError as error:
        if require_docker:
            raise
        docker: dict[str, Any] = {
            "status": "UNAVAILABLE",
            "error": str(error),
            "bind_mounts": [],
        }
        mounts = ()
    else:
        docker = {
            "status": "AVAILABLE",
            "error": None,
            "bind_mounts": [str(path) for path in mounts],
        }
    active_mounts = tuple(
        mount
        for mount in mounts
        if any(_is_within(mount, target) for target in targets)
    )
    if active_mounts:
        raise _error(
            "active Docker container bind mount intersects migration source",
            active_mounts[0],
        )

    processes = _pipeline_processes()
    run_ids = tuple(run.run_id for run in plan.runs)
    active_processes = tuple(
        (pid, arguments)
        for pid, arguments in processes
        if any(
            run_id in argument
            for argument in arguments
            for run_id in run_ids
        )
    )
    if active_processes:
        pid, arguments = active_processes[0]
        raise LegacyMigrationError(
            "active pipeline process names a migration run: "
            f"pid={pid} cmdline={arguments!r}"
        )
    return {
        "docker": docker,
        "processes": {
            "status": "AVAILABLE",
            "active": [],
        },
    }


def assert_sources_idle(repo: Path, plan: MigrationPlan) -> None:
    """Reject apply unless Docker and process probes prove both runs idle."""

    source_activity_report(repo, plan, require_docker=True)


def assert_publication_destinations_available(
    repo: Path,
    plan: MigrationPlan,
) -> None:
    """Reject conflicting final state or unjournaled transaction roots."""

    repo = _require_directory(Path(repo), "repository")
    for run in plan.runs:
        destination = repo / "runner-state" / run.run_id
        if _path_exists(destination):
            raise _error(
                "structured runner-state destination already exists",
                destination,
            )
    roots = (repo / "runs", repo / "runner-state")
    for root in roots:
        if not _path_exists(root):
            continue
        _require_directory(root, "migration parent")
        try:
            entries = tuple(root.iterdir())
        except OSError as error:
            raise _error("cannot scan migration parent", root) from error
        for entry in entries:
            if (
                entry.name.startswith(".legacy-migration-")
                and entry.name not in {_LOCK_NAME, _JOURNAL_NAME}
            ):
                raise _error(
                    "unjournaled legacy migration path requires manual attention",
                    entry,
                )


def _scope_run_ids(plan: MigrationPlan) -> tuple[str, ...]:
    run_ids = tuple(run.run_id for run in plan.runs)
    expected = tuple(spec.run_id for spec in SOURCE_SPECS)
    if run_ids != expected:
        raise LegacyMigrationError(
            f"migration plan must target the fixed run scope: {expected!r}"
        )
    return run_ids


def _begin_transaction(
    repo: Path,
    staged: StagedMigration,
    plan: MigrationPlan,
) -> dict[str, Any]:
    repo = _require_directory(Path(repo), "repository")
    if _read_journal(repo) is not None:
        raise _error(
            "migration transaction journal already exists",
            _journal_path(repo),
        )
    run_ids = _scope_run_ids(plan)
    if staged.repo != repo:
        raise LegacyMigrationError("staged migration repository does not match")
    paths: dict[str, Any] = {"runs": [], "audit": None}
    for run_id in run_ids:
        source = repo / "runs" / run_id
        staging = staged.runs_root / run_id
        state_staging = staged.state_root / run_id
        paths["runs"].append(
            {
                "run_id": run_id,
                "source": str(source),
                "staging": str(staging),
                "quarantine": str(
                    repo
                    / "runs"
                    / (
                        f".legacy-migration-{staged.transaction_id}"
                        f"-quarantine-{run_id}"
                    )
                ),
                "final": str(source),
                "state_staging": str(state_staging),
                "state_final": str(repo / "runner-state" / run_id),
                "source_sha256": pipeline_contract.sha256_tree(source),
                "staged_sha256": pipeline_contract.sha256_tree(staging),
                "state_sha256": pipeline_contract.sha256_tree(state_staging),
            }
        )
    audit_runs = tuple(
        run.audit_run_id for run in plan.runs if run.audit_run_id is not None
    )
    if len(audit_runs) != 1:
        raise LegacyMigrationError(
            "fixed migration scope must contain exactly one audit source"
        )
    audit_source = repo / "audits" / audit_runs[0]
    paths["audit"] = {
        "source": str(audit_source),
        "quarantine": str(
            repo
            / "audits"
            / (
                f".legacy-migration-{staged.transaction_id}"
                f"-quarantine-{audit_runs[0]}"
            )
        ),
        "source_sha256": pipeline_contract.sha256_tree(audit_source),
    }
    journal: dict[str, Any] = {
        "schema_version": _JOURNAL_SCHEMA_VERSION,
        "transaction_id": staged.transaction_id,
        "phase": "STAGED",
        "imported_at": staged.imported_at,
        "importer_commit": staged.importer_commit,
        "staging_roots": [
            str(staged.runs_root),
            str(staged.state_root),
        ],
        "paths": paths,
        "active_rename": None,
        "renames": [],
        "rollback": {"attempted": False, "succeeded": None},
        "manual_attention_paths": [],
    }
    _write_journal(repo, journal)
    return journal


def _set_phase(
    repo: Path,
    journal: dict[str, Any],
    phase: str,
) -> None:
    journal["phase"] = phase
    _write_journal(repo, journal)


def _transaction_rename(
    repo: Path,
    journal: dict[str, Any],
    source: Path,
    destination: Path,
    kind: str,
) -> None:
    if not _path_exists(source):
        raise _error("transaction rename source is missing", source)
    if _path_exists(destination):
        raise _error("transaction rename destination already exists", destination)
    record = {
        "source": str(source),
        "destination": str(destination),
        "kind": kind,
    }
    journal["active_rename"] = record
    _write_journal(repo, journal)
    try:
        source.rename(destination)
        journal["renames"].append(record)
        _fsync_directory(source.parent)
        if destination.parent != source.parent:
            _fsync_directory(destination.parent)
    except OSError as error:
        raise _error("migration transaction rename failed", source) from error
    journal["active_rename"] = None
    _write_journal(repo, journal)


def _publication_boundary(_name: str) -> None:
    """Test seam for failures after irreversible-looking rename groups."""


def _cleanup_staging_roots(journal: Mapping[str, Any]) -> None:
    roots = journal.get("staging_roots")
    if not isinstance(roots, list):
        return
    for value in roots:
        if not isinstance(value, str):
            continue
        path = Path(value)
        if _path_exists(path):
            shutil.rmtree(path)
            _fsync_directory(path.parent)


def _validate_restored_sources(journal: Mapping[str, Any]) -> None:
    paths = journal["paths"]
    for run in paths["runs"]:
        source = Path(run["source"])
        expected = run["source_sha256"]
        if pipeline_contract.sha256_tree(source) != expected:
            raise _error("rolled-back run source hash changed", source)
    audit = paths["audit"]
    source = Path(audit["source"])
    if pipeline_contract.sha256_tree(source) != audit["source_sha256"]:
        raise _error("rolled-back audit source hash changed", source)


def _rollback_transaction(
    repo: Path,
    journal: dict[str, Any],
) -> None:
    journal["rollback"] = {"attempted": True, "succeeded": None}
    _write_journal(repo, journal)
    manual: list[str] = []
    current_paths: list[str] = []
    try:
        for record in reversed(journal["renames"]):
            source = Path(record["source"])
            destination = Path(record["destination"])
            current_paths = [str(source), str(destination)]
            source_exists = _path_exists(source)
            destination_exists = _path_exists(destination)
            if destination_exists and not source_exists:
                destination.rename(source)
                _fsync_directory(source.parent)
                if destination.parent != source.parent:
                    _fsync_directory(destination.parent)
            elif source_exists and not destination_exists:
                continue
            else:
                manual.extend((str(source), str(destination)))
                raise LegacyMigrationError(
                    "rollback path state is ambiguous: "
                    f"{source}; {destination}"
                )
        _validate_restored_sources(journal)
        _cleanup_staging_roots(journal)
    except BaseException as error:
        if not manual:
            manual = current_paths
        journal["phase"] = "ROLLBACK_FAILED"
        journal["rollback"] = {"attempted": True, "succeeded": False}
        journal["manual_attention_paths"] = sorted(set(manual))
        _write_journal(repo, journal)
        raise LegacyMigrationRollbackError(
            "legacy migration rollback failed; manual attention required at: "
            + ", ".join(journal["manual_attention_paths"])
        ) from error
    journal["active_rename"] = None
    journal["phase"] = "ROLLBACK_SUCCEEDED"
    journal["rollback"] = {"attempted": True, "succeeded": True}
    journal["manual_attention_paths"] = []
    _write_journal(repo, journal)


def _published_staged(
    repo: Path,
    journal: Mapping[str, Any],
) -> StagedMigration:
    return StagedMigration(
        repo=repo,
        transaction_id=str(journal["transaction_id"]),
        runs_root=repo / "runs",
        state_root=repo / "runner-state",
        imported_at=str(journal["imported_at"]),
        importer_commit=str(journal["importer_commit"]),
    )


def _validate_published_hashes(journal: Mapping[str, Any]) -> None:
    for run in journal["paths"]["runs"]:
        final = Path(run["final"])
        state_final = Path(run["state_final"])
        if pipeline_contract.sha256_tree(final) != run["staged_sha256"]:
            raise _error("published run hash changed", final)
        if pipeline_contract.sha256_tree(state_final) != run["state_sha256"]:
            raise _error("published runner state hash changed", state_final)


def _remove_validated_quarantines(
    repo: Path,
    journal: dict[str, Any],
) -> None:
    quarantine_paths = [
        Path(run["quarantine"]) for run in journal["paths"]["runs"]
    ]
    quarantine_paths.append(Path(journal["paths"]["audit"]["quarantine"]))
    for path in quarantine_paths:
        if _path_exists(path):
            _require_directory(path, "migration quarantine")
            shutil.rmtree(path)
            _fsync_directory(path.parent)
    _cleanup_staging_roots(journal)
    _set_phase(repo, journal, "COMPLETE")
    _remove_journal(repo)


def publish_migration(
    repo: Path,
    staged: StagedMigration,
    plan: MigrationPlan,
) -> None:
    """Publish both fixed runs and their state as one rollback-safe transaction."""

    repo = _require_directory(Path(repo), "repository")
    validate_staged_migration(staged, plan)
    journal = _begin_transaction(repo, staged, plan)
    try:
        for run in journal["paths"]["runs"]:
            _transaction_rename(
                repo,
                journal,
                Path(run["source"]),
                Path(run["quarantine"]),
                "run-quarantine",
            )
        _set_phase(repo, journal, "RUNS_QUARANTINED")
        _publication_boundary("after-run-quarantine")

        audit = journal["paths"]["audit"]
        _transaction_rename(
            repo,
            journal,
            Path(audit["source"]),
            Path(audit["quarantine"]),
            "audit-quarantine",
        )
        _set_phase(repo, journal, "AUDIT_QUARANTINED")
        _publication_boundary("after-audit-quarantine")

        for run in journal["paths"]["runs"]:
            _transaction_rename(
                repo,
                journal,
                Path(run["staging"]),
                Path(run["final"]),
                "run-publish",
            )
        _set_phase(repo, journal, "RUNS_PUBLISHED")
        _publication_boundary("after-run-publish")

        for run in journal["paths"]["runs"]:
            _transaction_rename(
                repo,
                journal,
                Path(run["state_staging"]),
                Path(run["state_final"]),
                "state-publish",
            )
        _set_phase(repo, journal, "STATE_PUBLISHED")
        _publication_boundary("after-state-publish")

        validate_staged_migration(
            _published_staged(repo, journal),
            plan,
            _published=True,
        )
        _validate_published_hashes(journal)
        _publication_boundary("after-post-publish-validation")
        _set_phase(repo, journal, "VALIDATED")
    except BaseException:
        _rollback_transaction(repo, journal)
        raise
    _remove_validated_quarantines(repo, journal)


def _reconcile_active_rename(
    repo: Path,
    journal: dict[str, Any],
) -> None:
    active = journal.get("active_rename")
    if active is None:
        return
    if not isinstance(active, dict):
        raise _error(
            "migration transaction active rename is malformed",
            _journal_path(repo),
        )
    source = Path(str(active.get("source")))
    destination = Path(str(active.get("destination")))
    source_exists = _path_exists(source)
    destination_exists = _path_exists(destination)
    if source_exists and not destination_exists:
        journal["active_rename"] = None
    elif destination_exists and not source_exists:
        if active not in journal["renames"]:
            journal["renames"].append(active)
        journal["active_rename"] = None
    else:
        journal["manual_attention_paths"] = [
            str(source),
            str(destination),
        ]
        _write_journal(repo, journal)
        raise LegacyMigrationRollbackError(
            "migration recovery is ambiguous; manual attention required at: "
            f"{source}, {destination}"
        )
    _write_journal(repo, journal)


def recover_transaction(repo: Path) -> None:
    """Recover or finish the single journaled migration transaction."""

    repo = _require_directory(Path(repo), "repository")
    journal = _read_journal(repo)
    if journal is None:
        return
    _reconcile_active_rename(repo, journal)
    phase = journal["phase"]
    if phase == "COMPLETE":
        _remove_journal(repo)
        return
    if phase == "VALIDATED":
        _validate_published_hashes(journal)
        _remove_validated_quarantines(repo, journal)
        return
    if phase == "ROLLBACK_FAILED":
        paths = journal.get("manual_attention_paths", [])
        raise LegacyMigrationRollbackError(
            "migration rollback previously failed; manual attention required at: "
            + ", ".join(str(path) for path in paths)
        )
    if phase == "ROLLBACK_SUCCEEDED":
        _validate_restored_sources(journal)
        _cleanup_staging_roots(journal)
        _remove_journal(repo)
        return
    quarantine_renamed = any(
        record.get("kind") in {"run-quarantine", "audit-quarantine"}
        for record in journal["renames"]
        if isinstance(record, dict)
    )
    if not quarantine_renamed:
        _cleanup_staging_roots(journal)
        _remove_journal(repo)
        return
    _rollback_transaction(repo, journal)
    _remove_journal(repo)
