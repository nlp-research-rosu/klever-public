#!/usr/bin/env python3
"""Resolve immutable audit inputs and normalize reviewer verdicts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any

MODULE_REPO = Path(__file__).resolve().parent.parent
if str(MODULE_REPO) not in sys.path:
    sys.path.insert(0, str(MODULE_REPO))


CONDITIONS = {
    "bare": False,
    "kit": False,
    "semantics": True,
    "kit-semantics": True,
}

VALID_PAIRS = {
    ("PASS", "LEGIT"),
    ("CONCERNS", "LEGIT"),
    ("FAIL", "NOT_LEGIT"),
}

TRUSTED_CANONICAL_FILENAME = "canonical" + ".py"

_VERDICT_MARKER = re.compile(r"VERDICT: (PASS|CONCERNS|FAIL)")
_LEGITIMACY_MARKER = re.compile(r"LEGITIMACY: (LEGIT|NOT_LEGIT)")
_HASH_CHUNK_SIZE = 1024 * 1024


class AuditContractError(RuntimeError):
    """Raised when an audit input violates the host-side safety contract."""


def validate_safe_component(
    value: object, label: str, *, allow_hidden: bool
) -> None:
    if not isinstance(value, str):
        raise AuditContractError(f"{label} must be a string path component")
    path = Path(value)
    unsafe = (
        not value
        or value in {".", ".."}
        or (not allow_hidden and value.startswith("."))
        or path.is_absolute()
        or len(path.parts) != 1
        or "/" in value
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    )
    if unsafe:
        visibility = "nonhidden " if not allow_hidden else ""
        raise AuditContractError(
            f"{label} must be one safe {visibility}path component: {value!r}"
        )


def _lstat(path: Path, label: str) -> os.stat_result:
    try:
        return path.lstat()
    except OSError as error:
        raise AuditContractError(f"{label} is missing or cannot be inspected: {path}") from error


def require_real_directory(path: Path, label: str) -> Path:
    mode = _lstat(path, label).st_mode
    if not stat.S_ISDIR(mode):
        raise AuditContractError(f"{label} must be a real directory: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as error:
        raise AuditContractError(f"{label} cannot be resolved: {path}") from error


def require_regular_file(path: Path, label: str | None = None) -> Path:
    description = label or str(path)
    mode = _lstat(path, description).st_mode
    if not stat.S_ISREG(mode):
        raise AuditContractError(
            f"{description} must be a real regular file: {path}"
        )
    try:
        return path.resolve(strict=True)
    except OSError as error:
        raise AuditContractError(f"{description} cannot be resolved: {path}") from error


def require_direct_child(parent: Path, name: str, label: str) -> Path:
    parent = require_real_directory(parent, f"parent of {label}")
    child = parent / name
    resolved = require_real_directory(child, label)
    if resolved.parent != parent:
        raise AuditContractError(f"{label} must resolve directly below {parent}: {name!r}")
    return resolved


def read_regular_json(path: Path) -> dict[str, Any]:
    regular = require_regular_file(path)
    try:
        document = json.loads(regular.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise AuditContractError(f"{path}: malformed JSON: {error}") from error
    if not isinstance(document, dict):
        raise AuditContractError(f"{path}: JSON document must be an object")
    return document


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise AuditContractError(f"cannot hash regular file {path}: {error}") from error
    return digest.hexdigest()


def _optional_regular_file_hash(path: Path) -> str | None:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return None
    if not stat.S_ISREG(mode):
        return None
    try:
        return sha256_file(path)
    except AuditContractError:
        return None


def _tree_entry_type(mode: int) -> str:
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISFIFO(mode):
        return "fifo"
    if stat.S_ISSOCK(mode):
        return "socket"
    if stat.S_ISBLK(mode):
        return "block-device"
    if stat.S_ISCHR(mode):
        return "character-device"
    return "unknown"


def _framed_update(digest: Any, value: bytes) -> None:
    digest.update(len(value).to_bytes(8, "big"))
    digest.update(value)


def _framed_file_update(
    digest: Any, path: Path, expected_size: int
) -> None:
    digest.update(expected_size.to_bytes(8, "big"))
    bytes_read = 0
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        with os.fdopen(os.open(path, flags), "rb") as stream:
            for chunk in iter(lambda: stream.read(_HASH_CHUNK_SIZE), b""):
                bytes_read += len(chunk)
                digest.update(chunk)
    except OSError as error:
        raise AuditContractError(f"cannot read tree file {path}: {error}") from error
    if bytes_read != expected_size:
        raise AuditContractError(
            f"tree file changed size while hashing: {path} "
            f"(expected {expected_size}, read {bytes_read})"
        )


def sha256_tree(root: Path) -> str:
    root = require_real_directory(root, f"tree root {root}")
    entries: list[tuple[str, str, Path, int]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as iterator:
                children = list(iterator)
        except OSError as error:
            raise AuditContractError(f"cannot scan tree {directory}: {error}") from error
        for entry in children:
            path = Path(entry.path)
            try:
                entry_stat = entry.stat(follow_symlinks=False)
            except OSError as error:
                raise AuditContractError(
                    f"cannot inspect tree entry {path}: {error}"
                ) from error
            mode = entry_stat.st_mode
            entry_type = _tree_entry_type(mode)
            relative = path.relative_to(root).as_posix()
            entries.append((relative, entry_type, path, entry_stat.st_size))
            if entry_type == "directory":
                pending.append(path)

    digest = hashlib.sha256()
    for relative, entry_type, path, size in sorted(
        entries, key=lambda item: item[0]
    ):
        _framed_update(digest, os.fsencode(relative))
        _framed_update(digest, entry_type.encode())
        if entry_type == "file":
            _framed_file_update(digest, path, size)
        elif entry_type == "symlink":
            try:
                target = os.readlink(path)
            except OSError as error:
                raise AuditContractError(
                    f"cannot read tree symlink {path}: {error}"
                ) from error
            _framed_update(digest, os.fsencode(target))
        else:
            _framed_update(digest, b"")
    return digest.hexdigest()


def _optional_tree_hash(root: Path) -> str | None:
    try:
        mode = root.lstat().st_mode
    except OSError:
        return None
    if not stat.S_ISDIR(mode):
        return None
    try:
        return sha256_tree(root)
    except AuditContractError:
        return None


def legacy_content_tree_hash(root: Path) -> str:
    """Reproduce the schema-v1 seed-tree hash used by imported runs."""

    root = require_real_directory(root, "legacy seed tree")
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        try:
            metadata = path.lstat()
        except OSError as error:
            raise AuditContractError(
                f"cannot inspect legacy seed tree entry: {path}"
            ) from error
        if stat.S_ISDIR(metadata.st_mode):
            continue
        if not stat.S_ISREG(metadata.st_mode):
            raise AuditContractError(
                f"legacy seed tree contains a linked or unsupported entry: {path}"
            )
        relative = path.relative_to(root).as_posix().encode()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        try:
            content = path.read_bytes()
        except OSError as error:
            raise AuditContractError(
                f"cannot read legacy seed tree entry: {path}"
            ) from error
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def require_generation_evidence(candidate: Path) -> dict[str, Path]:
    evidence = {
        "metrics": require_regular_file(candidate / "metrics.json"),
        "codex_output": require_regular_file(candidate / "codex-output.log"),
        "codex_last": require_regular_file(candidate / "codex-last.txt"),
        "codex_trace": require_real_directory(
            candidate / "codex-trace", "codex-trace generation evidence"
        ),
    }
    return evidence


def _manifest_condition(manifest: dict[str, Any]) -> str:
    condition_block = manifest.get("condition")
    if not isinstance(condition_block, dict):
        raise AuditContractError("manifest condition must be an object")
    condition = condition_block.get("name")
    if not isinstance(condition, str):
        raise AuditContractError("manifest condition name must be a string")
    if condition not in CONDITIONS:
        raise AuditContractError(f"unsupported manifest condition: {condition!r}")
    return condition


def _manifest_input_hash(manifest: dict[str, Any], name: str) -> object:
    inputs = manifest.get("inputs")
    if not isinstance(inputs, dict):
        return None
    return inputs.get(name)


def build_resolution_and_hashes(
    repo: Path,
    config: str,
    problem: str,
    condition: str,
    candidate: Path,
    canonical: Path,
    prompt: Path,
    translator: Path,
    semantics: Path | None,
    manifest: dict[str, Any],
    manifest_path: Path,
    generation_evidence: dict[str, Path],
) -> dict[str, object]:
    candidate_prompt_hash = _optional_regular_file_hash(candidate / "prompt.py")
    candidate_translator_hash = _optional_regular_file_hash(candidate / "py2mpy.py")
    candidate_semantics_hash = _optional_tree_hash(candidate / "reference-semantics")
    trusted_prompt_hash = sha256_file(prompt)
    trusted_translator_hash = sha256_file(translator)
    trusted_semantics_hash = sha256_tree(semantics) if semantics is not None else None

    hashes = {
        "candidate_tree_sha256": sha256_tree(candidate),
        "manifest_sha256": sha256_file(manifest_path),
        "canonical_sha256": sha256_file(canonical),
        "trusted_prompt_sha256": trusted_prompt_hash,
        "candidate_prompt_sha256": candidate_prompt_hash,
        "trusted_translator_sha256": trusted_translator_hash,
        "candidate_translator_sha256": candidate_translator_hash,
        "trusted_reference_semantics_sha256": trusted_semantics_hash,
        "candidate_reference_semantics_sha256": candidate_semantics_hash,
        "generation_metrics_sha256": sha256_file(generation_evidence["metrics"]),
        "generation_codex_output_sha256": sha256_file(
            generation_evidence["codex_output"]
        ),
        "generation_codex_last_sha256": sha256_file(
            generation_evidence["codex_last"]
        ),
        "generation_codex_trace_sha256": sha256_tree(
            generation_evidence["codex_trace"]
        ),
    }
    integrity = {
        "candidate_prompt_matches_trusted": candidate_prompt_hash == trusted_prompt_hash,
        "candidate_translator_matches_trusted": (
            candidate_translator_hash == trusted_translator_hash
        ),
        "candidate_reference_semantics_matches_trusted": (
            candidate_semantics_hash == trusted_semantics_hash
            if semantics is not None
            else None
        ),
        "manifest_prompt_hash_matches_trusted": (
            _manifest_input_hash(manifest, "problem_prompt_sha256")
            == trusted_prompt_hash
        ),
        "manifest_translator_hash_matches_trusted": (
            _manifest_input_hash(manifest, "translator_sha256")
            == trusted_translator_hash
        ),
        "manifest_reference_semantics_hash_matches_trusted": (
            _manifest_input_hash(manifest, "reference_semantics_sha256")
            == trusted_semantics_hash
            if semantics is not None
            else None
        ),
    }
    return {
        "repo": str(repo),
        "config": config,
        "generation_config": config,
        "manifest_config": manifest.get("config"),
        "problem_id": problem,
        "condition": condition,
        "semantics_mode": (
            "SUPPLIED_SEMANTICS" if semantics is not None else "GENERATED_SEMANTICS"
        ),
        "mount_reference_semantics": semantics is not None,
        "candidate": str(candidate),
        "canonical": str(canonical),
        "trusted_prompt": str(prompt),
        "translator": str(translator),
        "reference_semantics": str(semantics) if semantics is not None else None,
        "generation_evidence": {
            name: str(path) for name, path in generation_evidence.items()
        },
        "manifest": manifest,
        "hashes": hashes,
        "integrity": integrity,
    }


def resolve_audit(repo: Path, config: str, problem: str) -> dict[str, object]:
    validate_safe_component(config, "generation config", allow_hidden=False)
    validate_safe_component(problem, "problem ID", allow_hidden=False)
    repo = require_real_directory(Path(repo), "repository root")
    runs = require_real_directory(repo / "runs", "runs root")
    config_dir = require_direct_child(runs, config, "generation config")
    if config_dir == (runs / "archive").resolve():
        raise AuditContractError("runs/archive cannot be audited as an active run")
    candidate = require_direct_child(config_dir, problem, "candidate task")
    manifest_path = require_regular_file(candidate / "run-input.json")
    manifest = read_regular_json(manifest_path)
    condition = _manifest_condition(manifest)
    if manifest.get("problem_id") != problem:
        raise AuditContractError("manifest problem_id does not match task directory")
    generation_evidence = require_generation_evidence(candidate)
    canonical = require_regular_file(
        repo / "data/questions" / problem / TRUSTED_CANONICAL_FILENAME,
        "trusted canonical",
    )
    prompt = require_regular_file(
        repo / "data/questions" / problem / "prompt.py", "trusted prompt"
    )
    translator = require_regular_file(repo / "tools/py2mpy.py", "trusted translator")
    supplied = CONDITIONS[condition]
    semantics = (
        require_real_directory(repo / "data/reference/src", "trusted semantics")
        if supplied
        else None
    )
    resolution = build_resolution_and_hashes(
        repo,
        config,
        problem,
        condition,
        candidate,
        canonical,
        prompt,
        translator,
        semantics,
        manifest,
        manifest_path,
        generation_evidence,
    )
    resolution["record_layout"] = "legacy"
    resolution["generation_root"] = str(candidate)
    resolution["run_manifest"] = None
    resolution["task_manifest"] = None
    resolution["stage1_result"] = None
    return resolution


STAGE1_REQUIRED_ARTIFACTS = (
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
)


def _is_complete_legacy_stage1_import(
    task: Path,
    run_manifest: dict[str, object],
    result: dict[str, object],
    invocation_manifest: dict[str, object],
    invocation_name: str,
) -> bool:
    if (
        run_manifest.get("legacy_import") is not True
        or result.get("legacy_import") is not True
        or invocation_manifest.get("legacy_import") is not True
    ):
        return False
    migration_path = task / "migration.json"
    try:
        migration = read_regular_json(
            require_regular_file(migration_path, "legacy migration manifest")
        )
    except AuditContractError:
        return False
    return (
        migration.get("legacy_import") is True
        and migration.get("status") == "SUCCEEDED"
        and migration.get("input_provenance") == "COMPLETE"
        and migration.get("invocation") == invocation_name
    )


def _pipeline_contract_module():
    try:
        from tools import pipeline_contract
    except ImportError as error:
        raise AuditContractError(
            "stage-oriented pipeline support is unavailable"
        ) from error
    return pipeline_contract


def _resolve_trusted_semantics(repo: Path, manifest: dict) -> Path:
    """Mount the trusted semantics version the candidate was generated with.

    The reference semantics may be revised (recorded CPython-faithfulness
    fixes); each task manifest records the tree hash of the version its
    workspace was seeded from. The auditor must integrity-compare the
    candidate against that exact version, never a later one.
    """

    pipeline_contract = _pipeline_contract_module()
    recorded = (
        manifest.get("inputs", {}).get("reference_semantics_sha256")
        if isinstance(manifest.get("inputs"), dict)
        else None
    )
    if not isinstance(recorded, str) or not recorded:
        raise AuditContractError(
            "task manifest does not record its reference-semantics hash"
        )
    registry = read_regular_json(
        require_regular_file(
            repo / "data/reference-semantics-versions.json",
            "reference-semantics version registry",
        )
    )
    entry = registry.get("versions", {}).get(recorded)
    if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
        raise AuditContractError(
            "task's recorded reference-semantics hash is not a registered "
            f"version: {recorded}"
        )
    semantics = require_real_directory(
        repo / entry["path"], "trusted semantics version"
    )
    actual = pipeline_contract.sha256_tree(semantics)
    if actual != recorded:
        raise AuditContractError(
            "registered reference-semantics tree changed: "
            f"expected {recorded}, observed {actual}"
        )
    return semantics


def resolve_stage2_audit(
    repo: Path, run_id: str, problem: str
) -> dict[str, object]:
    """Resolve a frozen successful Stage 1 candidate for independent audit."""

    pipeline_contract = _pipeline_contract_module()
    try:
        task, _state, run_manifest = pipeline_contract._resolve_task_state(
            repo, run_id, problem
        )
        pipeline_contract.require_task_unblocked(task, "Stage 2")
    except pipeline_contract.PipelineContractError as error:
        raise AuditContractError(str(error)) from error
    stage = require_real_directory(task / "01-k-proof", "Stage 1")
    workspace = require_real_directory(
        stage / "workspace", "Stage 1 candidate workspace"
    )
    result = read_regular_json(require_regular_file(stage / "result.json"))
    if result.get("status") != "SUCCEEDED":
        # User-authorized endgame provision (2026-08-01, chronicled in
        # ops/v2-hold-list.md): a terminal honest-PARTIAL candidate may
        # be audited under the registered task-specific grading
        # provision when explicitly enabled through the environment.
        if not (
            result.get("status") == "FAILED"
            and os.environ.get("HE_AUDIT_ACCEPT_PARTIAL")
        ):
            raise AuditContractError(
                "Stage 1 result must be SUCCEEDED before audit"
            )
    invocation_name = result.get("invocation")
    validate_safe_component(
        invocation_name, "selected Stage 1 invocation", allow_hidden=False
    )
    invocations = require_real_directory(
        stage / "invocations", "Stage 1 invocations"
    )
    invocation = require_direct_child(
        invocations, invocation_name, "selected Stage 1 invocation"
    )
    invocation_manifest = read_regular_json(
        require_regular_file(invocation / "invocation.json")
    )
    if invocation_manifest.get("status") != "SUCCEEDED":
        # Same env-gated endgame provision as the result-status check.
        if not (
            invocation_manifest.get("status") == "FAILED"
            and os.environ.get("HE_AUDIT_ACCEPT_PARTIAL")
        ):
            raise AuditContractError(
                "selected Stage 1 invocation must be finalized SUCCEEDED"
            )
    expected_workspace_hash = (
        result.get("outputs", {}).get("workspace_sha256")
        if isinstance(result.get("outputs"), dict)
        else None
    )
    try:
        no_kit_condition = not pipeline_contract.parse_codex_config(
            str(run_manifest.get("config"))
        ).condition.kit
    except pipeline_contract.PipelineContractError as error:
        raise AuditContractError(str(error)) from error
    required_artifacts = STAGE1_REQUIRED_ARTIFACTS
    legacy_selected_invocation = _is_complete_legacy_stage1_import(
        task,
        run_manifest,
        result,
        invocation_manifest,
        str(invocation_name),
    )
    if no_kit_condition or legacy_selected_invocation:
        required_artifacts = tuple(
            name for name in required_artifacts if name != "PROOF.md"
        )
    for name in required_artifacts:
        require_regular_file(workspace / name, f"Stage 1 {name}")
    candidate_hash = pipeline_contract.sha256_tree(workspace)
    if expected_workspace_hash != candidate_hash:
        raise AuditContractError(
            "Stage 1 workspace changed after its successful result was recorded"
        )
    generation_evidence = require_generation_evidence(invocation)
    additional_generation_records = {
        "prompt.txt": require_regular_file(
            invocation / "prompt.txt", "selected Stage 1 prompt.txt"
        )
    }
    if not legacy_selected_invocation:
        additional_generation_records.update(
            {
                name: require_regular_file(
                    invocation / name, f"selected Stage 1 {name}"
                )
                for name in ("runtime-metrics.json", "usage.json")
            }
        )
    else:
        usage = invocation / "usage.json"
        if usage.exists() or usage.is_symlink():
            additional_generation_records["usage.json"] = require_regular_file(
                usage, "selected Stage 1 usage.json"
            )

    task_manifest_path = require_regular_file(task / "task.json", "task manifest")
    task_manifest = read_regular_json(task_manifest_path)
    manifest = {**task_manifest, "config": run_manifest.get("config")}
    condition = _manifest_condition(manifest)
    if manifest.get("problem_id") != problem:
        raise AuditContractError("task manifest problem ID does not match directory")
    canonical = require_regular_file(
        Path(repo) / "data/questions" / problem / TRUSTED_CANONICAL_FILENAME,
        "trusted canonical",
    )
    prompt = require_regular_file(
        Path(repo) / "data/questions" / problem / "prompt.py", "trusted prompt"
    )
    translator = require_regular_file(
        Path(repo) / "tools/py2mpy.py", "trusted translator"
    )
    supplied = CONDITIONS[condition]
    semantics = (
        _resolve_trusted_semantics(Path(repo), manifest)
        if supplied
        else None
    )
    resolution = build_resolution_and_hashes(
        require_real_directory(Path(repo), "repository root"),
        str(run_manifest["config"]),
        problem,
        condition,
        workspace,
        canonical,
        prompt,
        translator,
        semantics,
        manifest,
        task_manifest_path,
        generation_evidence,
    )
    if semantics is not None:
        manifest_semantics_hash = pipeline_contract.sha256_tree(semantics)
        accepted_manifest_hashes = {manifest_semantics_hash}
        if legacy_selected_invocation:
            legacy_semantics_hash = legacy_content_tree_hash(semantics)
            resolution["hashes"][
                "trusted_reference_semantics_legacy_sha256"
            ] = legacy_semantics_hash
            accepted_manifest_hashes.add(legacy_semantics_hash)
        resolution["hashes"][
            "trusted_reference_semantics_manifest_sha256"
        ] = manifest_semantics_hash
        resolution["integrity"][
            "manifest_reference_semantics_hash_matches_trusted"
        ] = (
            _manifest_input_hash(manifest, "reference_semantics_sha256")
            in accepted_manifest_hashes
        )
    run_manifest_path = require_regular_file(
        task.parent.parent / "run.json", "run manifest"
    )
    stage1_result_path = require_regular_file(
        stage / "result.json", "Stage 1 result"
    )
    resolution["hashes"].update(
        {
            "run_manifest_sha256": sha256_file(run_manifest_path),
            "task_manifest_sha256": sha256_file(task_manifest_path),
            "stage1_result_sha256": sha256_file(stage1_result_path),
            "stage1_invocation_sha256": sha256_file(
                invocation / "invocation.json"
            ),
            "generation_prompt_sha256": sha256_file(
                additional_generation_records["prompt.txt"]
            ),
        }
    )
    if "runtime-metrics.json" in additional_generation_records:
        resolution["hashes"]["generation_runtime_metrics_sha256"] = sha256_file(
            additional_generation_records["runtime-metrics.json"]
        )
    if "usage.json" in additional_generation_records:
        resolution["hashes"]["generation_usage_sha256"] = sha256_file(
            additional_generation_records["usage.json"]
        )
    resolution["run_id"] = run_id
    resolution["record_layout"] = (
        "legacy-selected-stage1"
        if legacy_selected_invocation
        else "pipeline-v3"
    )
    resolution["generation_root"] = str(invocation)
    resolution["run_manifest"] = str(run_manifest_path)
    resolution["task_manifest"] = str(task_manifest_path)
    resolution["stage1_result"] = str(stage1_result_path)
    resolution["stage1_invocation"] = str(invocation)
    return resolution


def _execution_directories(executions: Path) -> list[Path]:
    executions = require_real_directory(executions, "Stage 2 executions")
    children: list[Path] = []
    try:
        entries = list(os.scandir(executions))
    except OSError as error:
        raise AuditContractError(f"cannot scan Stage 2 executions: {error}") from error
    for entry in entries:
        path = Path(entry.path)
        try:
            mode = entry.stat(follow_symlinks=False).st_mode
        except OSError as error:
            raise AuditContractError(
                f"cannot inspect Stage 2 execution: {path}"
            ) from error
        if not stat.S_ISDIR(mode) or not re.fullmatch(r"[0-9]{3}", path.name):
            raise AuditContractError(
                f"invalid Stage 2 execution entry: {path}"
            )
        children.append(path)
    return sorted(children)


def prepare_stage2_execution(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    replace_selected: bool = False,
) -> Path:
    # Resolve first so an incomplete or mutated Stage 1 never allocates output.
    resolve_stage2_audit(repo, run_id, problem)
    pipeline_contract = _pipeline_contract_module()
    try:
        task, _state, _run = pipeline_contract._resolve_task_state(
            repo, run_id, problem
        )
    except pipeline_contract.PipelineContractError as error:
        raise AuditContractError(str(error)) from error
    stage = require_real_directory(task / "02-k-audit", "Stage 2")
    executions = require_real_directory(
        stage / "executions", "Stage 2 executions"
    )
    existing = _execution_directories(executions)
    selected_path = stage / "selected.json"
    if selected_path.exists() or selected_path.is_symlink():
        selected = read_regular_json(require_regular_file(selected_path))
        if (
            selected.get("status") != "AUDIT_ERROR"
            and not replace_selected
        ):
            raise AuditContractError(
                "Stage 2 has a terminal selected audit and cannot be rerun"
            )
    elif existing:
        raise AuditContractError(
            "unselected Stage 2 execution exists; recover or select it before retry"
        )
    number = len(existing) + 1
    name = f"{number:03d}"
    destination = executions / name
    try:
        destination.mkdir()
        (destination / "evidence").mkdir()
    except OSError as error:
        if destination.exists():
            try:
                destination.rmdir()
            except OSError:
                pass
        raise AuditContractError(
            f"cannot allocate Stage 2 execution {name}"
        ) from error
    return destination.resolve(strict=True)


def stage2_eligibility(
    repo: Path, run_id: str, problem: str
) -> dict[str, object]:
    pipeline_contract = _pipeline_contract_module()
    try:
        task, _state, _run = pipeline_contract._resolve_task_state(
            repo, run_id, problem
        )
        pipeline_contract.require_task_unblocked(task, "Stage 2")
    except pipeline_contract.PipelineContractError as error:
        raise AuditContractError(str(error)) from error
    stage = require_real_directory(task / "02-k-audit", "Stage 2")
    selected = read_regular_json(
        require_regular_file(stage / "selected.json", "Stage 2 selection")
    )
    relative = selected.get("relative_path")
    if not isinstance(relative, str):
        raise AuditContractError("Stage 2 selected path is malformed")
    parts = Path(relative).parts
    if len(parts) != 2 or parts[0] != "executions":
        raise AuditContractError("Stage 2 selected path escapes executions")
    execution = require_direct_child(
        require_real_directory(stage / "executions", "Stage 2 executions"),
        parts[1],
        "selected Stage 2 execution",
    )
    try:
        current_hash = pipeline_contract.sha256_tree(execution)
    except pipeline_contract.PipelineContractError as error:
        raise AuditContractError(str(error)) from error
    if current_hash != selected.get("artifact_sha256"):
        raise AuditContractError(
            "selected Stage 2 audit changed after selection"
        )
    verdict = read_regular_json(
        require_regular_file(execution / "verdict.json", "Stage 2 verdict")
    )
    if verdict.get("audit_status") != "COMPLETE":
        raise AuditContractError("Stage 2 selected audit is not complete")
    value = verdict.get("verdict")
    legitimacy = verdict.get("legitimacy")
    if (value, legitimacy) not in VALID_PAIRS:
        raise AuditContractError("Stage 2 verdict is inconsistent")
    if selected.get("status") != value:
        raise AuditContractError(
            "Stage 2 selection status differs from its verdict"
        )
    return {
        "eligible": legitimacy == "LEGIT",
        "verdict": value,
        "legitimacy": legitimacy,
        "selected_relative_path": relative,
        "selected_artifact_sha256": current_hash,
        "selected_verdict_sha256": pipeline_contract.sha256_file(
            execution / "verdict.json"
        ),
    }


def _audit_error(message: str) -> dict[str, object]:
    return {
        "audit_status": "AUDIT_ERROR",
        "verdict": None,
        "legitimacy": None,
        "error": message,
    }


def normalize_verdict(
    review_text: str,
    model_exit_code: int,
    harness_exit_code: int,
    timed_out: bool,
) -> dict[str, object]:
    if harness_exit_code != 0:
        return _audit_error(
            f"audit harness exited with status {harness_exit_code}"
        )
    if timed_out:
        return _audit_error("reviewer session timed out")
    if model_exit_code != 0:
        return _audit_error(
            f"reviewer model process exited with status {model_exit_code}"
        )
    if not isinstance(review_text, str) or not review_text.strip():
        return _audit_error("REVIEW.md is missing or empty")

    nonempty = [line.strip() for line in review_text.splitlines() if line.strip()]
    verdict_lines = [line for line in nonempty if line.startswith("VERDICT:")]
    legitimacy_lines = [
        line for line in nonempty if line.startswith("LEGITIMACY:")
    ]
    if len(verdict_lines) != 1 or len(legitimacy_lines) != 1:
        return _audit_error(
            "REVIEW.md must contain exactly one verdict and one legitimacy marker"
        )
    if len(nonempty) < 2:
        return _audit_error("REVIEW.md is missing the final marker pair")

    verdict_match = _VERDICT_MARKER.fullmatch(nonempty[-2])
    legitimacy_match = _LEGITIMACY_MARKER.fullmatch(nonempty[-1])
    if verdict_match is None or legitimacy_match is None:
        return _audit_error(
            "the final two non-empty REVIEW.md lines must be the exact marker pair"
        )
    pair = (verdict_match.group(1), legitimacy_match.group(1))
    if pair not in VALID_PAIRS:
        return _audit_error(f"inconsistent verdict and legitimacy marker pair: {pair}")
    return {
        "audit_status": "COMPLETE",
        "verdict": pair[0],
        "legitimacy": pair[1],
        "error": None,
    }


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    destination = Path(path)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            json.dump(payload, temporary, indent=2, sort_keys=True)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, destination)
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except FileNotFoundError:
                pass


def _metrics_state(path: Path) -> tuple[int, int, bool]:
    metrics = read_regular_json(path)
    model_exit_code = metrics.get("model_exit_code")
    harness_exit_code = metrics.get("harness_exit_code")
    timed_out = metrics.get("timed_out", metrics.get("timeout", False))
    if isinstance(model_exit_code, bool) or not isinstance(model_exit_code, int):
        raise AuditContractError(
            "metrics.json must contain an integer model_exit_code"
        )
    if isinstance(harness_exit_code, bool) or not isinstance(harness_exit_code, int):
        raise AuditContractError(
            "metrics.json must contain an integer harness_exit_code"
        )
    if not isinstance(timed_out, bool):
        raise AuditContractError("metrics.json timed_out must be boolean")
    return model_exit_code, harness_exit_code, timed_out


def _resolve_command(args: argparse.Namespace) -> int:
    try:
        resolution = resolve_audit(Path(args.repo), args.config, args.problem)
    except AuditContractError as error:
        print(f"audit input error: {error}", file=sys.stderr)
        return 2
    json.dump(resolution, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


def _resolve_stage2_command(args: argparse.Namespace) -> int:
    try:
        resolution = resolve_stage2_audit(
            Path(args.repo), args.run_id, args.problem
        )
    except AuditContractError as error:
        print(f"audit input error: {error}", file=sys.stderr)
        return 2
    json.dump(resolution, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


def _prepare_stage2_command(args: argparse.Namespace) -> int:
    try:
        output = prepare_stage2_execution(
            Path(args.repo),
            args.run_id,
            args.problem,
            replace_selected=args.replace_selected,
        )
    except AuditContractError as error:
        print(f"audit state error: {error}", file=sys.stderr)
        return 2
    print(output)
    return 0


def _eligibility_command(args: argparse.Namespace) -> int:
    try:
        document = stage2_eligibility(
            Path(args.repo), args.run_id, args.problem
        )
    except AuditContractError as error:
        print(f"audit state error: {error}", file=sys.stderr)
        return 2
    json.dump(document, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


def _verdict_command(args: argparse.Namespace) -> int:
    try:
        model_exit_code, harness_exit_code, timed_out = _metrics_state(
            Path(args.metrics)
        )
        review_path = require_regular_file(Path(args.review), "REVIEW.md")
        try:
            review_text = review_path.read_text()
        except (OSError, UnicodeError) as error:
            raise AuditContractError(f"cannot read REVIEW.md: {error}") from error
        payload = normalize_verdict(
            review_text,
            model_exit_code,
            harness_exit_code,
            timed_out,
        )
    except AuditContractError as error:
        payload = _audit_error(f"audit artifact error: {error}")

    try:
        write_json_atomic(Path(args.output), payload)
    except OSError as error:
        print(f"cannot write verdict JSON: {error}", file=sys.stderr)
        return 2
    if payload["audit_status"] != "COMPLETE":
        print(payload["error"], file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("--repo", required=True)
    resolve_parser.add_argument("--config", required=True)
    resolve_parser.add_argument("--problem", required=True)
    resolve_parser.set_defaults(handler=_resolve_command)

    stage2_parser = subparsers.add_parser("resolve-stage2")
    stage2_parser.add_argument("--repo", required=True)
    stage2_parser.add_argument("--run-id", required=True)
    stage2_parser.add_argument("--problem", required=True)
    stage2_parser.set_defaults(handler=_resolve_stage2_command)

    prepare_stage2_parser = subparsers.add_parser("prepare-stage2")
    prepare_stage2_parser.add_argument("--repo", required=True)
    prepare_stage2_parser.add_argument("--run-id", required=True)
    prepare_stage2_parser.add_argument("--problem", required=True)
    prepare_stage2_parser.add_argument("--replace-selected", action="store_true")
    prepare_stage2_parser.set_defaults(handler=_prepare_stage2_command)

    eligibility_parser = subparsers.add_parser("stage2-eligibility")
    eligibility_parser.add_argument("--repo", required=True)
    eligibility_parser.add_argument("--run-id", required=True)
    eligibility_parser.add_argument("--problem", required=True)
    eligibility_parser.set_defaults(handler=_eligibility_command)

    verdict_parser = subparsers.add_parser("verdict")
    verdict_parser.add_argument("--review", required=True)
    verdict_parser.add_argument("--metrics", required=True)
    verdict_parser.add_argument("--output", required=True)
    verdict_parser.set_defaults(handler=_verdict_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
