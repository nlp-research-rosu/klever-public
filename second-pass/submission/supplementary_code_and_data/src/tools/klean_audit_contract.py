#!/usr/bin/env python3
"""Resolve immutable Stage 6 inputs and allocate independent Klean audits."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import (
    audit_contract,
    klean_export,
    pipeline_contract,
    stage4_runner,
    stage6_resolution_contract,
)


class KleanAuditContractError(RuntimeError):
    pass


_STAGE6_RESOLUTION_KEYS = stage6_resolution_contract.RESOLUTION_KEYS


def _canonical_json_sha256(document: Any) -> str:
    return stage6_resolution_contract.canonical_json_sha256(document)


def _validate_sha256(value: object, label: str) -> str:
    try:
        return stage6_resolution_contract.validate_sha256(
            value, label
        )
    except (
        stage6_resolution_contract.Stage6ResolutionContractError
    ) as error:
        raise KleanAuditContractError(str(error)) from error


def _stage6_audit_input(
    resolution: dict[str, Any],
) -> dict[str, Any]:
    return stage6_resolution_contract.build_audit_input(resolution)


def verify_stage6_audit_input(
    document: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    try:
        return stage6_resolution_contract.verify_audit_input(document)
    except (
        stage6_resolution_contract.Stage6ResolutionContractError
    ) as error:
        raise KleanAuditContractError(str(error)) from error


def _translate(error: Exception) -> KleanAuditContractError:
    return KleanAuditContractError(str(error))


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        return pipeline_contract._read_regular_json(path, label)
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error


def _selected(
    task: Path, stage_name: str, container_name: str
) -> tuple[Path, dict[str, Any]]:
    try:
        stage = pipeline_contract.require_real_directory(
            task / stage_name, stage_name
        )
        selected = pipeline_contract._read_regular_json(
            stage / "selected.json", f"{stage_name} selection"
        )
        relative = selected.get("relative_path")
        parts = Path(relative).parts if isinstance(relative, str) else ()
        if len(parts) != 2 or parts[0] != container_name:
            raise KleanAuditContractError(
                f"{stage_name} selected path is malformed"
            )
        candidate = pipeline_contract._require_direct_directory(
            stage / container_name,
            parts[1],
            f"selected {stage_name} output",
        )
        if (
            pipeline_contract.sha256_tree(candidate)
            != selected.get("artifact_sha256")
        ):
            noun = (
                "generation"
                if stage_name == "04-klean-generation"
                else "audit"
            )
            raise KleanAuditContractError(
                f"selected {stage_name} {noun} changed after selection"
            )
        return candidate, selected
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error


def _require_stage5(task: Path) -> tuple[Path, Path, dict[str, Any]]:
    try:
        stage = pipeline_contract.require_real_directory(
            task / "05-lean-proof", "Stage 5"
        )
        result = pipeline_contract._read_regular_json(
            stage / "result.json", "Stage 5 result"
        )
        if result.get("status") != "SUCCEEDED":
            raise KleanAuditContractError(
                "Stage 5 must be SUCCEEDED before proof-bearing audit"
            )
        workspace = pipeline_contract.require_real_directory(
            stage / "workspace", "Stage 5 Lean workspace"
        )
        invocation_name = pipeline_contract.validate_safe_component(
            result.get("invocation"), "Stage 5 invocation"
        )
        invocation = pipeline_contract._require_direct_directory(
            stage / "invocations",
            invocation_name,
            "successful Stage 5 invocation",
        )
        invocation_manifest = pipeline_contract._read_regular_json(
            invocation / "invocation.json", "Stage 5 invocation manifest"
        )
        if (
            invocation_manifest.get("status") != "SUCCEEDED"
            or invocation_manifest.get("name") != invocation_name
            or invocation_manifest.get("stage") != "05-lean-proof"
            or invocation_manifest.get("session_id")
            != result.get("session_id")
        ):
            raise KleanAuditContractError(
                "selected Stage 5 invocation is not successful"
            )
        for name in ("metrics.json", "codex-output.log", "codex-last.txt"):
            pipeline_contract.require_regular_file(
                invocation / name, f"Stage 5 {name}"
            )
        pipeline_contract._walk_regular_files(
            invocation / "codex-trace", "Stage 5 Codex trace"
        )
        for name in ("Proof.lean", "lakefile.lean", "lean-toolchain"):
            pipeline_contract.require_regular_file(
                workspace / name, f"Stage 5 {name}"
            )
        current_outputs = pipeline_contract._invocation_output_hashes(
            invocation, workspace
        )
        result_outputs = result.get("outputs")
        invocation_outputs = invocation_manifest.get("outputs")
        if (
            current_outputs.get("workspace_sha256")
            != (
                result_outputs.get("workspace_sha256")
                if isinstance(result_outputs, dict)
                else None
            )
            or current_outputs.get("workspace_sha256")
            != (
                invocation_outputs.get("workspace_sha256")
                if isinstance(invocation_outputs, dict)
                else None
            )
        ):
            raise KleanAuditContractError(
                "Lean workspace changed after Stage 5 succeeded"
            )
        if (
            current_outputs.get("evidence")
            != (
                result_outputs.get("evidence")
                if isinstance(result_outputs, dict)
                else None
            )
            or current_outputs.get("evidence")
            != (
                invocation_outputs.get("evidence")
                if isinstance(invocation_outputs, dict)
                else None
            )
        ):
            raise KleanAuditContractError(
                "Stage 5 invocation evidence changed after success"
            )
        return workspace, invocation, result
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error


def _stage1_source_hashes(workspace: Path) -> dict[str, str]:
    try:
        return {
            path.relative_to(workspace).as_posix(): (
                pipeline_contract.sha256_file(path)
            )
            for path in pipeline_contract._walk_regular_files(
                workspace, "Stage 1 source workspace"
            )
        }
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error


def _generation_producer_sources(
    repo: Path, generator_manifest: dict[str, Any]
) -> tuple[Path, str]:
    provenance = generator_manifest.get("provenance")
    image_id = (
        provenance.get("generator_image_id")
        if isinstance(provenance, dict)
        else None
    )
    if not isinstance(image_id, str) or not image_id.startswith("sha256:"):
        raise KleanAuditContractError(
            "generator image ID is missing from Stage 4 provenance"
        )
    image_key = image_id.removeprefix("sha256:")
    try:
        image_key = pipeline_contract.validate_safe_component(
            image_key, "generator image ID"
        )
        bundle = pipeline_contract._require_direct_directory(
            repo / "data/stage4-producer-sources",
            image_key,
            "Stage 4 producer source bundle",
        )
        source_manifest = pipeline_contract._read_regular_json(
            bundle / "source-manifest.json",
            "Stage 4 producer source manifest",
        )
        expected_files = {
            "klean_export.py": generator_manifest.get("exporter_sha256"),
            "klean.py": generator_manifest.get("klean_py_sha256"),
        }
        if (
            set(source_manifest) != {
                "schema_version",
                "generator_image_id",
                "files",
            }
            or source_manifest.get("schema_version") != 1
            or source_manifest.get("generator_image_id") != image_id
            or source_manifest.get("files") != expected_files
        ):
            raise KleanAuditContractError(
                "Stage 4 producer source manifest differs from generator "
                "provenance"
            )
        observed_names = {
            path.relative_to(bundle).as_posix()
            for path in pipeline_contract._walk_regular_files(
                bundle, "Stage 4 producer source bundle"
            )
        }
        if observed_names != {
            "source-manifest.json",
            "klean_export.py",
            "klean.py",
        }:
            raise KleanAuditContractError(
                "Stage 4 producer source bundle has unexpected files"
            )
        for name, expected in expected_files.items():
            digest = _validate_sha256(
                expected, f"Stage 4 producer source {name} SHA-256"
            )
            source = pipeline_contract.require_regular_file(
                bundle / name, f"Stage 4 producer source {name}"
            )
            if pipeline_contract.sha256_file(source) != digest:
                raise KleanAuditContractError(
                    f"Stage 4 producer source {name} SHA-256 differs "
                    "from generator provenance"
                )
        return bundle, pipeline_contract.sha256_tree(bundle)
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error


def resolve_stage6_audit(
    repo: Path, run_id: str, problem: str
) -> dict[str, Any]:
    """Resolve and re-hash every frozen input to the Stage 6 audit."""

    try:
        task, _state, run = pipeline_contract._resolve_task_state(
            repo, run_id, problem
        )
        pipeline_contract.require_task_unblocked(task, "Stage 6")
        k_stage = pipeline_contract.require_real_directory(
            task / "01-k-proof", "Stage 1"
        )
        k_workspace = pipeline_contract.require_real_directory(
            k_stage / "workspace", "Stage 1 K workspace"
        )
        k_result = pipeline_contract._read_regular_json(
            k_stage / "result.json", "Stage 1 result"
        )
        if k_result.get("status") != "SUCCEEDED":
            # User-authorized endgame provision (2026-08-01): the
            # honest-PARTIAL 129 stage-1 (stage-2 CONDITIONAL CONCERNS
            # under the registered provision) is admitted when
            # explicitly enabled.
            if not (
                k_result.get("status") == "FAILED"
                and os.environ.get("HE_AUDIT_ACCEPT_PARTIAL")
            ):
                raise KleanAuditContractError("Stage 1 is not successful")
        k_hash = pipeline_contract.sha256_tree(k_workspace)
        if (
            not isinstance(k_result.get("outputs"), dict)
            or k_result["outputs"].get("workspace_sha256") != k_hash
        ):
            raise KleanAuditContractError(
                "Stage 1 K workspace changed after success"
            )
        stage1_export_hash = klean_export.tree_digest(k_workspace)
        stage1_source_hashes = _stage1_source_hashes(k_workspace)

        k_audit, k_audit_selection = _selected(
            task, "02-k-audit", "executions"
        )
        k_verdict = pipeline_contract._read_regular_json(
            k_audit / "verdict.json", "Stage 2 verdict"
        )
        if (
            k_verdict.get("audit_status") != "COMPLETE"
            or k_verdict.get("legitimacy") != "LEGIT"
            or k_verdict.get("verdict") not in {"PASS", "CONCERNS"}
        ):
            raise KleanAuditContractError(
                "Stage 2 must have a selected LEGIT verdict"
            )

        try:
            discovery = stage4_runner._protected_stage3_discovery(task)
        except stage4_runner.Stage4RunnerError as error:
            raise KleanAuditContractError(str(error)) from error

        generation, generation_selection = _selected(
            task, "04-klean-generation", "generations"
        )
        generation_status = generation_selection.get("status")
        if generation_status not in {
            "PASS",
            "KLEAN_NO_OBLIGATIONS",
        }:
            raise KleanAuditContractError(
                "Stage 4 must have a selected passing Klean generation"
            )
        preflight = pipeline_contract._read_regular_json(
            generation / "preflight.json", "Stage 4 preflight"
        )
        if preflight.get("status") != generation_status:
            raise KleanAuditContractError(
                "Stage 4 selection status differs from its preflight"
            )
        generator_manifest = pipeline_contract._read_regular_json(
            generation / "generator-manifest.json", "generator manifest"
        )
        generation_producer_sources, producer_sources_hash = (
            _generation_producer_sources(repo, generator_manifest)
        )
        generated = pipeline_contract.require_real_directory(
            generation / "generated", "generated Klean project"
        )
        generated_hash = klean_export.tree_digest(generated)
        if generator_manifest.get("generated_tree_sha256") != generated_hash:
            raise KleanAuditContractError(
                "selected Stage 4 generation changed after preflight"
            )
        provenance = generator_manifest.get("provenance")
        if (
            not isinstance(provenance, dict)
            or provenance.get("stage1_workspace_sha256")
            != stage1_export_hash
            or provenance.get("stage3_discovery_manifest_sha256")
            != discovery.sha256
        ):
            raise KleanAuditContractError(
                "selected Stage 4 generation provenance is invalid"
            )
        target = generator_manifest.get("target")
        if generation_status == "PASS" and not isinstance(target, dict):
            raise KleanAuditContractError(
                "Stage 4 target manifest is malformed"
            )
        if (
            generation_status == "KLEAN_NO_OBLIGATIONS"
            and target is not None
        ):
            raise KleanAuditContractError(
                "no-obligation Stage 4 generation has an unexpected target"
            )

        lean_workspace: Path | None = None
        lean_invocation: Path | None = None
        lean_result: dict[str, Any] | None = None
        if generation_status == "PASS":
            mode = "CLASSIFICATION_AND_PROOF"
            lean_workspace, lean_invocation, lean_result = (
                _require_stage5(task)
            )
        else:
            mode = "CLASSIFICATION_ONLY"
            stage5_result = task / "05-lean-proof/result.json"
            if stage5_result.exists() or stage5_result.is_symlink():
                raise KleanAuditContractError(
                    "KLEAN_NO_OBLIGATIONS must not have a Stage 5 result"
                )
        condition = run.get("condition")
        if not isinstance(condition, dict):
            raise KleanAuditContractError("run condition is malformed")
        resolved = {
            "schema_version": stage6_resolution_contract.SCHEMA_VERSION,
            "run_id": run_id,
            "problem_id": problem,
            "condition": condition.get("name"),
            "mode": mode,
            "semantics_mode": (
                "SUPPLIED_SEMANTICS"
                if condition.get("semantics") is True
                else "GENERATED_SEMANTICS"
            ),
            "k_workspace": str(k_workspace),
            "k_audit": str(k_audit),
            "discovery_manifest": str(discovery.path),
            "klean_generation": str(generation),
            "generation_producer_sources": str(
                generation_producer_sources
            ),
            "lean_workspace": (
                str(lean_workspace)
                if lean_workspace is not None
                else None
            ),
            "lean_invocation": (
                str(lean_invocation)
                if lean_invocation is not None
                else None
            ),
            "target": target,
            "stage1_source_hashes": stage1_source_hashes,
            "trust_inventory": str(
                pipeline_contract.require_regular_file(
                    generation / "trust-inventory.json",
                    "Stage 4 trust inventory",
                )
            ),
            "hashes": {
                "k_workspace_sha256": k_hash,
                "stage1_export_sha256": stage1_export_hash,
                "discovery_manifest_sha256": discovery.sha256,
                "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
                "klean_generation_sha256": pipeline_contract.sha256_tree(
                    generation
                ),
                "generation_producer_sources_sha256": (
                    producer_sources_hash
                ),
                "generated_tree_sha256": generated_hash,
                "lean_workspace_sha256": (
                    pipeline_contract.sha256_tree(lean_workspace)
                    if lean_workspace is not None
                    else None
                ),
                "lean_invocation_sha256": (
                    pipeline_contract.sha256_tree(lean_invocation)
                    if lean_invocation is not None
                    else None
                ),
            },
            "selections": {
                "k_audit": k_audit_selection,
                "klean_generation": generation_selection,
            },
            "stage4_preflight": preflight,
            "stage5_result": lean_result,
        }
        return _stage6_audit_input(resolved)
    except klean_export.KleanExportError as error:
        raise KleanAuditContractError(str(error)) from error
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error


def _execution_directories(executions: Path) -> list[Path]:
    try:
        executions = pipeline_contract.require_real_directory(
            executions, "Stage 6 executions"
        )
        children: list[Path] = []
        for entry in os.scandir(executions):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            if not stat.S_ISDIR(mode) or not re.fullmatch(
                r"[0-9]{3}", path.name
            ):
                raise KleanAuditContractError(
                    f"invalid Stage 6 execution entry: {path}"
                )
            children.append(path)
        return sorted(children)
    except OSError as error:
        raise KleanAuditContractError(
            f"cannot scan Stage 6 executions: {error}"
        ) from error
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error


def prepare_stage6_execution(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    expected_resolved_input_sha256: str,
    replace_selected: bool = False,
) -> Path:
    expected_digest = _validate_sha256(
        expected_resolved_input_sha256,
        "expected Stage 6 resolved-input digest",
    )
    try:
        resolution = resolve_stage6_audit(repo, run_id, problem)
    except KleanAuditContractError as error:
        raise KleanAuditContractError(
            "resolved inputs changed before Stage 6 allocation"
        ) from error
    if resolution["resolved_input_sha256"] != expected_digest:
        raise KleanAuditContractError(
            "resolved inputs changed before Stage 6 allocation"
        )
    try:
        task, _state, _run = pipeline_contract._resolve_task_state(
            repo, run_id, problem
        )
        stage = pipeline_contract.require_real_directory(
            task / "06-lean-audit", "Stage 6"
        )
        executions = pipeline_contract.require_real_directory(
            stage / "executions", "Stage 6 executions"
        )
        existing = _execution_directories(executions)
        selected_path = stage / "selected.json"
        if selected_path.exists() or selected_path.is_symlink():
            selected = pipeline_contract._read_regular_json(
                selected_path, "Stage 6 selection"
            )
            if (
                selected.get("status") != "AUDIT_ERROR"
                and not replace_selected
            ):
                raise KleanAuditContractError(
                    "Stage 6 has a terminal selected audit"
                )
        elif existing:
            raise KleanAuditContractError(
                "unselected Stage 6 execution exists; recover it before retry"
            )
        destination = executions / f"{len(existing) + 1:03d}"
        destination.mkdir()
        (destination / "evidence").mkdir()
        return destination.resolve(strict=True)
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error
    except OSError as error:
        raise KleanAuditContractError(
            "cannot allocate Stage 6 execution"
        ) from error


def _mechanical_binding_error(
    mechanical: dict[str, Any],
    audit_input: dict[str, Any],
) -> str | None:
    resolution, expected_digest = verify_stage6_audit_input(
        audit_input
    )
    expected_mode = resolution.get("mode")
    expected_hashes = resolution.get("hashes")
    if (
        not isinstance(expected_digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_digest) is None
        or expected_mode not in {
            "CLASSIFICATION_ONLY",
            "CLASSIFICATION_AND_PROOF",
        }
        or not isinstance(expected_hashes, dict)
    ):
        raise KleanAuditContractError(
            "Stage 6 audit input binding is malformed"
        )
    if mechanical.get("resolved_input_sha256") != expected_digest:
        return "mechanical resolved-input digest differs from audit input"
    if mechanical.get("mode") != expected_mode:
        return "mechanical audit mode differs from audit input"
    if mechanical.get("input_hashes") != expected_hashes:
        return "mechanical input hashes differ from audit input"
    return None


def reconcile_mechanical_verdict(
    verdict_path: Path,
    mechanical_path: Path,
    audit_input_path: Path,
) -> dict[str, Any]:
    verdict = _read_json(Path(verdict_path), "Stage 6 verdict")
    mechanical = _read_json(
        Path(mechanical_path), "Stage 6 mechanical check"
    )
    audit_input = _read_json(
        Path(audit_input_path), "Stage 6 audit input"
    )
    binding_error = _mechanical_binding_error(
        mechanical, audit_input
    )
    status = mechanical.get("status")
    if binding_error is not None:
        verdict = {
            "audit_status": "COMPLETE",
            "verdict": "FAIL",
            "legitimacy": "NOT_LEGIT",
            "error": binding_error,
            "mechanical_gate": "FAIL",
        }
    elif status == "FAIL":
        verdict = {
            "audit_status": "COMPLETE",
            "verdict": "FAIL",
            "legitimacy": "NOT_LEGIT",
            "error": None,
            "mechanical_gate": "FAIL",
        }
    elif status == "AUDIT_ERROR":
        verdict = {
            "audit_status": "AUDIT_ERROR",
            "verdict": None,
            "legitimacy": None,
            "error": "mechanical Lean audit infrastructure failed: "
            + str(mechanical.get("error", "unknown error")),
            "mechanical_gate": "AUDIT_ERROR",
        }
    elif status == "PASS":
        verdict["mechanical_gate"] = "PASS"
    else:
        raise KleanAuditContractError(
            "Stage 6 mechanical check status is invalid"
        )
    try:
        pipeline_contract.write_json_atomic(Path(verdict_path), verdict)
    except pipeline_contract.PipelineContractError as error:
        raise _translate(error) from error
    return verdict


def publish_stage6_execution(
    repo: Path,
    run_id: str,
    problem: str,
    candidate_name: str,
    *,
    expected_resolved_input_sha256: str,
    expected_candidate_sha256: str,
    replace_selected: bool = False,
) -> dict[str, Any]:
    expected_digest = _validate_sha256(
        expected_resolved_input_sha256,
        "expected Stage 6 resolved-input digest",
    )
    expected_candidate = _validate_sha256(
        expected_candidate_sha256,
        "expected Stage 6 candidate digest",
    )
    task, _state, _run = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    candidate_name = pipeline_contract.validate_safe_component(
        candidate_name, "Stage 6 execution name"
    )
    candidate = pipeline_contract._require_direct_directory(
        task / "06-lean-audit/executions",
        candidate_name,
        "finalized Stage 6 execution",
    )
    audit_input = _read_json(
        candidate / "audit-input.json", "Stage 6 audit input"
    )
    mechanical = _read_json(
        candidate / "mechanical-check.json",
        "Stage 6 mechanical check",
    )
    stored_resolution, stored_digest = verify_stage6_audit_input(
        audit_input
    )
    if stored_digest != expected_digest:
        raise KleanAuditContractError(
            "Stage 6 execution audit input digest changed before publication"
        )
    binding_error = _mechanical_binding_error(
        mechanical, audit_input
    )
    if binding_error is not None:
        raise KleanAuditContractError(binding_error)
    if pipeline_contract.sha256_tree(candidate) != expected_candidate:
        raise KleanAuditContractError(
            "Stage 6 candidate changed before publication"
        )
    try:
        fresh_audit_input = resolve_stage6_audit(
            repo, run_id, problem
        )
    except KleanAuditContractError as error:
        raise KleanAuditContractError(
            "resolved inputs changed before Stage 6 publication"
        ) from error
    fresh_resolution, fresh_digest = verify_stage6_audit_input(
        fresh_audit_input
    )
    if stored_resolution != fresh_resolution:
        raise KleanAuditContractError(
            "resolved inputs changed before Stage 6 publication: "
            "stored signed resolution differs from fresh resolution"
        )
    if fresh_digest != expected_digest:
        raise KleanAuditContractError(
            "resolved inputs changed before Stage 6 publication"
        )
    return pipeline_contract.select_stage_output(
        repo,
        run_id,
        problem,
        "06-lean-audit",
        candidate_name,
        expected_candidate_sha256=expected_candidate,
        replace_selected=replace_selected,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("resolve", "prepare"):
        command = subparsers.add_parser(name)
        command.add_argument("--repo", type=Path, default=REPO)
        command.add_argument("--run-id", required=True)
        command.add_argument("--problem", required=True)
        if name == "prepare":
            command.add_argument(
                "--expected-resolved-input-sha256",
                required=True,
            )
            command.add_argument(
                "--replace-selected", action="store_true"
            )
    reconcile = subparsers.add_parser("reconcile")
    reconcile.add_argument("--verdict", required=True, type=Path)
    reconcile.add_argument("--mechanical-check", required=True, type=Path)
    reconcile.add_argument("--audit-input", required=True, type=Path)
    publish = subparsers.add_parser("publish")
    publish.add_argument("--repo", type=Path, default=REPO)
    publish.add_argument("--run-id", required=True)
    publish.add_argument("--problem", required=True)
    publish.add_argument("--candidate", required=True)
    publish.add_argument(
        "--expected-resolved-input-sha256",
        required=True,
    )
    publish.add_argument(
        "--expected-candidate-sha256",
        required=True,
    )
    publish.add_argument("--replace-selected", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "reconcile":
            print(
                json.dumps(
                    reconcile_mechanical_verdict(
                        arguments.verdict,
                        arguments.mechanical_check,
                        arguments.audit_input,
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
        elif arguments.command == "resolve":
            print(
                json.dumps(
                    resolve_stage6_audit(
                        arguments.repo, arguments.run_id, arguments.problem
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
        elif arguments.command == "prepare":
            print(
                prepare_stage6_execution(
                    arguments.repo,
                    arguments.run_id,
                    arguments.problem,
                    expected_resolved_input_sha256=(
                        arguments.expected_resolved_input_sha256
                    ),
                    replace_selected=arguments.replace_selected,
                )
            )
        else:
            print(
                json.dumps(
                    publish_stage6_execution(
                        arguments.repo,
                        arguments.run_id,
                        arguments.problem,
                        arguments.candidate,
                        expected_resolved_input_sha256=(
                            arguments.expected_resolved_input_sha256
                        ),
                        expected_candidate_sha256=(
                            arguments.expected_candidate_sha256
                        ),
                        replace_selected=arguments.replace_selected,
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
    except (
        KleanAuditContractError,
        audit_contract.AuditContractError,
        pipeline_contract.PipelineContractError,
    ) as error:
        print(f"Stage 6 input error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
