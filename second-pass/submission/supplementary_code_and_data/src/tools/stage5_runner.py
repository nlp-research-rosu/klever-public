#!/usr/bin/env python3
"""Resume the original Codex session to prove the immutable Klean target."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import klean_export, pipeline_contract, stage4_runner
from tools.stage1_runner import (
    Stage1RunnerError,
    _container_name,
    _inspect_container,
    _read_entry_metrics,
)
from tools.stage3_runner import (
    Stage3RunnerError,
    _read_regular_nofollow,
)


class Stage5RunnerError(RuntimeError):
    pass


STAGE = "05-lean-proof"
RESULT_PATTERN = re.compile(
    r"RESULT: LEAN_PROOF_COMPLETE — (\S(?:.*\S)?)"
)


@dataclass(frozen=True)
class InvocationOutcome:
    exit_code: int
    duration_s: int
    timeout_marker: bool
    oom_killed: bool
    image_id: str


@dataclass(frozen=True)
class ProtectedGeneration:
    path: Path
    status: str
    sha256: str
    selection_path: Path
    selection_data: bytes
    selection_identity: tuple[int, int]
    manifest_data: bytes
    manifest_identity: tuple[int, int]


@dataclass(frozen=True)
class ProtectedInputs:
    session_id: str
    k_reference: Path
    k_reference_sha256: str
    stage4_stage1_sha256: str
    discovery: stage4_runner.ProtectedDiscovery
    generation: ProtectedGeneration
    generation_manifest: dict[str, Any]


@dataclass(frozen=True)
class ProtectedCompletionEvidence:
    path: Path
    data: bytes
    identity: tuple[int, int]
    sha256: str
    summary: str


@dataclass(frozen=True)
class ProtectedMechanicalEvidence:
    path: Path
    data: bytes
    identity: tuple[int, int]
    sha256: str
    document: dict[str, Any]


def _parse_stage5_result_data(data: bytes) -> str:
    try:
        lines = data.decode().splitlines()
    except UnicodeDecodeError as error:
        raise Stage5RunnerError("Stage 5 final message is malformed") from error
    result_lines = [line for line in lines if line.startswith("RESULT:")]
    if len(result_lines) != 1:
        raise Stage5RunnerError(
            "Stage 5 final message must contain exactly one RESULT marker"
        )
    match = RESULT_PATTERN.fullmatch(result_lines[0])
    if match is None:
        raise Stage5RunnerError("Stage 5 RESULT marker is malformed")
    return match.group(1)


def _completion_evidence(path: Path) -> ProtectedCompletionEvidence:
    path = Path(path)
    try:
        data, identity = _read_regular_nofollow(
            path, "Stage 5 final message"
        )
    except Stage3RunnerError as error:
        raise Stage5RunnerError(str(error)) from error
    return ProtectedCompletionEvidence(
        path=path,
        data=data,
        identity=identity,
        sha256=hashlib.sha256(data).hexdigest(),
        summary=_parse_stage5_result_data(data),
    )


def parse_stage5_result(path: Path) -> str:
    return _completion_evidence(path).summary


def _run_mechanical_check(
    image_id: str,
    generation: Path,
    candidate: Path,
    *,
    docker: str,
) -> dict[str, Any]:
    if re.fullmatch(r"sha256:[0-9a-f]{64}", image_id) is None:
        raise Stage5RunnerError(
            "Stage 5 mechanical check requires an immutable image ID"
        )
    command = [
        docker,
        "run",
        "--rm",
        "--network",
        "none",
        "--pull=never",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,exec,nosuid,size=8g",
        "--memory",
        "8g",
        "--memory-swap",
        "8g",
        "--mount",
        f"type=bind,src={Path(generation).resolve()},"
        "dst=/generation,readonly",
        "--mount",
        f"type=bind,src={Path(candidate).resolve()},"
        "dst=/candidate,readonly",
        "--entrypoint",
        "python3",
        image_id,
        "/opt/humaneval/tools/stage5_mechanical_check.py",
        "--generation",
        "/generation",
        "--candidate",
        "/candidate",
    ]
    process = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode != 0:
        raise Stage5RunnerError(
            "Stage 5 mechanical-check container failed: "
            + process.stderr[-600:]
        )
    try:
        document = json.loads(process.stdout)
    except (TypeError, ValueError) as error:
        raise Stage5RunnerError(
            "Stage 5 mechanical-check output is malformed"
        ) from error
    if not isinstance(document, dict) or document.get("status") not in {
        "PASS",
        "FAIL",
        "AUDIT_ERROR",
    }:
        raise Stage5RunnerError(
            "Stage 5 mechanical-check result is malformed"
        )
    if document["status"] == "AUDIT_ERROR":
        raise Stage5RunnerError(
            "Stage 5 mechanical check hit infrastructure failure: "
            + str(document.get("error", "unknown error"))
        )
    return document


def _publish_mechanical_evidence(
    invocation: Path, document: dict[str, Any]
) -> ProtectedMechanicalEvidence:
    path = Path(invocation) / "lean-validation.json"
    if path.exists() or path.is_symlink():
        raise Stage5RunnerError(
            "Stage 5 invocation already has mechanical evidence"
        )
    data = (
        json.dumps(document, indent=2, sort_keys=True) + "\n"
    ).encode()
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)
    try:
        observed, identity = _read_regular_nofollow(
            path, "Stage 5 mechanical evidence"
        )
    except Stage3RunnerError as error:
        raise Stage5RunnerError(str(error)) from error
    if observed != data:
        raise Stage5RunnerError(
            "Stage 5 mechanical evidence changed during publication"
        )
    return ProtectedMechanicalEvidence(
        path=path,
        data=data,
        identity=identity,
        sha256=hashlib.sha256(data).hexdigest(),
        document=document,
    )


def _safe_lean_identifier(value: str) -> bool:
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*", value):
        return True
    return (
        len(value) >= 3
        and value.startswith("«")
        and value.endswith("»")
        and "\n" not in value
        and "\r" not in value
        and "«" not in value[1:-1]
        and "»" not in value[1:-1]
    )


def _json_from_bytes(data: bytes, label: str) -> dict[str, Any]:
    try:
        document = json.loads(data)
    except (TypeError, ValueError) as error:
        raise Stage5RunnerError(f"{label} is malformed") from error
    if not isinstance(document, dict):
        raise Stage5RunnerError(f"{label} must be a JSON object")
    return document


def _canonical_uuid(value: object, label: str) -> str:
    try:
        parsed = str(uuid.UUID(value))
    except (AttributeError, TypeError, ValueError) as error:
        raise Stage5RunnerError(f"{label} is not a canonical UUID") from error
    if value != parsed:
        raise Stage5RunnerError(f"{label} is not a canonical UUID")
    return parsed


def _terminal_session_uuid(
    task: Path,
    stage: str,
    *,
    kinds: set[str],
) -> str:
    label = {
        "01-k-proof": "Stage 1",
        "03-lemma-discovery": "Stage 3",
    }.get(stage, stage)
    result = pipeline_contract._read_regular_json(
        task / stage / "result.json", f"{label} terminal result"
    )
    invocation_name = result.get("invocation")
    # User-authorized endgame provision (2026-08-01): the honest-PARTIAL
    # 129 stage-1 (stage-2 CONDITIONAL CONCERNS under the registered
    # provision) is admitted when explicitly enabled.
    status_ok = result.get("status") == "SUCCEEDED" or (
        stage == "01-k-proof"
        and result.get("status") == "FAILED"
        and os.environ.get("HE_AUDIT_ACCEPT_PARTIAL")
    )
    if (
        result.get("stage") != stage
        or not status_ok
        or not isinstance(invocation_name, str)
    ):
        raise Stage5RunnerError(
            f"{label} has no successful terminal session record"
        )
    invocation_name = pipeline_contract.validate_safe_component(
        invocation_name, f"{label} terminal invocation"
    )
    invocation_path = pipeline_contract._require_direct_directory(
        task / stage / "invocations",
        invocation_name,
        f"{label} terminal invocation",
    )
    invocation = pipeline_contract._read_regular_json(
        invocation_path / "invocation.json",
        f"{label} terminal invocation manifest",
    )
    invocation_status_ok = invocation.get("status") == "SUCCEEDED" or (
        stage == "01-k-proof"
        and invocation.get("status") == "FAILED"
        and os.environ.get("HE_AUDIT_ACCEPT_PARTIAL")
    )
    if (
        invocation.get("stage") != stage
        or invocation.get("name") != invocation_name
        or not invocation_status_ok
        or invocation.get("kind") not in kinds
    ):
        raise Stage5RunnerError(
            f"{label} terminal invocation provenance is malformed"
        )
    result_uuid = _canonical_uuid(
        result.get("session_id"), f"{label} result session ID"
    )
    invocation_uuid = _canonical_uuid(
        invocation.get("session_id"),
        f"{label} invocation session ID",
    )
    if result_uuid != invocation_uuid:
        raise Stage5RunnerError(
            f"{label} terminal records name different session UUIDs"
        )
    return result_uuid


def _canonical_session_uuid(task: Path, state: Path) -> str:
    stage1_uuid = _terminal_session_uuid(
        task,
        "01-k-proof",
        kinds={"initial", "timeout-resume", "oom-resume", "terminal-resume", "infrastructure-retry"},
    )
    stage3_uuid = _terminal_session_uuid(
        task,
        "03-lemma-discovery",
        kinds={"stage-resume", "timeout-resume", "infrastructure-retry"},
    )
    if stage3_uuid != stage1_uuid:
        raise Stage5RunnerError(
            "Stage 3 terminal session differs from canonical Stage 1 session"
        )
    current_uuid = pipeline_contract._read_session_state(state)[
        "session_id"
    ]
    if current_uuid != stage1_uuid:
        raise Stage5RunnerError(
            "persisted session state differs from canonical Stage 1 session"
        )
    return stage1_uuid


def _selected_generation(
    task: Path,
    problem: str,
    *,
    stage1_workspace_sha256: str,
    stage3_discovery_manifest_sha256: str,
) -> tuple[ProtectedGeneration, dict[str, Any]]:
    stage = pipeline_contract.require_real_directory(
        task / "04-klean-generation", "Stage 4 Klean generation"
    )
    selection_path = stage / "selected.json"
    try:
        selection_data, selection_identity = _read_regular_nofollow(
            selection_path, "Stage 4 selection"
        )
    except Stage3RunnerError as error:
        raise Stage5RunnerError(str(error)) from error
    selected = _json_from_bytes(selection_data, "Stage 4 selection")
    status = selected.get("status")
    if status not in {"PASS", "KLEAN_NO_OBLIGATIONS"}:
        raise Stage5RunnerError(
            "Stage 4 has no selected passing Klean generation"
        )
    if (
        selected.get("schema_version") != pipeline_contract.SCHEMA_VERSION
        or selected.get("stage") != "04-klean-generation"
    ):
        raise Stage5RunnerError("Stage 4 selection provenance is malformed")
    relative = selected.get("relative_path")
    parts = Path(relative).parts if isinstance(relative, str) else ()
    if len(parts) != 2 or parts[0] != "generations":
        raise Stage5RunnerError("Stage 4 selected path is malformed")
    expected_candidate_sha256 = selected.get("artifact_sha256")
    if (
        not isinstance(expected_candidate_sha256, str)
        or re.fullmatch(
            r"[0-9a-f]{64}", expected_candidate_sha256
        )
        is None
    ):
        raise Stage5RunnerError(
            "Stage 4 selected candidate hash is malformed"
        )
    generation = pipeline_contract._require_direct_directory(
        stage / "generations", parts[1], "selected Stage 4 generation"
    )
    try:
        validated_sha256 = stage4_runner._validated_candidate_sha256(
            generation,
            0,
            expected_candidate_sha256=expected_candidate_sha256,
            problem=problem,
            stage1_workspace_sha256=stage1_workspace_sha256,
            stage3_discovery_manifest_sha256=(
                stage3_discovery_manifest_sha256
            ),
        )
        preflight, _preflight_data = stage4_runner._candidate_json(
            generation, "preflight.json"
        )
    except (
        pipeline_contract.PipelineContractError,
        stage4_runner.Stage4RunnerError,
    ) as error:
        raise Stage5RunnerError(
            f"selected Stage 4 generation is invalid: {error}"
        ) from error
    if preflight.get("status") != status:
        raise Stage5RunnerError(
            "Stage 4 selection status differs from its candidate"
        )
    manifest_path = generation / "generator-manifest.json"
    try:
        manifest_data, manifest_identity = _read_regular_nofollow(
            manifest_path, "selected Stage 4 generator manifest"
        )
        after_selection_data, after_selection_identity = (
            _read_regular_nofollow(selection_path, "Stage 4 selection")
        )
    except Stage3RunnerError as error:
        raise Stage5RunnerError(str(error)) from error
    if (
        after_selection_data != selection_data
        or after_selection_identity != selection_identity
        or pipeline_contract.sha256_tree(generation) != validated_sha256
    ):
        raise Stage5RunnerError(
            "Stage 4 selection changed during protected validation"
        )
    manifest = _json_from_bytes(
        manifest_data, "selected Stage 4 generator manifest"
    )
    return (
        ProtectedGeneration(
            path=generation,
            status=status,
            sha256=validated_sha256,
            selection_path=selection_path,
            selection_data=selection_data,
            selection_identity=selection_identity,
            manifest_data=manifest_data,
            manifest_identity=manifest_identity,
        ),
        manifest,
    )


def _protected_inputs(
    task: Path, state: Path, problem: str
) -> ProtectedInputs:
    session_id = _canonical_session_uuid(task, state)
    try:
        k_reference, k_reference_sha256 = (
            stage4_runner._stage1_workspace(task)
        )
        discovery = stage4_runner._protected_stage3_discovery(task)
    except (
        pipeline_contract.PipelineContractError,
        stage4_runner.Stage4RunnerError,
    ) as error:
        raise Stage5RunnerError(str(error)) from error
    try:
        stage4_stage1_sha256 = klean_export.tree_digest(k_reference)
    except (OSError, klean_export.KleanExportError) as error:
        raise Stage5RunnerError(
            "cannot hash the protected Stage 1 input"
        ) from error
    generation, manifest = _selected_generation(
        task,
        problem,
        stage1_workspace_sha256=stage4_stage1_sha256,
        stage3_discovery_manifest_sha256=discovery.sha256,
    )
    if _canonical_session_uuid(task, state) != session_id:
        raise Stage5RunnerError(
            "canonical session changed during Stage 5 input validation"
        )
    return ProtectedInputs(
        session_id=session_id,
        k_reference=k_reference,
        k_reference_sha256=k_reference_sha256,
        stage4_stage1_sha256=stage4_stage1_sha256,
        discovery=discovery,
        generation=generation,
        generation_manifest=manifest,
    )


def _timeout_policy(run_manifest: dict[str, Any]) -> tuple[int, int]:
    try:
        initial_s = int(run_manifest["timeouts"]["lean_initial_s"])
        total_s = int(run_manifest["timeouts"]["lean_total_s"])
    except (KeyError, TypeError, ValueError) as error:
        raise Stage5RunnerError(
            "Stage 5 timeout policy is malformed"
        ) from error
    if initial_s < 3600 or total_s < initial_s:
        raise Stage5RunnerError("Stage 5 timeout policy is unsupported")
    return initial_s, total_s


def inspect_stage5(
    repo: Path, run_id: str, problem: str
) -> dict[str, Any]:
    repo = pipeline_contract.require_real_directory(
        Path(repo), "repository"
    )
    task, state, run_manifest = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    pipeline_contract.require_task_unblocked(task, "Stage 5")
    protected = _protected_inputs(task, state, problem)
    initial_s, total_s = _timeout_policy(run_manifest)
    return {
        "run_id": run_id,
        "problem": problem,
        "status": protected.generation.status,
        "session_id": protected.session_id,
        "initial_timeout_s": initial_s,
        "total_timeout_s": total_s,
        "stage1_reference": str(protected.k_reference),
        "stage3_discovery": str(protected.discovery.path),
        "stage4_generation": str(protected.generation.path),
        "workspace": str(task / f"{STAGE}/workspace"),
        "prompt": "klean-prove.md",
    }


def _initialize_workspace(
    workspace: Path, generation_manifest: dict[str, Any], problem: str
) -> None:
    target = generation_manifest.get("target")
    if not isinstance(target, dict):
        raise Stage5RunnerError("generator target manifest is malformed")
    statement = target.get("statement")
    declaration = target.get("declaration")
    parameters = target.get("parameters")
    if not isinstance(statement, str) or not statement:
        raise Stage5RunnerError("generated target statement is missing")
    if not isinstance(declaration, str) or "." not in declaration:
        raise Stage5RunnerError("generated target declaration is malformed")
    if not isinstance(parameters, list):
        raise Stage5RunnerError("generated target parameters are malformed")
    normalized_parameters: list[tuple[str, str, str, list[str]]] = []
    for parameter in parameters:
        if not isinstance(parameter, dict):
            raise Stage5RunnerError(
                "generated target parameter is malformed"
            )
        name = parameter.get("name")
        lean_type = parameter.get("type")
        kore_symbol = parameter.get("kore_symbol")
        source_rule_ids = parameter.get("source_rule_ids")
        binding_sha256 = parameter.get("binding_sha256")
        if (
            not isinstance(name, str)
            or not _safe_lean_identifier(name)
            or not isinstance(lean_type, str)
            or not lean_type.strip()
            or "\n" in lean_type
            or not isinstance(kore_symbol, str)
            or not kore_symbol
            or "\n" in kore_symbol
            or not isinstance(source_rule_ids, list)
            or not source_rule_ids
            or not all(
                isinstance(source_rule_id, str) and source_rule_id
                for source_rule_id in source_rule_ids
            )
        ):
            raise Stage5RunnerError("generated target parameter is unsafe")
        binding = {
            "kore_symbol": kore_symbol,
            "name": name,
            "type": lean_type,
            "source_rule_ids": source_rule_ids,
        }
        expected_binding_sha256 = hashlib.sha256(
            json.dumps(
                binding, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
        if binding_sha256 != expected_binding_sha256:
            raise Stage5RunnerError(
                "generated target parameter binding changed"
            )
        normalized_parameters.append(
            (name, lean_type.strip(), kore_symbol, source_rule_ids)
        )
    expected_statement = " ".join(
        (
            declaration,
            *(
                name
                for name, _lean_type, _kore_symbol, _source_rule_ids
                in normalized_parameters
            ),
        )
    )
    if statement != expected_statement:
        raise Stage5RunnerError(
            "generated target application is inconsistent"
        )
    module = declaration.rsplit(".", 1)[0]
    package = f"klean-{problem.lower()}"
    lakefile = (
        "import Lake\n"
        "open Lake DSL\n"
        'package "proof"\n'
        f'require «{package}» from "./Base"\n'
        "@[default_target]\n"
        "lean_lib Proof\n"
    )
    toolchain = generation_manifest.get("toolchain", {}).get(
        "lean_toolchain"
    )
    if not isinstance(toolchain, str) or not toolchain:
        raise Stage5RunnerError("generated Lean toolchain is missing")
    existing = list(workspace.iterdir())
    if existing:
        required = {"Proof.lean", "lakefile.lean", "lean-toolchain"}
        if not required.issubset(path.name for path in existing):
            raise Stage5RunnerError(
                "Lean workspace is partially initialized"
            )
        try:
            pipeline_contract.require_regular_file(
                workspace / "Proof.lean", "Stage 5 proof module"
            )
            lakefile_path = pipeline_contract.require_regular_file(
                workspace / "lakefile.lean", "Stage 5 Lean lakefile"
            )
            toolchain_path = pipeline_contract.require_regular_file(
                workspace / "lean-toolchain",
                "Stage 5 Lean toolchain",
            )
        except pipeline_contract.PipelineContractError as error:
            raise Stage5RunnerError(
                "Lean workspace contains a linked or non-regular "
                "immutable file"
            ) from error
        if lakefile_path.read_text() != lakefile:
            raise Stage5RunnerError("immutable Lean lakefile changed")
        if toolchain_path.read_text() != toolchain + "\n":
            raise Stage5RunnerError("immutable Lean toolchain changed")
        return
    workspace.joinpath("lakefile.lean").write_text(lakefile)
    workspace.joinpath("lean-toolchain").write_text(toolchain + "\n")
    parameter_stubs = "".join(
        "/- KORE symbol: "
        + kore_symbol
        + "; frozen source obligations: "
        + ", ".join(source_rule_ids)
        + ". Replace this stub with its honest total meaning from the frozen "
        "K semantics. -/\n"
        + f"axiom {name} : {lean_type}\n"
        for name, lean_type, kore_symbol, source_rule_ids
        in normalized_parameters
    )
    if parameter_stubs:
        parameter_stubs += "\n"
    workspace.joinpath("Proof.lean").write_text(
        f"import {module}\n\n"
        "namespace Proof\n\n"
        f"{parameter_stubs}"
        "theorem final :\n"
        f"    {statement} := by\n"
        "  sorry\n\n"
        "end Proof\n"
    )


def _verify_input_snapshots(
    task: Path,
    state: Path,
    problem: str,
    expected: ProtectedInputs,
) -> None:
    if _canonical_session_uuid(task, state) != expected.session_id:
        raise Stage5RunnerError(
            "canonical Stage 1/3 session changed during Stage 5"
        )
    try:
        k_reference, k_reference_sha256 = (
            stage4_runner._stage1_workspace(task)
        )
        discovery = stage4_runner._protected_stage3_discovery(task)
    except (
        pipeline_contract.PipelineContractError,
        stage4_runner.Stage4RunnerError,
    ) as error:
        raise Stage5RunnerError(
            f"protected Stage 1 or Stage 3 input changed: {error}"
        ) from error
    if (
        k_reference != expected.k_reference
        or k_reference_sha256 != expected.k_reference_sha256
    ):
        raise Stage5RunnerError(
            "protected Stage 1 input changed during Stage 5"
        )
    try:
        stage4_stage1_sha256 = klean_export.tree_digest(k_reference)
    except (OSError, klean_export.KleanExportError) as error:
        raise Stage5RunnerError(
            "protected Stage 1 input changed during Stage 5"
        ) from error
    if stage4_stage1_sha256 != expected.stage4_stage1_sha256:
        raise Stage5RunnerError(
            "protected Stage 1 input changed during Stage 5"
        )
    if discovery != expected.discovery:
        raise Stage5RunnerError(
            "protected Stage 3 input changed during Stage 5"
        )
    try:
        generation, manifest = _selected_generation(
            task,
            problem,
            stage1_workspace_sha256=stage4_stage1_sha256,
            stage3_discovery_manifest_sha256=discovery.sha256,
        )
    except (
        pipeline_contract.PipelineContractError,
        Stage5RunnerError,
    ) as error:
        raise Stage5RunnerError(
            f"protected Stage 4 input changed: {error}"
        ) from error
    if (
        generation != expected.generation
        or manifest != expected.generation_manifest
    ):
        raise Stage5RunnerError(
            "protected Stage 4 input changed during Stage 5"
        )
    if _canonical_session_uuid(task, state) != expected.session_id:
        raise Stage5RunnerError(
            "canonical Stage 1/3 session changed during Stage 5"
        )


def _verify_post_model_integrity(
    task: Path,
    state: Path,
    problem: str,
    invocation: pipeline_contract.Invocation,
    protected: ProtectedInputs,
    *,
    require_trace: bool,
) -> None:
    _verify_input_snapshots(task, state, problem, protected)
    canonical_session = _canonical_session_uuid(task, state)
    if (
        invocation.session_id != canonical_session
        or invocation.kind not in {"stage-resume", "timeout-resume"}
    ):
        raise Stage5RunnerError(
            "Stage 5 invocation does not resume the persisted session"
        )
    trace = invocation.path / "codex-trace"
    if trace.exists() or trace.is_symlink():
        if (
            pipeline_contract.validate_session_trace_tree(
                trace, canonical_session
            )
            != canonical_session
        ):
            raise Stage5RunnerError(
                "Stage 5 trace session does not match persisted session"
            )
    elif require_trace:
        raise Stage5RunnerError(
            "successful Stage 5 invocation has no session trace"
        )


def _run_one(
    repo: Path,
    run_id: str,
    problem: str,
    invocation: pipeline_contract.Invocation,
    run_manifest: dict[str, Any],
    state: Path,
    k_reference: Path,
    discovery: Path,
    generation: Path,
    *,
    docker: str,
) -> InvocationOutcome:
    prompt = (
        repo / "prompts/klean-prove.md"
        if invocation.name == "001-initial"
        else repo / "prompts/timeout-resume.md"
    )
    pipeline_contract.record_invocation_prompt(invocation.path, prompt)
    task = repo / f"runs/{run_id}/tasks/{problem}"
    workspace = task / f"{STAGE}/workspace"
    command = [
        docker,
        "compose",
        "-f",
        str(repo / "docker/codex/docker-compose.yml"),
    ]
    kit = bool(run_manifest["condition"]["kit"])
    if kit:
        command.extend(
            ["-f", str(repo / "docker/codex/docker-compose.kit.yml")]
        )
    command.extend(
        [
            "-f",
            str(repo / "docker/codex/docker-compose.klean.yml"),
            "run",
            "--name",
            _container_name(
                run_id, problem, f"lean-{invocation.name}"
            ),
            "-T",
            "runner",
        ]
    )
    name = command[command.index("--name") + 1]
    environment = os.environ.copy()
    environment.update(
        {
            "WORKSPACE_DIR": str(workspace),
            "INVOCATION_DIR": str(invocation.path),
            "CODEX_HOME_DIR": str(state / "codex-home"),
            "PROMPT_PATH": str(prompt),
            "K_REFERENCE_DIR": str(k_reference),
            "STAGE3_DISCOVERY_PATH": str(discovery),
            "GENERATED_DIR": str(generation / "generated"),
            "LEAN_LAKEFILE_PATH": str(workspace / "lakefile.lean"),
            "LEAN_TOOLCHAIN_PATH": str(workspace / "lean-toolchain"),
            "INVOCATION_KIND": invocation.kind,
            "SESSION_ID": invocation.session_id or "",
            "MODEL": str(run_manifest["model"]),
            "EFFORT": str(run_manifest["effort"]),
            "TIMEOUT_S": str(invocation.allocation_s),
            "KIT": "1" if kit else "0",
        }
    )
    process = subprocess.run(command, env=environment)
    try:
        try:
            inspection = _inspect_container(docker, name)
        except Stage1RunnerError:
            return InvocationOutcome(
                exit_code=(
                    process.returncode if process.returncode != 0 else 70
                ),
                duration_s=0,
                timeout_marker=False,
                oom_killed=False,
                image_id="UNAVAILABLE",
            )
    finally:
        subprocess.run(
            [docker, "rm", "-f", name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    try:
        metrics = _read_entry_metrics(invocation.path / "metrics.json")
    except (
        pipeline_contract.PipelineContractError,
        Stage1RunnerError,
    ):
        return InvocationOutcome(
            exit_code=inspection["exit_code"] or 70,
            duration_s=0,
            timeout_marker=False,
            oom_killed=inspection["oom_killed"],
            image_id=inspection["image_id"],
        )
    consistent = (
        process.returncode == inspection["exit_code"]
        and metrics["final_exit_code"] == inspection["exit_code"]
    )
    return InvocationOutcome(
        exit_code=inspection["exit_code"] if consistent else 70,
        duration_s=metrics["duration_s"],
        timeout_marker=(
            metrics["timeout_marker"] if consistent else False
        ),
        oom_killed=(
            inspection["oom_killed"] or metrics["oom_killed"]
        ),
        image_id=inspection["image_id"],
    )


def run_stage5(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    docker: str = "docker",
) -> dict[str, Any]:
    repo = pipeline_contract.require_real_directory(
        Path(repo), "repository"
    )
    task, state, run_manifest = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    pipeline_contract.require_task_unblocked(task, "Stage 5")
    if bool(run_manifest["condition"]["kit"]):
        os.environ["KIT_SKILLS_PATH"] = str(
            pipeline_contract.resolve_stage_kit_skills(repo, run_id, problem)
        )
    _initial_s, total_s = _timeout_policy(run_manifest)
    protected = _protected_inputs(task, state, problem)
    if protected.generation.status == "KLEAN_NO_OBLIGATIONS":
        return {
            "status": "KLEAN_NO_OBLIGATIONS",
            "skipped": True,
        }
    workspace = task / f"{STAGE}/workspace"
    _initialize_workspace(
        workspace, protected.generation_manifest, problem
    )
    _verify_input_snapshots(task, state, problem, protected)
    while True:
        invocation = pipeline_contract.prepare_invocation(
            repo, run_id, problem, STAGE
        )
        _verify_post_model_integrity(
            task,
            state,
            problem,
            invocation,
            protected,
            require_trace=False,
        )
        outcome = _run_one(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            protected.k_reference,
            protected.discovery.path,
            protected.generation.path,
            docker=docker,
        )
        exit_code = outcome.exit_code
        candidate_success = (
            exit_code == 0
            and not outcome.timeout_marker
            and not outcome.oom_killed
        )
        completion: ProtectedCompletionEvidence | None = None
        mechanical: ProtectedMechanicalEvidence | None = None
        if candidate_success:
            try:
                completion = _completion_evidence(
                    invocation.path / "codex-last.txt"
                )
            except (
                pipeline_contract.PipelineContractError,
                Stage5RunnerError,
            ):
                exit_code = 1
        if exit_code == 0 and completion is not None:
            _verify_post_model_integrity(
                task,
                state,
                problem,
                invocation,
                protected,
                require_trace=True,
            )
            mechanical_document = _run_mechanical_check(
                outcome.image_id,
                protected.generation.path,
                workspace,
                docker=docker,
            )
            mechanical = _publish_mechanical_evidence(
                invocation.path, mechanical_document
            )
            if mechanical_document["status"] != "PASS":
                exit_code = 1
            else:
                try:
                    observed_generation = klean_export.tree_digest(
                        protected.generation.path
                    )
                    observed_candidate = klean_export.tree_digest(workspace)
                except (OSError, klean_export.KleanExportError) as error:
                    raise Stage5RunnerError(
                        "cannot verify Stage 5 mechanical input hashes"
                    ) from error
                if (
                    mechanical_document.get("generation_sha256")
                    != observed_generation
                    or mechanical_document.get("candidate_sha256")
                    != observed_candidate
                ):
                    raise Stage5RunnerError(
                        "Stage 5 mechanical check bound different inputs"
                    )
        successful = (
            exit_code == 0
            and not outcome.timeout_marker
            and not outcome.oom_killed
        )
        expected_evidence = None
        if successful and completion is not None and mechanical is not None:
            expected_evidence = {
                "codex-last.txt": completion.sha256,
                "lean-validation.json": mechanical.sha256,
            }

        def prepublication_guard() -> None:
            _verify_post_model_integrity(
                task,
                state,
                problem,
                invocation,
                protected,
                require_trace=successful,
            )
            if successful and completion is not None:
                current = _completion_evidence(completion.path)
                if (
                    current.data != completion.data
                    or current.identity != completion.identity
                    or current.sha256 != completion.sha256
                ):
                    raise Stage5RunnerError(
                        "Stage 5 completion evidence changed before "
                        "publication"
                    )
            if successful and mechanical is not None:
                try:
                    current_data, current_identity = _read_regular_nofollow(
                        mechanical.path, "Stage 5 mechanical evidence"
                    )
                    current_candidate = klean_export.tree_digest(workspace)
                    current_generation = klean_export.tree_digest(
                        protected.generation.path
                    )
                except (
                    Stage3RunnerError,
                    OSError,
                    klean_export.KleanExportError,
                ) as error:
                    raise Stage5RunnerError(
                        "Stage 5 mechanical evidence changed before "
                        "publication"
                    ) from error
                if (
                    current_data != mechanical.data
                    or current_identity != mechanical.identity
                    or hashlib.sha256(current_data).hexdigest()
                    != mechanical.sha256
                    or current_candidate
                    != mechanical.document.get("candidate_sha256")
                    or current_generation
                    != mechanical.document.get("generation_sha256")
                ):
                    raise Stage5RunnerError(
                        "Stage 5 mechanical evidence changed before "
                        "publication"
                    )

        result = pipeline_contract.finalize_invocation(
            repo,
            run_id,
            problem,
            STAGE,
            invocation.name,
            exit_code=exit_code,
            duration_s=outcome.duration_s,
            timeout_marker=outcome.timeout_marker,
            oom_killed=outcome.oom_killed,
            image_id=outcome.image_id,
            prepublication_guard=prepublication_guard,
            expected_evidence=expected_evidence,
        )
        if (
            result["status"] == "TIMEOUT"
            and invocation.name == "001-initial"
            and total_s > invocation.allocation_s
        ):
            continue
        return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--print-config", action="store_true")
    parser.add_argument("run_id")
    parser.add_argument("problem")
    arguments = parser.parse_args(argv)
    try:
        if arguments.print_config:
            print(
                json.dumps(
                    inspect_stage5(
                        arguments.repo,
                        arguments.run_id,
                        arguments.problem,
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        result = run_stage5(
            arguments.repo, arguments.run_id, arguments.problem
        )
    except (
        pipeline_contract.PipelineContractError,
        Stage1RunnerError,
        Stage3RunnerError,
        stage4_runner.Stage4RunnerError,
        Stage5RunnerError,
    ) as error:
        print(f"Stage 5 failed: {error}", file=sys.stderr)
        return 2
    return 0 if result["status"] in {
        "SUCCEEDED",
        "KLEAN_NO_OBLIGATIONS",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
