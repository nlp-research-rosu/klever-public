#!/usr/bin/env python3
"""Contracts and filesystem layout for resumable benchmark pipeline runs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import uuid
from pathlib import Path
from typing import Any, Callable, Iterable


SCHEMA_VERSION = 3
CODEX_CLI_VERSION = "0.144.6"
K_VERSION = "7.1.293"
K_BASE_IMAGE = (
    "runtimeverificationinc/kframework-k:ubuntu-jammy-7.1.293@"
    "sha256:f3f64ab72bd7b560082d50e4c6c23e107025cf217ca62ab73700104fc45de09a"
)
K_COMMIT = "ff15baac9e66426612ec45ff912af7f14965b64a"
PYK_VERSION = "7.1.293"
PYK_PROJECT = "pyk@runtimeverification/k"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.22.0"
LEAN_COMMIT = "ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05"
FROZEN_TOOLCHAIN_LOCK = {
    "codex_cli_version": CODEX_CLI_VERSION,
    "k_base_image": K_BASE_IMAGE,
    "k_version": K_VERSION,
    "lean_commit": LEAN_COMMIT,
    "lean_toolchain": LEAN_TOOLCHAIN,
    "pyk_version": PYK_VERSION,
    "pyk_project": PYK_PROJECT,
    "runtimeverification_k_commit": K_COMMIT,
}
STAGE_NAMES = (
    "01-k-proof",
    "02-k-audit",
    "03-lemma-discovery",
    "04-klean-generation",
    "05-lean-proof",
    "06-lean-audit",
)
_INVOCATION_STAGES = {
    "01-k-proof": ("k_initial_s", "k_total_s"),
    "03-lemma-discovery": ("lemma_initial_s", "lemma_total_s"),
    "05-lean-proof": ("lean_initial_s", "lean_total_s"),
}

_CONDITIONS = (
    ("kit-semantics", True, True, "kit-semantics.md"),
    ("semantics", False, True, "with-semantics.md"),
    ("kit", True, False, "kit-bare.md"),
    ("bare", False, False, "bare.md"),
)
_CODEX_CONFIG = re.compile(r"^codex-(?P<model>.+)-xhigh-(?P<condition>.+)$")
_HASH_CHUNK_SIZE = 1024 * 1024
_BWRAP_NAMESPACE_DENIAL = (
    b"bwrap: No permissions to create a new namespace"
)


class PipelineContractError(RuntimeError):
    """Raised when a pipeline path, manifest, or state violates the contract."""


def _usage_accounting_module():
    try:
        from tools import usage_accounting
    except ImportError as error:
        raise PipelineContractError(
            "usage accounting support is unavailable"
        ) from error
    return usage_accounting


@dataclass(frozen=True)
class Condition:
    name: str
    kit: bool
    semantics: bool
    prompt_file: str


@dataclass(frozen=True)
class CodexConfig:
    name: str
    model: str
    effort: str
    condition: Condition


@dataclass(frozen=True)
class Invocation:
    stage: str
    name: str
    kind: str
    path: Path
    allocation_s: int
    session_id: str | None


def validate_safe_component(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise PipelineContractError(f"{label} must be a string path component")
    path = Path(value)
    if (
        not value
        or value in {".", ".."}
        or value.startswith(".")
        or path.is_absolute()
        or len(path.parts) != 1
        or "/" in value
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise PipelineContractError(
            f"{label} must be one safe nonhidden path component: {value!r}"
        )
    return value


def parse_codex_config(config: str) -> CodexConfig:
    validate_safe_component(config, "config")
    match = _CODEX_CONFIG.fullmatch(config)
    if match is None:
        raise PipelineContractError(f"invalid Codex config grammar: {config}")
    condition_name = match.group("condition")
    condition = next(
        (
            Condition(name, kit, semantics, prompt)
            for name, kit, semantics, prompt in _CONDITIONS
            if name == condition_name
        ),
        None,
    )
    if condition is None:
        raise PipelineContractError(f"unsupported benchmark condition: {condition_name}")
    return CodexConfig(
        name=config,
        model=match.group("model"),
        effort="xhigh",
        condition=condition,
    )


def _lstat(path: Path, label: str) -> os.stat_result:
    try:
        return path.lstat()
    except OSError as error:
        raise PipelineContractError(f"{label} is missing: {path}") from error


def require_real_directory(path: Path, label: str) -> Path:
    if not stat.S_ISDIR(_lstat(path, label).st_mode):
        raise PipelineContractError(f"{label} must be a real directory: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as error:
        raise PipelineContractError(f"{label} cannot be resolved: {path}") from error


def require_regular_file(path: Path, label: str) -> Path:
    if not stat.S_ISREG(_lstat(path, label).st_mode):
        raise PipelineContractError(f"{label} must be a real regular file: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as error:
        raise PipelineContractError(f"{label} cannot be resolved: {path}") from error


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(_HASH_CHUNK_SIZE), b""):
                digest.update(chunk)
    except OSError as error:
        raise PipelineContractError(f"cannot hash file {path}: {error}") from error
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    root = require_real_directory(root, "tree root")
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        try:
            children = list(os.scandir(directory))
        except OSError as error:
            raise PipelineContractError(f"cannot scan tree {directory}: {error}") from error
        for child in children:
            path = Path(child.path)
            try:
                mode = child.stat(follow_symlinks=False).st_mode
            except OSError as error:
                raise PipelineContractError(
                    f"cannot inspect tree entry {path}: {error}"
                ) from error
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise PipelineContractError(
                    f"tree contains linked or unsupported entry: {path}"
                )
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            try:
                size = path.stat(follow_symlinks=False).st_size
                digest.update(size.to_bytes(8, "big"))
                with path.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(_HASH_CHUNK_SIZE), b""):
                        digest.update(chunk)
            except OSError as error:
                raise PipelineContractError(
                    f"cannot hash tree file {path}: {error}"
                ) from error
    return digest.hexdigest()


def write_json_atomic(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _copy_file_atomic_no_clobber(source: Path, destination: Path) -> None:
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        dir=destination.parent,
    )
    os.close(file_descriptor)
    temporary = Path(temporary_name)
    published_identity: tuple[int, int] | None = None

    def remove_published_destination() -> None:
        if published_identity is None:
            return
        try:
            destination_stat = destination.lstat()
        except FileNotFoundError:
            return
        if (
            stat.S_ISREG(destination_stat.st_mode)
            and (destination_stat.st_dev, destination_stat.st_ino)
            == published_identity
        ):
            try:
                destination.unlink()
            except OSError as error:
                raise PipelineContractError(
                    "cannot clean up incomplete runtime metrics publication"
                ) from error

    try:
        shutil.copy2(source, temporary)
        with temporary.open("rb") as stream:
            os.fsync(stream.fileno())
        temporary_stat = temporary.stat()
        published_identity = (temporary_stat.st_dev, temporary_stat.st_ino)
        try:
            os.link(temporary, destination)
        except FileExistsError as error:
            raise PipelineContractError(
                "runtime metrics already exist"
            ) from error
        try:
            temporary.unlink()
        except OSError as error:
            remove_published_destination()
            raise PipelineContractError(
                f"cannot finalize runtime metrics publication: {error}"
            ) from error
    except PipelineContractError:
        remove_published_destination()
        raise
    except OSError as error:
        remove_published_destination()
        raise PipelineContractError(
            f"cannot preserve runtime metrics: {error}"
        ) from error
    except BaseException:
        remove_published_destination()
        raise
    finally:
        try:
            temporary.unlink()
        except OSError:
            pass
        except BaseException:
            remove_published_destination()
            raise


def _copy_file_atomic_replace(source: Path, destination: Path) -> None:
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        dir=destination.parent,
    )
    os.close(file_descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copy2(source, temporary)
        with temporary.open("rb") as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except OSError as error:
        raise PipelineContractError(
            f"cannot restore runtime metrics: {error}"
        ) from error
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _read_regular_json(path: Path, label: str) -> dict[str, Any]:
    regular = require_regular_file(path, label)
    try:
        document = json.loads(regular.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PipelineContractError(f"{label} is malformed: {path}: {error}") from error
    if not isinstance(document, dict):
        raise PipelineContractError(f"{label} must be a JSON object: {path}")
    return document


def task_pipeline_block(task: Path) -> str | None:
    manifest = _read_regular_json(task / "task.json", "task manifest")
    block = manifest.get("pipeline_block")
    if block is None:
        return None
    if block == "INPUT_PROVENANCE_INCOMPLETE":
        if manifest.get("input_provenance") != "INCOMPLETE":
            raise PipelineContractError(
                "pipeline block lacks incomplete provenance"
            )
        return block
    if block == "SESSION_STATE_UNRECOVERABLE":
        provenance = manifest.get("session_provenance")
        allowed_reasons = {
            "SESSION_STATE_MISSING",
            "SESSION_STATE_MALFORMED",
            "SESSION_ID_MISMATCH",
        }
        if (
            not isinstance(provenance, dict)
            or provenance.get("status") != "UNRECOVERABLE"
            or provenance.get("reason") not in allowed_reasons
        ):
            raise PipelineContractError(
                "session-state pipeline block lacks explicit "
                "unrecoverable provenance"
            )
        return block
    raise PipelineContractError(
        f"unknown task pipeline block: {block!r}"
    )


def require_task_unblocked(task: Path, stage: str) -> None:
    block = task_pipeline_block(task)
    if block is not None:
        raise PipelineContractError(f"{stage} blocked by {block}")


def _ensure_state_root(repo: Path) -> Path:
    root = repo / "runner-state"
    try:
        mode = root.lstat().st_mode
    except FileNotFoundError:
        root.mkdir(mode=0o700)
    except OSError as error:
        raise PipelineContractError(f"runner-state root cannot be inspected: {root}") from error
    else:
        if not stat.S_ISDIR(mode):
            raise PipelineContractError(
                f"runner-state root must be a real directory: {root}"
            )
        root.chmod(0o700)
    return root.resolve(strict=True)


def _prevalidate_inputs(
    repo: Path, config: CodexConfig, problem_ids: Iterable[str]
) -> list[dict[str, Any]]:
    validated: list[dict[str, Any]] = []
    seen: set[str] = set()
    translator = require_regular_file(repo / "tools/py2mpy.py", "translator")
    instruction = require_regular_file(
        repo / "prompts" / config.condition.prompt_file,
        "instruction prompt",
    )
    semantics = None
    if config.condition.semantics:
        semantics = require_real_directory(
            repo / "data/reference/src", "reference semantics"
        )
        sha256_tree(semantics)
    for problem_id in problem_ids:
        problem_id = validate_safe_component(problem_id, "problem ID")
        if problem_id in seen:
            raise PipelineContractError(f"duplicate problem ID: {problem_id}")
        seen.add(problem_id)
        prompt = require_regular_file(
            repo / "data/questions" / problem_id / "prompt.py",
            f"{problem_id} prompt",
        )
        validated.append(
            {
                "problem_id": problem_id,
                "prompt": prompt,
                "prompt_sha256": sha256_file(prompt),
                "translator": translator,
                "translator_sha256": sha256_file(translator),
                "instruction_sha256": sha256_file(instruction),
                "semantics": semantics,
                "semantics_sha256": (
                    sha256_tree(semantics) if semantics is not None else None
                ),
            }
        )
    if not validated:
        raise PipelineContractError("at least one problem ID is required")
    return validated


def _create_task(
    run_staging: Path,
    state_staging: Path,
    config: CodexConfig,
    input_document: dict[str, Any],
) -> None:
    problem_id = input_document["problem_id"]
    task = run_staging / "tasks" / problem_id
    for stage in STAGE_NAMES:
        (task / stage).mkdir(parents=True, exist_ok=False)
    (task / "01-k-proof/workspace").mkdir()
    (task / "01-k-proof/invocations").mkdir()
    (task / "02-k-audit/executions").mkdir()
    (task / "03-lemma-discovery/workspace").mkdir()
    (task / "03-lemma-discovery/invocations").mkdir()
    (task / "04-klean-generation/generations").mkdir()
    (task / "05-lean-proof/workspace").mkdir()
    (task / "05-lean-proof/invocations").mkdir()
    (task / "06-lean-audit/executions").mkdir()

    workspace = task / "01-k-proof/workspace"
    shutil.copy2(input_document["prompt"], workspace / "prompt.py")
    shutil.copy2(input_document["translator"], workspace / "py2mpy.py")
    if input_document["semantics"] is not None:
        shutil.copytree(
            input_document["semantics"], workspace / "reference-semantics"
        )

    task_manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "problem_id": problem_id,
        "condition": {
            "name": config.condition.name,
            "kit": config.condition.kit,
            "semantics": config.condition.semantics,
        },
        "current_stage": "01-k-proof",
        "inputs": {
            "problem_prompt_sha256": input_document["prompt_sha256"],
            "instruction_prompt_sha256": input_document["instruction_sha256"],
            "translator_sha256": input_document["translator_sha256"],
        },
    }
    if input_document["semantics_sha256"] is not None:
        task_manifest["inputs"]["reference_semantics_sha256"] = input_document[
            "semantics_sha256"
        ]
    write_json_atomic(task / "task.json", task_manifest)

    state = state_staging / problem_id
    state.mkdir(mode=0o700)
    (state / "codex-home").mkdir(mode=0o700)
    (state / "stage-ledger.jsonl").touch(mode=0o600)


def create_run(
    repo: Path,
    *,
    run_id: str,
    config: str,
    problem_ids: Iterable[str],
) -> Path:
    repo = require_real_directory(Path(repo), "repository")
    run_id = validate_safe_component(run_id, "run ID")
    parsed = parse_codex_config(config)
    inputs = _prevalidate_inputs(repo, parsed, list(problem_ids))
    toolchain_lock_path = require_regular_file(
        repo / "data/klean-toolchain.lock.json",
        "frozen toolchain lock",
    )
    toolchain_lock = _read_regular_json(
        toolchain_lock_path, "frozen toolchain lock"
    )
    if toolchain_lock != FROZEN_TOOLCHAIN_LOCK:
        raise PipelineContractError(
            "frozen toolchain lock differs from the canonical "
            "Codex 0.144.6 / K 7.1.293 / Klean 7.1.293 / Lean 4.22.0 stack"
        )

    runs_root = require_real_directory(repo / "runs", "runs root")
    state_root = _ensure_state_root(repo)
    destination = runs_root / run_id
    state_destination = state_root / run_id
    if destination.exists() or destination.is_symlink():
        raise PipelineContractError(f"run already exists: {destination}")
    if state_destination.exists() or state_destination.is_symlink():
        raise PipelineContractError(
            f"runner state already exists for run: {state_destination}"
        )

    run_staging = Path(tempfile.mkdtemp(prefix=f".{run_id}.", dir=runs_root))
    state_staging = Path(tempfile.mkdtemp(prefix=f".{run_id}.", dir=state_root))
    state_staging.chmod(0o700)
    try:
        (run_staging / "tasks").mkdir()
        for input_document in inputs:
            _create_task(run_staging, state_staging, parsed, input_document)

        run_manifest: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "config": parsed.name,
            "model": parsed.model,
            "effort": parsed.effort,
            "condition": {
                "name": parsed.condition.name,
                "kit": parsed.condition.kit,
                "semantics": parsed.condition.semantics,
            },
            "timeouts": {
                "k_initial_s": 3600,
                "k_total_s": 7200,
                "lemma_initial_s": 1200,
                "lemma_total_s": 1200,
                "lean_initial_s": 3600,
                "lean_total_s": 7200,
            },
            "tasks": [document["problem_id"] for document in inputs],
            "runtime": {
                "codex_cli_version": CODEX_CLI_VERSION,
                "k_version": K_VERSION,
                "runtimeverification_k_commit": K_COMMIT,
                "pyk_version": PYK_VERSION,
                "lean_toolchain": LEAN_TOOLCHAIN,
                "klean_toolchain_lock_sha256": sha256_file(
                    toolchain_lock_path
                ),
            },
        }
        if parsed.condition.kit:
            lock = _read_regular_json(
                repo / "data/kit-skills.lock.json", "Kit bundle lock"
            )
            try:
                run_manifest["kit"] = {
                    "commit": lock["commit"],
                    "skills_tree": lock["skills_tree"],
                }
            except KeyError as error:
                raise PipelineContractError(
                    "Kit bundle lock is missing commit or skills_tree"
                ) from error
        write_json_atomic(run_staging / "run.json", run_manifest)
        (run_staging / "task-list.txt").write_text(
            "".join(f"{document['problem_id']}\n" for document in inputs)
        )

        run_staging.rename(destination)
        state_staging.rename(state_destination)
    except BaseException:
        if run_staging.exists():
            shutil.rmtree(run_staging)
        if state_staging.exists():
            shutil.rmtree(state_staging)
        if destination.exists() and not state_destination.exists():
            shutil.rmtree(destination)
        raise
    return destination.resolve(strict=True)


def _require_direct_directory(parent: Path, name: str, label: str) -> Path:
    parent = require_real_directory(parent, f"parent of {label}")
    child = require_real_directory(parent / name, label)
    if child.parent != parent:
        raise PipelineContractError(
            f"{label} must be a direct real child of {parent}: {name!r}"
        )
    return child


def _validate_kit_provenance(
    value: object, label: str
) -> dict[str, str]:
    if not isinstance(value, dict):
        raise PipelineContractError(f"{label} Kit provenance is malformed")
    commit = value.get("commit")
    skills_tree = value.get("skills_tree")
    if (
        not isinstance(commit, str)
        or not commit
        or not isinstance(skills_tree, str)
        or not skills_tree
    ):
        raise PipelineContractError(f"{label} Kit provenance is malformed")
    return {"commit": commit, "skills_tree": skills_tree}


def _resolve_task_state(
    repo: Path,
    run_id: str,
    problem_id: str,
    *,
    require_current_kit: bool = False,
) -> tuple[Path, Path, dict[str, Any]]:
    repo = require_real_directory(Path(repo), "repository")
    run_id = validate_safe_component(run_id, "run ID")
    problem_id = validate_safe_component(problem_id, "problem ID")
    runs = require_real_directory(repo / "runs", "runs root")
    run = _require_direct_directory(runs, run_id, "run")
    tasks = require_real_directory(run / "tasks", "tasks root")
    task = _require_direct_directory(tasks, problem_id, "task")
    state_root = require_real_directory(repo / "runner-state", "runner-state root")
    run_state = _require_direct_directory(state_root, run_id, "run state")
    state = _require_direct_directory(run_state, problem_id, "task state")
    manifest = _read_regular_json(run / "run.json", "run manifest")
    if manifest.get("run_id") != run_id:
        raise PipelineContractError("run manifest ID does not match its directory")
    if problem_id not in manifest.get("tasks", []):
        raise PipelineContractError("task is not declared by the run manifest")
    runtime = manifest.get("runtime")
    if runtime is None:
        if manifest.get("legacy_import") is not True:
            raise PipelineContractError(
                "run manifest is missing frozen toolchain provenance"
            )
    else:
        lock_path = require_regular_file(
            repo / "data/klean-toolchain.lock.json",
            "frozen toolchain lock",
        )
        lock = _read_regular_json(lock_path, "frozen toolchain lock")
        expected_runtime = {
            "codex_cli_version": CODEX_CLI_VERSION,
            "k_version": K_VERSION,
            "runtimeverification_k_commit": K_COMMIT,
            "pyk_version": PYK_VERSION,
            "lean_toolchain": LEAN_TOOLCHAIN,
            "klean_toolchain_lock_sha256": sha256_file(lock_path),
        }
        if (
            lock != FROZEN_TOOLCHAIN_LOCK
            or runtime != expected_runtime
        ):
            raise PipelineContractError(
                "run toolchain differs from the frozen "
                "Codex 0.144.6 / K 7.1.293 / Klean 7.1.293 / Lean 4.22.0 stack"
            )
        condition = manifest.get("condition")
        if isinstance(condition, dict) and condition.get("kit") is True:
            # The run manifest records the Kit the run was created under.
            # A task manifest may override it with the Kit revision that
            # actually produced the selected candidate (adaptive Kit
            # development promotes replacement generations into one run).
            run_kit = _validate_kit_provenance(
                manifest.get("kit"), "run manifest"
            )
            task_manifest = _read_regular_json(
                task / "task.json", "task manifest"
            )
            task_kit = task_manifest.get("kit")
            effective_kit = (
                _validate_kit_provenance(task_kit, "task manifest")
                if task_kit is not None
                else run_kit
            )
            if require_current_kit:
                # Launching new model work mounts the vendored bundle in
                # data/skills, so the task's effective Kit must match the
                # frozen current lock exactly. Resolving historical
                # artifacts (status, audits, selection) must not.
                kit_lock = _read_regular_json(
                    repo / "data/kit-skills.lock.json", "Kit bundle lock"
                )
                expected_kit = {
                    "commit": kit_lock.get("commit"),
                    "skills_tree": kit_lock.get("skills_tree"),
                }
                if effective_kit != expected_kit:
                    raise PipelineContractError(
                        "run Kit provenance differs from the frozen Kit bundle"
                    )
    return task, state, manifest


def _walk_regular_files(root: Path, label: str) -> list[Path]:
    root = require_real_directory(root, label)
    pending = [root]
    files: list[Path] = []
    while pending:
        directory = pending.pop()
        try:
            entries = list(os.scandir(directory))
        except OSError as error:
            raise PipelineContractError(f"cannot scan {label}: {directory}") from error
        for entry in entries:
            path = Path(entry.path)
            try:
                mode = entry.stat(follow_symlinks=False).st_mode
            except OSError as error:
                raise PipelineContractError(
                    f"cannot inspect {label} entry: {path}"
                ) from error
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                files.append(path)
            else:
                raise PipelineContractError(
                    f"{label} contains linked or unsupported entry: {path}"
                )
    return sorted(files)


def extract_session_uuid(trace_root: Path) -> str:
    """Extract the sole Codex session UUID from a protected rollout tree."""

    root = require_real_directory(Path(trace_root), "Codex trace")
    session_ids: set[str] = set()
    rollout_count = 0
    for path in _walk_regular_files(root, "Codex trace"):
        if path.suffix != ".jsonl":
            continue
        rollout_count += 1
        try:
            with path.open(encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError as error:
                        raise PipelineContractError(
                            f"malformed rollout JSON at {path}:{line_number}"
                        ) from error
                    if not isinstance(event, dict):
                        raise PipelineContractError(
                            f"rollout event must be an object at {path}:{line_number}"
                        )
                    if event.get("type") != "session_meta":
                        continue
                    payload = event.get("payload")
                    value = payload.get("id") if isinstance(payload, dict) else None
                    try:
                        parsed = uuid.UUID(value)
                    except (AttributeError, TypeError, ValueError) as error:
                        raise PipelineContractError(
                            f"malformed session UUID at {path}:{line_number}"
                        ) from error
                    session_ids.add(str(parsed))
        except OSError as error:
            raise PipelineContractError(f"cannot read rollout: {path}") from error
    if rollout_count == 0:
        raise PipelineContractError("Codex trace contains no rollout JSONL")
    if len(session_ids) != 1:
        raise PipelineContractError(
            f"Codex trace must contain exactly one session UUID; found {len(session_ids)}"
        )
    return next(iter(session_ids))


def validate_session_trace_tree(trace_root: Path, expected_root: str) -> str:
    """Validate one Codex session plus authenticated subagent descendants."""

    try:
        root_uuid = str(uuid.UUID(expected_root))
    except (AttributeError, TypeError, ValueError) as error:
        raise PipelineContractError(
            "expected Codex trace root UUID is malformed"
        ) from error
    root = require_real_directory(Path(trace_root), "Codex trace")
    session_ids: set[str] = set()
    parents: dict[str, str] = {}
    rollout_count = 0
    for path in _walk_regular_files(root, "Codex trace"):
        if path.suffix != ".jsonl":
            continue
        rollout_count += 1
        try:
            with path.open(encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError as error:
                        raise PipelineContractError(
                            f"malformed rollout JSON at {path}:{line_number}"
                        ) from error
                    if not isinstance(event, dict):
                        raise PipelineContractError(
                            f"rollout event must be an object at {path}:{line_number}"
                        )
                    if event.get("type") != "session_meta":
                        continue
                    payload = event.get("payload")
                    value = payload.get("id") if isinstance(payload, dict) else None
                    try:
                        session_id = str(uuid.UUID(value))
                    except (AttributeError, TypeError, ValueError) as error:
                        raise PipelineContractError(
                            f"malformed session UUID at {path}:{line_number}"
                        ) from error
                    session_ids.add(session_id)
                    if session_id == root_uuid:
                        continue
                    parent_value = payload.get("parent_thread_id")
                    source = payload.get("source")
                    subagent = (
                        source.get("subagent")
                        if isinstance(source, dict)
                        else None
                    )
                    spawn = (
                        subagent.get("thread_spawn")
                        if isinstance(subagent, dict)
                        else None
                    )
                    spawn_parent_value = (
                        spawn.get("parent_thread_id")
                        if isinstance(spawn, dict)
                        else None
                    )
                    depth = spawn.get("depth") if isinstance(spawn, dict) else None
                    try:
                        parent_id = str(uuid.UUID(parent_value))
                        spawn_parent_id = str(uuid.UUID(spawn_parent_value))
                    except (AttributeError, TypeError, ValueError) as error:
                        raise PipelineContractError(
                            f"unrooted subagent session at {path}:{line_number}"
                        ) from error
                    if (
                        parent_id != spawn_parent_id
                        or isinstance(depth, bool)
                        or not isinstance(depth, int)
                        or depth <= 0
                    ):
                        raise PipelineContractError(
                            f"malformed subagent lineage at {path}:{line_number}"
                        )
                    previous = parents.setdefault(session_id, parent_id)
                    if previous != parent_id:
                        raise PipelineContractError(
                            f"conflicting subagent lineage at {path}:{line_number}"
                        )
        except OSError as error:
            raise PipelineContractError(f"cannot read rollout: {path}") from error
    if rollout_count == 0:
        raise PipelineContractError("Codex trace contains no rollout JSONL")
    if root_uuid not in session_ids:
        raise PipelineContractError("Codex trace does not contain expected root session")
    for session_id in session_ids - {root_uuid}:
        seen: set[str] = set()
        current = session_id
        while current != root_uuid:
            if current in seen:
                raise PipelineContractError("Codex subagent lineage contains a cycle")
            seen.add(current)
            parent = parents.get(current)
            if parent is None or parent not in session_ids:
                raise PipelineContractError(
                    "Codex subagent lineage is not rooted at expected session"
                )
            current = parent
    return root_uuid


def _append_ledger(state: Path, event: dict[str, Any]) -> None:
    ledger = require_regular_file(state / "stage-ledger.jsonl", "stage ledger")
    flags = os.O_RDWR | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(ledger, flags)
        with os.fdopen(descriptor, "r+", encoding="utf-8") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            stream.seek(0)
            sequence = sum(1 for line in stream if line.strip()) + 1
            record = {
                "sequence": sequence,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                **event,
            }
            encoded = json.dumps(record, sort_keys=True) + "\n"
            stream.seek(0, os.SEEK_END)
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
            fcntl.flock(stream, fcntl.LOCK_UN)
    except OSError as error:
        raise PipelineContractError(f"cannot append stage ledger: {ledger}") from error


def write_session_state(state: Path, session_id: str, source: str) -> dict[str, Any]:
    state = require_real_directory(Path(state), "task state")
    try:
        session_id = str(uuid.UUID(session_id))
    except (AttributeError, TypeError, ValueError) as error:
        raise PipelineContractError("session ID must be a UUID") from error
    home = _require_direct_directory(state, "codex-home", "persistent CODEX_HOME")
    home_stat = home.stat()
    document = {
        "schema_version": SCHEMA_VERSION,
        "session_id": session_id,
        "codex_home_relative": "codex-home",
        "codex_home_device": home_stat.st_dev,
        "codex_home_inode": home_stat.st_ino,
        "source": source,
    }
    write_json_atomic(state / "session.json", document)
    os.chmod(state / "session.json", 0o600)
    return document


def _read_session_state(state: Path) -> dict[str, Any]:
    document = _read_regular_json(state / "session.json", "session state")
    try:
        session_id = str(uuid.UUID(document["session_id"]))
        relative = document["codex_home_relative"]
        device = int(document["codex_home_device"])
        inode = int(document["codex_home_inode"])
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise PipelineContractError("session state is malformed") from error
    if relative != "codex-home":
        raise PipelineContractError("session state names an unexpected CODEX_HOME")
    home = _require_direct_directory(state, relative, "persistent CODEX_HOME")
    current = home.stat()
    if current.st_dev != device or current.st_ino != inode:
        raise PipelineContractError(
            "persistent CODEX_HOME was replaced after the session was recorded"
        )
    return {**document, "session_id": session_id}


def _stage_timeout_keys(stage: str) -> tuple[str, str]:
    try:
        return _INVOCATION_STAGES[stage]
    except KeyError as error:
        raise PipelineContractError(
            f"unsupported invocation stage: {stage}"
        ) from error


def _invocation_directories(invocations: Path) -> list[Path]:
    invocations = require_real_directory(invocations, "invocations root")
    children: list[Path] = []
    try:
        entries = list(os.scandir(invocations))
    except OSError as error:
        raise PipelineContractError(f"cannot scan invocations: {invocations}") from error
    for entry in entries:
        path = Path(entry.path)
        try:
            mode = entry.stat(follow_symlinks=False).st_mode
        except OSError as error:
            raise PipelineContractError(
                f"cannot inspect invocation entry: {path}"
            ) from error
        if not stat.S_ISDIR(mode):
            raise PipelineContractError(
                f"invocations root contains a non-directory entry: {path}"
            )
        children.append(path)
    return sorted(children, key=lambda child: child.name)


def resolve_stage_kit_skills(
    repo: Path, run_id: str, problem_id: str
) -> Path:
    """Return the Kit bundle path matching the task's recorded provenance.

    Later stages resume work generated under a historical Kit and must mount
    that exact bundle rather than the moving vendored copy. When the task's
    effective Kit matches the current lock, the vendored bundle is used;
    otherwise the recorded commit is materialized once from the Kit source
    repository into data/kit-archive/<commit>/skills, verified against the
    recorded skills tree, and reused thereafter.
    """
    import subprocess

    task, _state, run_manifest = _resolve_task_state(repo, run_id, problem_id)
    task_manifest = _read_regular_json(task / "task.json", "task manifest")
    task_kit = task_manifest.get("kit")
    effective = (
        _validate_kit_provenance(task_kit, "task manifest")
        if task_kit is not None
        else _validate_kit_provenance(
            run_manifest.get("kit"), "run manifest"
        )
    )
    lock = _read_regular_json(
        repo / "data/kit-skills.lock.json", "Kit bundle lock"
    )
    if effective == {
        "commit": lock.get("commit"),
        "skills_tree": lock.get("skills_tree"),
    }:
        # The compose mount validates existence at launch; fixtures and
        # dry-run paths must not require the vendored bundle on disk.
        return repo / "data/skills"
    commit = effective["commit"]
    source = lock.get("source_repository")
    if not isinstance(source, str) or not source:
        raise PipelineContractError(
            "Kit bundle lock does not record a source repository"
        )
    try:
        tree = subprocess.run(
            ["git", "-C", source, "rev-parse", f"{commit}:skills"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise PipelineContractError(
            f"cannot resolve recorded Kit commit {commit} in {source}"
        ) from error
    if tree != effective["skills_tree"]:
        raise PipelineContractError(
            "recorded Kit skills tree does not match its commit"
        )
    archive = repo / "data/kit-archive" / commit / "skills"
    if not archive.is_dir():
        archive.parent.mkdir(parents=True, exist_ok=True)
        try:
            payload = subprocess.run(
                ["git", "-C", source, "archive", commit, "skills"],
                capture_output=True,
                check=True,
            ).stdout
            extract = subprocess.run(
                ["tar", "-x", "-C", str(archive.parent)],
                input=payload,
                check=True,
            )
            del extract
        except (OSError, subprocess.CalledProcessError) as error:
            shutil.rmtree(archive.parent, ignore_errors=True)
            raise PipelineContractError(
                f"cannot materialize Kit commit {commit} from {source}"
            ) from error
    return require_real_directory(archive, "materialized Kit bundle")


def prepare_invocation(
    repo: Path, run_id: str, problem_id: str, stage: str
) -> Invocation:
    # New Stage 1 launches mount the vendored bundle and must match the
    # current lock; later stages mount the task's recorded Kit via
    # resolve_stage_kit_skills, so their gate is per-task provenance.
    task, state, run_manifest = _resolve_task_state(
        repo, run_id, problem_id, require_current_kit=(stage == "01-k-proof")
    )
    if stage not in _INVOCATION_STAGES:
        raise PipelineContractError(f"unsupported invocation stage: {stage}")
    stage_root = _require_direct_directory(task, stage, stage)
    invocations = _require_direct_directory(
        stage_root, "invocations", f"{stage} invocations"
    )
    existing = _invocation_directories(invocations)
    initial_key, total_key = _stage_timeout_keys(stage)
    try:
        initial_s = int(run_manifest["timeouts"][initial_key])
        total_s = int(run_manifest["timeouts"][total_key])
    except (KeyError, TypeError, ValueError) as error:
        raise PipelineContractError("run timeout policy is malformed") from error
    if initial_s <= 0 or total_s < initial_s:
        raise PipelineContractError("run timeout policy is unsupported")

    session_id: str | None = None
    if not existing:
        name = "001-initial"
        if stage == "01-k-proof":
            kind = "initial"
        else:
            session_id = _read_session_state(state)["session_id"]
            kind = "stage-resume"
        allocation_s = initial_s
    elif len(existing) == 1:
        first = existing[0]
        if first.name != "001-initial":
            raise PipelineContractError("first invocation has an unexpected name")
        first_manifest = _read_regular_json(
            first / "invocation.json", "first invocation manifest"
        )
        if first_manifest.get("status") != "TIMEOUT":
            raise PipelineContractError(
                f"{stage} is terminal and cannot be resumed"
            )
        finalized_allocation = first_manifest.get("allocation_s")
        if (
            isinstance(finalized_allocation, bool)
            or not isinstance(finalized_allocation, int)
            or finalized_allocation <= 0
        ):
            raise PipelineContractError(
                "finalized invocation allocation is malformed"
            )
        allocation_s = total_s - finalized_allocation
        if allocation_s <= 0:
            raise PipelineContractError(
                f"{stage} invocation budget is exhausted"
            )
        session_id = _read_session_state(state)["session_id"]
        name = "002-timeout-resume"
        kind = "timeout-resume"
    elif (
        len(existing) == 2
        and stage == "05-lean-proof"
        and os.environ.get("HE_STAGE5_THIRD_ALLOCATION_S")
    ):
        # User-authorized one-off extension: a third timeout continuation
        # of the SAME persisted session, budgeted explicitly through the
        # environment so the frozen run timeout policy stays untouched.
        # Chronicled in ops/v2-hold-list.md (2026-08-01 endgame).
        for prior in existing:
            prior_manifest = _read_regular_json(
                prior / "invocation.json", "prior invocation manifest"
            )
            if prior_manifest.get("status") not in ("TIMEOUT", "FAILED"):
                raise PipelineContractError(
                    f"{stage} is terminal and cannot be resumed"
                )
        try:
            allocation_s = int(os.environ["HE_STAGE5_THIRD_ALLOCATION_S"])
        except ValueError as error:
            raise PipelineContractError(
                "third-invocation allocation override is malformed"
            ) from error
        if allocation_s <= 0:
            raise PipelineContractError(
                "third-invocation allocation override must be positive"
            )
        session_id = _read_session_state(state)["session_id"]
        name = "003-timeout-resume"
        kind = "timeout-resume"
    elif (
        len(existing) >= 2
        and stage == "01-k-proof"
        and os.environ.get("HE_STAGE1_EXTRA_ALLOCATION_S")
    ):
        # User-authorized endgame extension mirroring the stage-5 one:
        # further timeout continuations of the SAME persisted stage-1
        # session after OOM/TIMEOUT priors, budgeted explicitly through
        # the environment. Chronicled in ops/v2-hold-list.md
        # (2026-08-01 endgame).
        for prior in existing:
            prior_manifest = _read_regular_json(
                prior / "invocation.json", "prior invocation manifest"
            )
            if prior_manifest.get("status") not in ("TIMEOUT", "OOM"):
                raise PipelineContractError(
                    f"{stage} is terminal and cannot be resumed"
                )
        try:
            allocation_s = int(os.environ["HE_STAGE1_EXTRA_ALLOCATION_S"])
        except ValueError as error:
            raise PipelineContractError(
                "extension allocation override is malformed"
            ) from error
        if allocation_s <= 0:
            raise PipelineContractError(
                "extension allocation override must be positive"
            )
        session_id = _read_session_state(state)["session_id"]
        name = f"{len(existing) + 1:03d}-timeout-resume"
        kind = "timeout-resume"
    elif (
        len(existing) >= 3
        and stage == "05-lean-proof"
        and os.environ.get("HE_STAGE5_FOURTH_ALLOCATION_S")
    ):
        # User-authorized endgame extension: further timeout
        # continuations of the SAME persisted session past the frozen
        # two-invocation budget, each budgeted explicitly through the
        # environment so the frozen run timeout policy stays untouched.
        # Every continuation is chronicled in ops/v2-hold-list.md
        # (2026-08-01 endgame).
        for prior in existing:
            prior_manifest = _read_regular_json(
                prior / "invocation.json", "prior invocation manifest"
            )
            if prior_manifest.get("status") not in ("TIMEOUT", "FAILED"):
                raise PipelineContractError(
                    f"{stage} is terminal and cannot be resumed"
                )
        try:
            allocation_s = int(os.environ["HE_STAGE5_FOURTH_ALLOCATION_S"])
        except ValueError as error:
            raise PipelineContractError(
                "extension allocation override is malformed"
            ) from error
        if allocation_s <= 0:
            raise PipelineContractError(
                "extension allocation override must be positive"
            )
        session_id = _read_session_state(state)["session_id"]
        name = f"{len(existing) + 1:03d}-timeout-resume"
        kind = "timeout-resume"
    else:
        raise PipelineContractError(f"{stage} invocation budget is exhausted")

    destination = invocations / name
    try:
        destination.mkdir()
    except FileExistsError as error:
        raise PipelineContractError(
            f"invocation was concurrently prepared: {destination}"
        ) from error
    task_manifest = _read_regular_json(task / "task.json", "task manifest")
    document = {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "name": name,
        "kind": kind,
        "status": "PREPARED",
        "allocation_s": allocation_s,
        "session_id": session_id,
        "prompt_sha256": task_manifest.get("inputs", {}).get(
            "instruction_prompt_sha256"
        ),
        "inputs": {
            "workspace_sha256": sha256_tree(stage_root / "workspace"),
        },
        "outputs": None,
    }
    try:
        write_json_atomic(destination / "invocation.json", document)
        _append_ledger(
            state,
            {
                "event": "invocation_prepared",
                "stage": stage,
                "invocation": name,
                "kind": kind,
                "allocation_s": allocation_s,
            },
        )
    except BaseException:
        shutil.rmtree(destination)
        raise
    return Invocation(
        stage=stage,
        name=name,
        kind=kind,
        path=destination.resolve(strict=True),
        allocation_s=allocation_s,
        session_id=session_id,
    )


def prepare_oom_resume(
    repo: Path, run_id: str, problem_id: str
) -> Invocation:
    task, state, _run_manifest = _resolve_task_state(
        repo, run_id, problem_id, require_current_kit=True
    )
    stage = "01-k-proof"
    stage_root = _require_direct_directory(task, stage, stage)
    invocations = _require_direct_directory(
        stage_root, "invocations", f"{stage} invocations"
    )
    existing = _invocation_directories(invocations)
    history = [path.name for path in existing]
    if history not in (
        ["001-initial"],
        ["001-initial", "002-timeout-resume"],
    ):
        # User-authorized endgame extension: a third OOM continuation
        # with an explicit higher memory ceiling, gated through the
        # environment so the frozen policy stays untouched. Chronicled
        # in ops/v2-hold-list.md (2026-08-01 endgame).
        if not (
            history == ["001-initial", "002-oom-resume"]
            and os.environ.get("HE_STAGE1_THIRD_OOM_MEMORY_BYTES")
        ):
            raise PipelineContractError(
                "OOM continuation history is unsupported"
            )
    previous = existing[-1]
    previous_document = _read_regular_json(
        previous / "invocation.json", "previous invocation manifest"
    )
    result = _read_regular_json(stage_root / "result.json", "Stage 1 result")
    current_workspace = sha256_tree(stage_root / "workspace")
    previous_outputs = previous_document.get("outputs")
    if (
        previous_document.get("status") != "OOM"
        or result.get("status") != "OOM"
        or result.get("invocation") != previous.name
        or result.get("outputs") != previous_outputs
        or not isinstance(previous_outputs, dict)
        or previous_outputs.get("workspace_sha256") != current_workspace
    ):
        raise PipelineContractError(
            "OOM continuation requires an unchanged terminal OOM result"
        )
    session_id = _read_session_state(state)["session_id"]
    if previous_document.get("session_id") != session_id:
        raise PipelineContractError(
            "OOM continuation session does not match persisted session"
        )

    name = (
        "002-oom-resume" if len(existing) == 1 else "003-oom-resume"
    )
    memory_limit_bytes = 16 * 1024**3
    override = os.environ.get("HE_STAGE1_THIRD_OOM_MEMORY_BYTES")
    if override:
        try:
            memory_limit_bytes = int(override)
        except ValueError as error:
            raise PipelineContractError(
                "OOM memory override is malformed"
            ) from error
        if memory_limit_bytes <= 16 * 1024**3:
            raise PipelineContractError(
                "OOM memory override must exceed the frozen 16 GiB limit"
            )
    destination = invocations / name
    try:
        destination.mkdir()
    except FileExistsError as error:
        raise PipelineContractError(
            f"OOM continuation already exists: {destination}"
        ) from error
    task_manifest = _read_regular_json(task / "task.json", "task manifest")
    document = {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "name": name,
        "kind": "oom-resume",
        "status": "PREPARED",
        "allocation_s": 3600,
        "session_id": session_id,
        "retry_of": previous.name,
        "memory_limit_bytes": memory_limit_bytes,
        "prompt_sha256": task_manifest.get("inputs", {}).get(
            "instruction_prompt_sha256"
        ),
        "inputs": {"workspace_sha256": current_workspace},
        "outputs": None,
    }
    try:
        write_json_atomic(destination / "invocation.json", document)
        _append_ledger(
            state,
            {
                "event": "invocation_prepared",
                "stage": stage,
                "invocation": name,
                "kind": "oom-resume",
                "allocation_s": 3600,
                "retry_of": previous.name,
                "memory_limit_bytes": memory_limit_bytes,
            },
        )
    except BaseException:
        shutil.rmtree(destination)
        raise
    return Invocation(
        stage=stage,
        name=name,
        kind="oom-resume",
        path=destination.resolve(strict=True),
        allocation_s=3600,
        session_id=session_id,
    )


def prepare_terminal_resume(
    repo: Path, run_id: str, problem_id: str
) -> Invocation:
    task, state, _run_manifest = _resolve_task_state(
        repo, run_id, problem_id, require_current_kit=True
    )
    stage = "01-k-proof"
    stage_root = _require_direct_directory(task, stage, stage)
    invocations = _require_direct_directory(
        stage_root, "invocations", f"{stage} invocations"
    )
    existing = _invocation_directories(invocations)
    names = [path.name for path in existing]
    previous = existing[-1] if existing else None
    if names == ["001-initial"]:
        expected_status = "FAILED"
        name = "002-failure-resume"
        reason = "transient-model-failure"
    elif names == ["001-initial", "002-timeout-resume"]:
        expected_status = "TIMEOUT"
        name = "003-timeout-extension"
        reason = "exhausted-timeout"
    else:
        raise PipelineContractError(
            "terminal continuation history is unsupported"
        )
    previous_document = _read_regular_json(
        previous / "invocation.json", "previous invocation manifest"
    )
    result = _read_regular_json(stage_root / "result.json", "Stage 1 result")
    current_workspace = sha256_tree(stage_root / "workspace")
    previous_outputs = previous_document.get("outputs")
    if (
        previous_document.get("status") != expected_status
        or result.get("status") != expected_status
        or result.get("invocation") != previous.name
        or result.get("outputs") != previous_outputs
        or not isinstance(previous_outputs, dict)
        or previous_outputs.get("workspace_sha256") != current_workspace
    ):
        raise PipelineContractError(
            "terminal continuation requires an unchanged terminal result"
        )
    session_id = _read_session_state(state)["session_id"]
    if previous_document.get("session_id") != session_id:
        raise PipelineContractError(
            "terminal continuation session does not match persisted session"
        )

    destination = invocations / name
    try:
        destination.mkdir()
    except FileExistsError as error:
        raise PipelineContractError(
            f"terminal continuation already exists: {destination}"
        ) from error
    task_manifest = _read_regular_json(task / "task.json", "task manifest")
    document = {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "name": name,
        "kind": "terminal-resume",
        "status": "PREPARED",
        "allocation_s": 3600,
        "session_id": session_id,
        "retry_of": previous.name,
        "continuation_reason": reason,
        "memory_limit_bytes": 8 * 1024**3,
        "prompt_sha256": task_manifest.get("inputs", {}).get(
            "instruction_prompt_sha256"
        ),
        "inputs": {"workspace_sha256": current_workspace},
        "outputs": None,
    }
    try:
        write_json_atomic(destination / "invocation.json", document)
        _append_ledger(
            state,
            {
                "event": "invocation_prepared",
                "stage": stage,
                "invocation": name,
                "kind": "terminal-resume",
                "allocation_s": 3600,
                "retry_of": previous.name,
                "continuation_reason": reason,
                "memory_limit_bytes": 8 * 1024**3,
            },
        )
    except BaseException:
        shutil.rmtree(destination)
        raise
    return Invocation(
        stage=stage,
        name=name,
        kind="terminal-resume",
        path=destination.resolve(strict=True),
        allocation_s=3600,
        session_id=session_id,
    )


def prepare_infrastructure_retry(
    repo: Path, run_id: str, problem_id: str, stage: str
) -> Invocation:
    task, state, _run_manifest = _resolve_task_state(
        repo, run_id, problem_id, require_current_kit=True
    )
    if stage != "01-k-proof":
        raise PipelineContractError(
            "infrastructure retry is supported only for 01-k-proof"
        )
    stage_root = _require_direct_directory(task, stage, stage)
    invocations = _require_direct_directory(
        stage_root, "invocations", f"{stage} invocations"
    )
    existing = _invocation_directories(invocations)
    names = [path.name for path in existing]
    if names[:2] != [
        "001-initial",
        "002-timeout-resume",
    ] or len(existing) not in {2, 3}:
        raise PipelineContractError(
            "infrastructure retry budget is exhausted or history is malformed"
        )
    first, second = existing[:2]
    first_document = _read_regular_json(
        first / "invocation.json", "first invocation manifest"
    )
    second_document = _read_regular_json(
        second / "invocation.json", "second invocation manifest"
    )
    if first_document.get("status") != "TIMEOUT":
        raise PipelineContractError(
            "infrastructure retry requires an initial timeout"
        )
    if second_document.get("status") == "PREPARED":
        raise PipelineContractError(
            "infrastructure retry requires a finalized second invocation"
        )
    if second_document.get("kind") != "timeout-resume":
        raise PipelineContractError(
            "infrastructure retry requires the timeout continuation"
        )
    session_id = _read_session_state(state)["session_id"]
    if second_document.get("session_id") != session_id:
        raise PipelineContractError(
            "infrastructure retry session does not match persisted session"
        )
    current_workspace = sha256_tree(stage_root / "workspace")

    def require_unchanged_workspace(
        document: dict[str, Any], label: str
    ) -> dict[str, Any]:
        inputs = document.get("inputs")
        outputs = document.get("outputs")
        input_workspace = (
            inputs.get("workspace_sha256")
            if isinstance(inputs, dict)
            else None
        )
        output_workspace = (
            outputs.get("workspace_sha256")
            if isinstance(outputs, dict)
            else None
        )
        if (
            not isinstance(input_workspace, str)
            or output_workspace != input_workspace
            or current_workspace != output_workspace
        ):
            raise PipelineContractError(
                f"infrastructure retry requires an unchanged {label} workspace"
            )
        return outputs

    outputs = require_unchanged_workspace(
        second_document, "timeout-continuation"
    )
    output_log = require_regular_file(
        second / "codex-output.log", "second invocation Codex output"
    )
    evidence = outputs.get("evidence") if isinstance(outputs, dict) else None
    expected_output_hash = (
        evidence.get("codex-output.log")
        if isinstance(evidence, dict)
        else None
    )
    output_hash = sha256_file(output_log)
    if expected_output_hash != output_hash:
        raise PipelineContractError(
            "second invocation Codex output changed after finalization"
        )
    try:
        namespace_denied = _BWRAP_NAMESPACE_DENIAL in output_log.read_bytes()
    except OSError as error:
        raise PipelineContractError(
            f"cannot read second invocation Codex output: {output_log}"
        ) from error
    if not namespace_denied:
        raise PipelineContractError(
            "infrastructure retry requires protected namespace-denial evidence"
        )
    allocation_s = second_document.get("allocation_s")
    if not isinstance(allocation_s, int) or allocation_s <= 0:
        raise PipelineContractError(
            "second invocation allocation is malformed"
        )

    retry_of = second.name
    infrastructure_error = {
        "kind": "codex-bubblewrap-userns-denied",
        "evidence": "002-timeout-resume/codex-output.log",
        "evidence_sha256": output_hash,
    }
    name = "003-infrastructure-retry"
    if len(existing) == 3:
        third = existing[2]
        if third.name != "003-infrastructure-retry":
            raise PipelineContractError(
                "infrastructure retry history is malformed"
            )
        third_document = _read_regular_json(
            third / "invocation.json",
            "first infrastructure retry manifest",
        )
        if third_document.get("status") == "PREPARED":
            raise PipelineContractError(
                "first infrastructure retry is still PREPARED"
            )
        if (
            third_document.get("kind") != "infrastructure-retry"
            or third_document.get("status") != "FAILED"
            or third_document.get("exit_code") != 70
            or third_document.get("duration_s") != 0
            or third_document.get("session_id") != session_id
        ):
            raise PipelineContractError(
                "infrastructure retry budget is exhausted"
            )
        third_outputs = require_unchanged_workspace(
            third_document, "pre-model harness-failure"
        )
        third_evidence = third_outputs.get("evidence")
        if not isinstance(third_evidence, dict) or third_evidence:
            raise PipelineContractError(
                "pre-model harness failure contains unexpected model evidence"
            )
        retry_of = third.name
        name = "004-infrastructure-retry"
        infrastructure_error = {
            "kind": "entrypoint-pre-model-harness-failure",
            "evidence": "003-infrastructure-retry/invocation.json",
            "evidence_sha256": sha256_file(
                third / "invocation.json"
            ),
        }

    destination = invocations / name
    try:
        destination.mkdir()
    except FileExistsError as error:
        raise PipelineContractError(
            f"infrastructure retry already exists: {destination}"
        ) from error
    task_manifest = _read_regular_json(task / "task.json", "task manifest")
    document = {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "name": name,
        "kind": "infrastructure-retry",
        "status": "PREPARED",
        "allocation_s": allocation_s,
        "session_id": session_id,
        "retry_of": retry_of,
        "infrastructure_error": infrastructure_error,
        "prompt_sha256": task_manifest.get("inputs", {}).get(
            "instruction_prompt_sha256"
        ),
        "inputs": {"workspace_sha256": current_workspace},
        "outputs": None,
    }
    try:
        write_json_atomic(destination / "invocation.json", document)
        _append_ledger(
            state,
            {
                "event": "invocation_prepared",
                "stage": stage,
                "invocation": name,
                "kind": "infrastructure-retry",
                "allocation_s": allocation_s,
                "retry_of": retry_of,
            },
        )
    except BaseException:
        shutil.rmtree(destination)
        raise
    return Invocation(
        stage=stage,
        name=name,
        kind="infrastructure-retry",
        path=destination.resolve(strict=True),
        allocation_s=allocation_s,
        session_id=session_id,
    )


def record_invocation_prompt(invocation: Path, prompt: Path) -> dict[str, Any]:
    invocation = require_real_directory(Path(invocation), "invocation")
    prompt = require_regular_file(Path(prompt), "invocation prompt")
    document = _read_regular_json(
        invocation / "invocation.json", "invocation manifest"
    )
    if document.get("status") != "PREPARED":
        raise PipelineContractError("only a PREPARED invocation can receive a prompt")
    document["prompt_sha256"] = sha256_file(prompt)
    write_json_atomic(invocation / "invocation.json", document)
    return document


def _invocation_output_hashes(invocation: Path, workspace: Path) -> dict[str, Any]:
    evidence: dict[str, str] = {}
    for path in _walk_regular_files(invocation, "invocation evidence"):
        if path.name in {"invocation.json", "metrics.json"}:
            continue
        evidence[path.relative_to(invocation).as_posix()] = sha256_file(path)
    return {
        "workspace_sha256": sha256_tree(workspace),
        "evidence": evidence,
    }


def previous_session_cumulative(
    task: Path, session_id: str
) -> dict[str, int] | None:
    """Return the latest finalized Stage 1/3/5 cumulative for one session."""

    task = require_real_directory(Path(task), "task")
    try:
        session_id = str(uuid.UUID(session_id))
    except (AttributeError, TypeError, ValueError) as error:
        raise PipelineContractError("session ID must be a UUID") from error

    latest: dict[str, int] | None = None
    for stage in _INVOCATION_STAGES:
        stage_root = _require_direct_directory(task, stage, stage)
        invocations = _require_direct_directory(
            stage_root, "invocations", f"{stage} invocations"
        )
        for invocation in _invocation_directories(invocations):
            manifest = _read_regular_json(
                invocation / "invocation.json",
                "prior invocation manifest",
            )
            if (
                manifest.get("status") == "PREPARED"
                or manifest.get("session_id") != session_id
            ):
                continue
            usage_path = invocation / "usage.json"
            if not usage_path.exists() and not usage_path.is_symlink():
                continue
            usage = _read_regular_json(
                usage_path,
                "prior invocation usage",
            )
            cumulative = usage.get("cumulative")
            if cumulative is None:
                continue
            if not isinstance(cumulative, dict):
                raise PipelineContractError(
                    "prior invocation cumulative usage is malformed"
                )
            normalized: dict[str, int] = {}
            for name in _usage_accounting_module().TOKEN_FIELDS:
                value = cumulative.get(name)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int)
                    or value < 0
                ):
                    raise PipelineContractError(
                        "prior invocation cumulative usage is malformed"
                    )
                normalized[name] = value
            if latest is None or all(
                normalized[name] >= latest[name]
                for name in normalized
            ):
                latest = normalized
            elif not all(
                normalized[name] <= latest[name]
                for name in normalized
            ):
                raise PipelineContractError(
                    "prior invocation cumulative usage is inconsistent"
                )
    return latest


def refresh_run_usage_summary(run: Path) -> dict[str, Any]:
    """Serialize and refresh one run's aggregate usage summary."""

    run = require_real_directory(Path(run), "run")
    lock_path = run / ".usage-summary.lock"
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as error:
        raise PipelineContractError(
            f"cannot open run usage-summary lock: {lock_path}: {error}"
        ) from error
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise PipelineContractError(
                f"run usage-summary lock must be a regular file: {lock_path}"
            )
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        return _usage_accounting_module().write_run_summary(run)
    except OSError as error:
        raise PipelineContractError(
            f"cannot lock run usage summary: {lock_path}: {error}"
        ) from error
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def finalize_invocation(
    repo: Path,
    run_id: str,
    problem_id: str,
    stage: str,
    invocation_name: str,
    *,
    exit_code: int,
    duration_s: int,
    timeout_marker: bool,
    oom_killed: bool,
    image_id: str,
    result_metadata: dict[str, Any] | None = None,
    prepublication_guard: Callable[[], None] | None = None,
    expected_evidence: dict[str, str] | None = None,
) -> dict[str, Any]:
    task, state, _run_manifest = _resolve_task_state(repo, run_id, problem_id)
    invocation_name = validate_safe_component(invocation_name, "invocation name")
    stage_root = _require_direct_directory(task, stage, stage)
    invocations = _require_direct_directory(
        stage_root, "invocations", f"{stage} invocations"
    )
    invocation = _require_direct_directory(
        invocations, invocation_name, "invocation"
    )
    document = _read_regular_json(
        invocation / "invocation.json", "invocation manifest"
    )
    if document.get("status") != "PREPARED":
        raise PipelineContractError("invocation is not in PREPARED state")
    if not isinstance(exit_code, int) or not isinstance(duration_s, int):
        raise PipelineContractError("exit code and duration must be integers")
    if duration_s < 0:
        raise PipelineContractError("duration cannot be negative")
    if not isinstance(timeout_marker, bool) or not isinstance(oom_killed, bool):
        raise PipelineContractError("timeout and OOM states must be booleans")
    if not isinstance(image_id, str) or not image_id:
        raise PipelineContractError("container image ID is required")
    metadata = {} if result_metadata is None else result_metadata
    reserved_metadata_keys = {
        "schema_version",
        "stage",
        "name",
        "kind",
        "status",
        "invocation",
        "session_id",
        "resumable",
        "exit_code",
        "duration_s",
        "cumulative_duration_s",
        "image_id",
        "outputs",
    }
    if (
        not isinstance(metadata, dict)
        or not all(isinstance(key, str) for key in metadata)
        or reserved_metadata_keys.intersection(metadata)
    ):
        raise PipelineContractError("result metadata is malformed")
    try:
        json.dumps(metadata)
    except (TypeError, ValueError) as error:
        raise PipelineContractError("result metadata is not JSON-safe") from error
    if prepublication_guard is not None and not callable(
        prepublication_guard
    ):
        raise PipelineContractError("prepublication guard is malformed")
    expected_evidence_hashes = (
        {} if expected_evidence is None else expected_evidence
    )
    if not isinstance(expected_evidence_hashes, dict):
        raise PipelineContractError("expected invocation evidence is malformed")
    for relative, digest in expected_evidence_hashes.items():
        if (
            not isinstance(relative, str)
            or not relative
            or relative.startswith("/")
            or "\\" in relative
            or any(
                component in {"", ".", ".."}
                for component in relative.split("/")
            )
            or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        ):
            raise PipelineContractError(
                "expected invocation evidence is malformed"
            )
    trust_digest = metadata.get("trust_boundary_sha256")
    trust_artifact = metadata.get("trust_boundary_artifact")
    if trust_digest is not None or trust_artifact is not None:
        artifact_prefix = f"invocations/{invocation_name}/"
        relative_artifact = (
            trust_artifact.removeprefix(artifact_prefix)
            if isinstance(trust_artifact, str)
            and trust_artifact.startswith(artifact_prefix)
            else None
        )
        if (
            not isinstance(trust_digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", trust_digest) is None
            or relative_artifact is None
            or expected_evidence_hashes.get(relative_artifact)
            != trust_digest
        ):
            raise PipelineContractError(
                "trust-boundary metadata does not match expected evidence"
            )

    raw_metrics: Path | None = invocation / "metrics.json"
    runtime_metrics = invocation / "runtime-metrics.json"
    if raw_metrics.exists() or raw_metrics.is_symlink():
        raw_metrics = require_regular_file(
            raw_metrics, "entrypoint runtime metrics"
        )
        if runtime_metrics.exists() or runtime_metrics.is_symlink():
            raise PipelineContractError("runtime metrics already exist")
    else:
        raw_metrics = None

    if oom_killed:
        status = "OOM"
    elif timeout_marker:
        status = "TIMEOUT"
    elif exit_code == 0:
        status = "SUCCEEDED"
    else:
        status = "FAILED"

    trace = invocation / "codex-trace"
    session_id: str | None
    if document.get("kind") == "initial":
        try:
            session_id = extract_session_uuid(trace)
        except PipelineContractError:
            if status == "SUCCEEDED":
                raise
            session_id = None
        if session_id is not None:
            write_session_state(
                state, session_id, f"{stage}/{invocation_name}"
            )
    else:
        session = _read_session_state(state)
        session_id = session["session_id"]
        expected = document.get("session_id")
        if expected != session_id:
            raise PipelineContractError(
                "invocation session does not match persisted session"
            )
        trace_exists = trace.exists() or trace.is_symlink()
        if (
            stage in {"03-lemma-discovery", "05-lean-proof"}
            and status == "SUCCEEDED"
            and not trace_exists
        ):
            raise PipelineContractError(
                "successful stage-resume requires a session trace"
            )
        # Only Stage 1 recovery can succeed without a trace, for the protected
        # namespace-denial path. Any trace present there must still match.
        if trace_exists:
            try:
                trace_session_id = (
                    validate_session_trace_tree(trace, session_id)
                    if stage == "05-lean-proof"
                    else extract_session_uuid(trace)
                )
            except PipelineContractError as error:
                raise PipelineContractError(
                    "trace session does not match persisted session"
                ) from error
            if trace_session_id != session_id:
                raise PipelineContractError(
                    "trace session does not match persisted session"
                )

    previous_duration = 0
    for other in _invocation_directories(invocations):
        if other == invocation:
            continue
        other_document = _read_regular_json(
            other / "invocation.json", "prior invocation manifest"
        )
        if other_document.get("status") == "PREPARED":
            raise PipelineContractError("another invocation is still PREPARED")
        value = other_document.get("duration_s")
        if not isinstance(value, int) or value < 0:
            raise PipelineContractError("prior invocation duration is malformed")
        previous_duration += value
    cumulative = previous_duration + duration_s

    usage_accounting = _usage_accounting_module()
    if session_id is not None and (trace.exists() or trace.is_symlink()):
        usage_accounting.write_trace_usage(
            trace,
            invocation / "usage.json",
            previous_cumulative=previous_session_cumulative(task, session_id),
        )
    metrics = {
        "exit_code": exit_code,
        "duration_s": duration_s,
        "timeout_marker": timeout_marker,
        "oom_killed": oom_killed,
        "status": status,
        "allocation_s": document["allocation_s"],
        "cumulative_duration_s": cumulative,
        "image_id": image_id,
    }
    runtime_metrics_created = False
    normalized_metrics_written = False
    try:
        if raw_metrics is not None:
            _copy_file_atomic_no_clobber(raw_metrics, runtime_metrics)
            runtime_metrics_created = True
        write_json_atomic(invocation / "metrics.json", metrics)
        normalized_metrics_written = True
        outputs = _invocation_output_hashes(
            invocation, stage_root / "workspace"
        )
        evidence = outputs["evidence"]
        for relative, digest in expected_evidence_hashes.items():
            if evidence.get(relative) != digest:
                raise PipelineContractError(
                    "expected invocation evidence does not match "
                    f"published outputs: {relative}"
                )
        if prepublication_guard is not None:
            prepublication_guard()
        finalized = {
            **document,
            "status": status,
            "exit_code": exit_code,
            "duration_s": duration_s,
            "cumulative_duration_s": cumulative,
            "image_id": image_id,
            "session_id": session_id,
            "resumable": session_id is not None,
            "outputs": outputs,
            **metadata,
        }
        write_json_atomic(invocation / "invocation.json", finalized)
    except BaseException:
        try:
            if normalized_metrics_written:
                if raw_metrics is None:
                    (invocation / "metrics.json").unlink()
                else:
                    _copy_file_atomic_replace(
                        runtime_metrics,
                        invocation / "metrics.json",
                    )
            if runtime_metrics_created:
                runtime_metrics.unlink()
        except OSError as rollback_error:
            raise PipelineContractError(
                "cannot roll back incomplete invocation finalization"
            ) from rollback_error
        raise
    result = {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "status": status,
        "invocation": invocation_name,
        "session_id": session_id,
        "resumable": session_id is not None,
        "cumulative_duration_s": cumulative,
        "outputs": outputs,
        **metadata,
    }
    write_json_atomic(stage_root / "result.json", result)
    _append_ledger(
        state,
        {
            "event": "invocation_finalized",
            "stage": stage,
            "invocation": invocation_name,
            "status": status,
            "duration_s": duration_s,
            "cumulative_duration_s": cumulative,
        },
    )
    refresh_run_usage_summary(task.parent.parent)
    return result


_SELECTION_STAGES = {
    "02-k-audit": ("executions", "verdict.json"),
    "04-klean-generation": ("generations", "preflight.json"),
    "06-lean-audit": ("executions", "verdict.json"),
}


def _audit_error_has_token_evidence(stage: str, candidate: Path) -> bool:
    trace = candidate / "codex-trace"
    if not trace.exists() and not trace.is_symlink():
        return False
    usage_accounting = _usage_accounting_module()
    try:
        usage = usage_accounting.extract_trace_usage(trace)
    except usage_accounting.UsageAccountingError as error:
        raise PipelineContractError(
            f"{stage} Codex trace usage is invalid: {error}"
        ) from error
    return usage.get("status") == "COMPLETE"


def _selection_status(stage: str, candidate: Path) -> str:
    _container, document_name = _SELECTION_STAGES[stage]
    if stage in {"02-k-audit", "06-lean-audit"}:
        document = _read_regular_json(
            candidate / document_name, f"{stage} candidate status"
        )
        if document.get("audit_status") == "AUDIT_ERROR":
            require_regular_file(
                candidate / "audit-input.json", f"{stage} audit-input.json"
            )
            if _audit_error_has_token_evidence(stage, candidate):
                require_regular_file(
                    candidate / "usage.json", f"{stage} usage.json"
                )
            return "AUDIT_ERROR"
        for name in (
            "audit-input.json",
            "metrics.json",
            "codex-output.log",
            "codex-last.txt",
            "REVIEW.md",
            "verdict.json",
            "usage.json",
        ):
            require_regular_file(candidate / name, f"{stage} {name}")
        _walk_regular_files(candidate / "codex-trace", f"{stage} Codex trace")
        if not _walk_regular_files(
            candidate / "evidence", f"{stage} evidence"
        ):
            raise PipelineContractError(f"{stage} evidence is empty")
    else:
        document = _read_regular_json(
            candidate / document_name, f"{stage} candidate status"
        )
    if stage == "04-klean-generation":
        status = document.get("status")
        if status not in {
            "PASS",
            "KLEAN_NO_OBLIGATIONS",
            "KLEAN_PREFLIGHT_ERROR",
        }:
            raise PipelineContractError("Klean preflight status is invalid")
        require_regular_file(candidate / "export.log", "Klean export log")
        if status in {"PASS", "KLEAN_NO_OBLIGATIONS"}:
            for name in (
                "input-manifest.json",
                "generator-manifest.json",
                "trust-inventory.json",
                "export-result.json",
                "preflight.log",
            ):
                require_regular_file(candidate / name, f"Klean {name}")
            _walk_regular_files(
                candidate / "generated", "generated Lean project"
            )
        return status
    audit_status = document.get("audit_status")
    if audit_status != "COMPLETE":
        raise PipelineContractError("audit is neither complete nor AUDIT_ERROR")
    if stage == "06-lean-audit":
        mechanical = _read_regular_json(
            candidate / "mechanical-check.json",
            "Stage 6 mechanical check",
        )
        mechanical_status = mechanical.get("status")
        if mechanical_status == "FAIL" and (
            document.get("verdict"),
            document.get("legitimacy"),
        ) != ("FAIL", "NOT_LEGIT"):
            raise PipelineContractError(
                "failed mechanical gate must force a NOT_LEGIT audit"
            )
        if mechanical_status not in {"PASS", "FAIL"}:
            raise PipelineContractError(
                "completed Stage 6 audit lacks a terminal mechanical gate"
            )
    pair = (document.get("verdict"), document.get("legitimacy"))
    if pair not in {
        ("PASS", "LEGIT"),
        ("CONCERNS", "LEGIT"),
        ("FAIL", "NOT_LEGIT"),
    }:
        raise PipelineContractError("audit verdict and legitimacy are inconsistent")
    return str(document["verdict"])


def select_stage_output_at(
    task: Path,
    state: Path,
    stage: str,
    candidate_name: str,
    *,
    expected_candidate_sha256: str | None = None,
    replace_selected: bool = False,
) -> dict[str, Any]:
    task = require_real_directory(Path(task), "task")
    state = require_real_directory(Path(state), "task state")
    if stage not in _SELECTION_STAGES:
        raise PipelineContractError(f"unsupported selection stage: {stage}")
    if replace_selected and stage not in {
        "02-k-audit",
        "04-klean-generation",
        "06-lean-audit",
    }:
        raise PipelineContractError(
            "explicit terminal replacement is unsupported for this stage"
        )
    if expected_candidate_sha256 is not None and (
        not isinstance(expected_candidate_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_candidate_sha256) is None
    ):
        raise PipelineContractError(
            "expected candidate hash is malformed"
        )
    candidate_name = validate_safe_component(candidate_name, "candidate name")
    stage_root = _require_direct_directory(task, stage, stage)
    container_name, _document_name = _SELECTION_STAGES[stage]
    container = _require_direct_directory(
        stage_root, container_name, f"{stage} candidates"
    )
    candidate = _require_direct_directory(
        container, candidate_name, f"{stage} candidate"
    )
    status = _selection_status(stage, candidate)
    selected_path = stage_root / "selected.json"
    previous: dict[str, Any] | None = None
    if selected_path.exists() or selected_path.is_symlink():
        previous = _read_regular_json(selected_path, f"{stage} selection")
        previous_relative = previous.get("relative_path")
        if not isinstance(previous_relative, str):
            raise PipelineContractError("previous selection path is malformed")
        parts = Path(previous_relative).parts
        if len(parts) != 2 or parts[0] != container_name:
            raise PipelineContractError("previous selection escapes its stage")
        previous_candidate = _require_direct_directory(
            container, parts[1], f"previous {stage} candidate"
        )
        previous_status = _selection_status(stage, previous_candidate)
        retryable = (
            previous_status == "KLEAN_PREFLIGHT_ERROR"
            if stage == "04-klean-generation"
            else previous_status == "AUDIT_ERROR"
        )
        if not retryable and not replace_selected:
            raise PipelineContractError(
                f"{stage} selection is terminal and cannot be replaced"
            )
    candidate_sha256 = sha256_tree(candidate)
    if (
        expected_candidate_sha256 is not None
        and candidate_sha256 != expected_candidate_sha256
    ):
        raise PipelineContractError(
            f"{stage} candidate changed before selection"
        )
    document = {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "relative_path": f"{container_name}/{candidate_name}",
        "artifact_sha256": candidate_sha256,
        "status": status,
        "selected_at": datetime.now(timezone.utc).isoformat(),
        "replaces": previous.get("relative_path") if previous else None,
    }
    write_json_atomic(selected_path, document)
    _append_ledger(
        state,
        {
            "event": "stage_output_selected",
            "stage": stage,
            "relative_path": document["relative_path"],
            "status": status,
        },
    )
    return document


def select_stage_output(
    repo: Path,
    run_id: str,
    problem_id: str,
    stage: str,
    candidate_name: str,
    *,
    expected_candidate_sha256: str | None = None,
    replace_selected: bool = False,
) -> dict[str, Any]:
    """Select a stage output resolved through the public run layout."""

    task, state, _run_manifest = _resolve_task_state(repo, run_id, problem_id)
    return select_stage_output_at(
        task,
        state,
        stage,
        candidate_name,
        expected_candidate_sha256=expected_candidate_sha256,
        replace_selected=replace_selected,
    )
