#!/usr/bin/env python3
"""Launch deterministic Stage 4 Klean export from protected Stage 3 evidence."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import audit_contract, klean_export, pipeline_contract
from tools.stage3_runner import (
    Stage3RunnerError as LemmaDiscoveryRunnerError,
    _read_regular_nofollow,
)


IMAGE = "humaneval-klean-runner:locked"


class Stage4RunnerError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProtectedDiscovery:
    path: Path
    sha256: str
    identity: tuple[int, int]
    result_sha256: str


def _generation_directories(root: Path) -> list[Path]:
    root = pipeline_contract.require_real_directory(root, "generation root")
    result: list[Path] = []
    for entry in os.scandir(root):
        mode = entry.stat(follow_symlinks=False).st_mode
        path = Path(entry.path)
        if not entry.is_dir(follow_symlinks=False) or not re.fullmatch(
            r"[0-9]{3}", path.name
        ):
            raise Stage4RunnerError(f"invalid generation entry: {path}")
        result.append(path)
    return sorted(result)


def _stage1_workspace(task: Path) -> tuple[Path, str]:
    workspace = pipeline_contract.require_real_directory(
        task / "01-k-proof/workspace", "finalized Stage 1 workspace"
    )
    result = pipeline_contract._read_regular_json(
        task / "01-k-proof/result.json", "Stage 1 result"
    )
    outputs = result.get("outputs")
    expected = (
        outputs.get("workspace_sha256")
        if isinstance(outputs, dict)
        else None
    )
    current = pipeline_contract.sha256_tree(workspace)
    # User-authorized endgame provision (2026-08-01): the honest-PARTIAL
    # 129 artifact (stage-2 CONDITIONAL CONCERNS under the registered
    # provision) is admitted when explicitly enabled; the workspace
    # integrity hash requirement is unchanged.
    status_ok = result.get("status") == "SUCCEEDED" or (
        result.get("status") == "FAILED"
        and os.environ.get("HE_AUDIT_ACCEPT_PARTIAL")
    )
    if not status_ok or expected != current:
        raise Stage4RunnerError(
            "finalized Stage 1 workspace does not match its successful result"
        )
    return workspace, current


def _protected_stage3_discovery(task: Path) -> ProtectedDiscovery:
    stage = pipeline_contract.require_real_directory(
        task / "03-lemma-discovery", "Stage 3 lemma discovery"
    )
    result_path = pipeline_contract.require_regular_file(
        stage / "result.json", "Stage 3 result"
    )
    result = pipeline_contract._read_regular_json(
        result_path, "Stage 3 result"
    )
    invocation = result.get("invocation")
    artifact = result.get("trust_boundary_artifact")
    digest = result.get("trust_boundary_sha256")
    expected_artifact = (
        f"invocations/{invocation}/validated-trust-boundary.json"
        if isinstance(invocation, str)
        and re.fullmatch(
            r"[0-9]{3}-(?:initial|timeout-resume|infrastructure-retry)",
            invocation,
        )
        else None
    )
    outputs = result.get("outputs")
    evidence = outputs.get("evidence") if isinstance(outputs, dict) else None
    if (
        result.get("status") != "SUCCEEDED"
        or expected_artifact is None
        or artifact != expected_artifact
        or not isinstance(digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        or not isinstance(evidence, dict)
        or evidence.get("validated-trust-boundary.json") != digest
    ):
        raise Stage4RunnerError(
            "Stage 3 has no protected validated trust-boundary evidence"
        )
    invocation_path = pipeline_contract._require_direct_directory(
        stage / "invocations", invocation, "Stage 3 invocation"
    )
    invocation_manifest = pipeline_contract._read_regular_json(
        invocation_path / "invocation.json", "Stage 3 invocation manifest"
    )
    invocation_outputs = invocation_manifest.get("outputs")
    invocation_evidence = (
        invocation_outputs.get("evidence")
        if isinstance(invocation_outputs, dict)
        else None
    )
    if (
        invocation_manifest.get("status") != "SUCCEEDED"
        or invocation_manifest.get("kind")
        not in {"stage-resume", "timeout-resume", "infrastructure-retry"}
        or invocation_manifest.get("trust_boundary_artifact") != artifact
        or invocation_manifest.get("trust_boundary_sha256") != digest
        or not isinstance(invocation_evidence, dict)
        or invocation_evidence.get("validated-trust-boundary.json")
        != digest
    ):
        raise Stage4RunnerError(
            "protected Stage 3 provenance differs across terminal records"
        )
    path = invocation_path / "validated-trust-boundary.json"
    try:
        data, identity = _read_regular_nofollow(
            path, "protected Stage 3 trust-boundary evidence"
        )
    except LemmaDiscoveryRunnerError as error:
        raise Stage4RunnerError(str(error)) from error
    if hashlib.sha256(data).hexdigest() != digest:
        raise Stage4RunnerError(
            "protected Stage 3 trust-boundary evidence changed"
        )
    return ProtectedDiscovery(
        path=path,
        sha256=digest,
        identity=identity,
        result_sha256=pipeline_contract.sha256_file(result_path),
    )


def inspect_stage4(repo: Path, run_id: str, problem: str) -> dict[str, Any]:
    repo = pipeline_contract.require_real_directory(Path(repo), "repository")
    task, _state, _run = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    pipeline_contract.require_task_unblocked(task, "Stage 4")
    eligibility = audit_contract.stage2_eligibility(repo, run_id, problem)
    frozen, frozen_hash = _stage1_workspace(task)
    discovery = _protected_stage3_discovery(task)
    root = task / "04-klean-generation/generations"
    existing = _generation_directories(root)
    return {
        "run_id": run_id,
        "problem": problem,
        "eligible": eligibility["eligible"],
        "stage2_verdict": eligibility["verdict"],
        "frozen_input": str(frozen),
        "frozen_input_sha256": frozen_hash,
        "discovery_manifest": str(discovery.path),
        "discovery_manifest_sha256": discovery.sha256,
        "output_root": str(root),
        "next_generation": f"{len(existing) + 1:03d}",
        "image": IMAGE,
    }


def _next_generation(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    replace_selected: bool = False,
) -> tuple[Path, str]:
    task, _state, _run = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    pipeline_contract.require_task_unblocked(task, "Stage 4")
    try:
        eligibility = audit_contract.stage2_eligibility(
            repo, run_id, problem
        )
    except audit_contract.AuditContractError as error:
        raise Stage4RunnerError(str(error)) from error
    if not eligibility["eligible"]:
        raise Stage4RunnerError(
            "Stage 2 is NOT_LEGIT; Klean generation is forbidden"
        )
    _stage1_workspace(task)
    _protected_stage3_discovery(task)
    stage = task / "04-klean-generation"
    root = stage / "generations"
    existing = _generation_directories(root)
    selected = stage / "selected.json"
    if selected.exists() or selected.is_symlink():
        document = pipeline_contract._read_regular_json(
            selected, "Stage 4 selection"
        )
        if (
            document.get("status") != "KLEAN_PREFLIGHT_ERROR"
            and not replace_selected
        ):
            raise Stage4RunnerError(
                "Stage 4 already has a terminal passing generation"
            )
    elif existing:
        raise Stage4RunnerError(
            "unselected generation exists; inspect it before allocating another"
        )
    return root, f"{len(existing) + 1:03d}"


def _validate_terminal_preflight(
    generation: Path,
    preflight: dict[str, Any],
    returncode: int,
    *,
    stage1_workspace_sha256: str,
    stage3_discovery_manifest_sha256: str,
) -> None:
    if preflight.get("schema_version") != 3:
        raise Stage4RunnerError(
            "Stage 4 Klean preflight schema version is not 3"
        )
    status = preflight.get("status")
    successful = {"PASS", "KLEAN_NO_OBLIGATIONS"}
    terminal = successful | {"KLEAN_PREFLIGHT_ERROR"}
    if status not in terminal:
        raise Stage4RunnerError(
            "Stage 4 Klean preflight status is not terminal"
        )
    if (
        preflight.get("stage1_workspace_sha256")
        != stage1_workspace_sha256
    ):
        raise Stage4RunnerError(
            "Stage 4 preflight does not match the protected Stage 1 input"
        )
    if (
        preflight.get("stage3_discovery_manifest_sha256")
        != stage3_discovery_manifest_sha256
    ):
        raise Stage4RunnerError(
            "Stage 4 preflight does not match the protected Stage 3 evidence"
        )
    if returncode == 0 and status not in successful:
        raise Stage4RunnerError(
            "container succeeded without a passing preflight"
        )
    if returncode != 0 and status in successful:
        raise Stage4RunnerError(
            "container failed after recording a passing preflight"
        )
    if status in successful:
        try:
            generated_sha256 = klean_export.tree_digest(
                generation / "generated"
            )
        except (OSError, klean_export.KleanExportError) as error:
            raise Stage4RunnerError(
                "passing preflight has no safe generated project"
            ) from error
        if preflight.get("generated_tree_sha256") != generated_sha256:
            raise Stage4RunnerError(
                "passing preflight generated project hash is invalid"
            )


def _candidate_json(
    generation: Path,
    name: str,
) -> tuple[dict[str, Any], bytes]:
    try:
        data, _identity = _read_regular_nofollow(
            generation / name, f"Stage 4 candidate sidecar {name}"
        )
    except LemmaDiscoveryRunnerError as error:
        raise Stage4RunnerError(str(error)) from error
    try:
        document = json.loads(data)
    except (TypeError, ValueError) as error:
        raise Stage4RunnerError(
            f"Stage 4 candidate sidecar is malformed: {name}"
        ) from error
    if not isinstance(document, dict):
        raise Stage4RunnerError(
            f"Stage 4 candidate sidecar must be a JSON object: {name}"
        )
    return document, data


def _validated_candidate_sha256(
    generation: Path,
    returncode: int,
    *,
    expected_candidate_sha256: str,
    problem: str,
    stage1_workspace_sha256: str,
    stage3_discovery_manifest_sha256: str,
) -> str:
    before_sha256 = pipeline_contract.sha256_tree(generation)
    if before_sha256 != expected_candidate_sha256:
        raise Stage4RunnerError(
            "Stage 4 candidate changed during final protected-input checks"
        )
    preflight, _preflight_bytes = _candidate_json(
        generation, "preflight.json"
    )
    _validate_terminal_preflight(
        generation,
        preflight,
        returncode,
        stage1_workspace_sha256=stage1_workspace_sha256,
        stage3_discovery_manifest_sha256=(
            stage3_discovery_manifest_sha256
        ),
    )
    if preflight["status"] in {"PASS", "KLEAN_NO_OBLIGATIONS"}:
        input_manifest, _input_bytes = _candidate_json(
            generation, "input-manifest.json"
        )
        generator_manifest, _generator_bytes = _candidate_json(
            generation, "generator-manifest.json"
        )
        _trust_inventory, trust_inventory_bytes = _candidate_json(
            generation, "trust-inventory.json"
        )
        export_result, _export_bytes = _candidate_json(
            generation, "export-result.json"
        )
        generated_sha256 = preflight["generated_tree_sha256"]
        common_documents = (
            ("input manifest", input_manifest),
            ("generator manifest", generator_manifest),
            ("export result", export_result),
        )
        for label, document in common_documents:
            if document.get("schema_version") != 3:
                raise Stage4RunnerError(
                    f"Stage 4 candidate {label} schema version is not 3"
                )
        if (
            input_manifest.get("problem") != problem
            or input_manifest.get("frozen_input_sha256")
            != stage1_workspace_sha256
            or input_manifest.get("stage1_workspace_sha256")
            != stage1_workspace_sha256
            or input_manifest.get("stage3_discovery_manifest_sha256")
            != stage3_discovery_manifest_sha256
        ):
            raise Stage4RunnerError(
                "Stage 4 candidate input sidecar provenance is invalid"
            )
        provenance = generator_manifest.get("provenance")
        if (
            generator_manifest.get("generated_tree_sha256")
            != generated_sha256
            or not isinstance(provenance, dict)
            or provenance.get("stage1_workspace_sha256")
            != stage1_workspace_sha256
            or provenance.get("stage3_discovery_manifest_sha256")
            != stage3_discovery_manifest_sha256
        ):
            raise Stage4RunnerError(
                "Stage 4 candidate generator sidecar provenance is invalid"
            )
        expected_export_status = (
            "OK"
            if preflight["status"] == "PASS"
            else "KLEAN_NO_OBLIGATIONS"
        )
        if (
            export_result.get("problem") != problem
            or export_result.get("status") != expected_export_status
            or export_result.get("frozen_input_sha256")
            != stage1_workspace_sha256
            or export_result.get("stage3_discovery_manifest_sha256")
            != stage3_discovery_manifest_sha256
            or export_result.get("generated_tree_sha256")
            != generated_sha256
            or export_result.get("trust_inventory_sha256")
            != hashlib.sha256(trust_inventory_bytes).hexdigest()
        ):
            raise Stage4RunnerError(
                "Stage 4 candidate export sidecar provenance is invalid"
            )
        obligation_count = preflight.get("obligation_count")
        if (
            not isinstance(obligation_count, int)
            or isinstance(obligation_count, bool)
            or obligation_count < 0
            or generator_manifest.get("obligation_count")
            != obligation_count
            or export_result.get("obligation_count")
            != obligation_count
        ):
            raise Stage4RunnerError(
                "Stage 4 candidate sidecar obligation counts are invalid"
            )
    after_sha256 = pipeline_contract.sha256_tree(generation)
    if (
        after_sha256 != before_sha256
        or after_sha256 != expected_candidate_sha256
    ):
        raise Stage4RunnerError(
            "Stage 4 candidate changed during final validation"
        )
    return after_sha256


def run_stage4(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    docker: str = "docker",
    replace_selected: bool = False,
) -> dict[str, Any]:
    repo = pipeline_contract.require_real_directory(Path(repo), "repository")
    root, generation_id = _next_generation(
        repo,
        run_id,
        problem,
        replace_selected=replace_selected,
    )
    task, _state, _run = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    eligibility = audit_contract.stage2_eligibility(repo, run_id, problem)
    frozen, frozen_hash = _stage1_workspace(task)
    stage1_workspace_sha256 = klean_export.tree_digest(frozen)
    discovery = _protected_stage3_discovery(task)
    image = subprocess.run(
        [docker, "image", "inspect", IMAGE, "--format", "{{.Id}}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    image_id = image.stdout.strip()
    if image.returncode != 0 or not image_id:
        raise Stage4RunnerError(
            f"cannot resolve pinned generator image ID: {image.stderr[-300:]}"
        )

    staging = Path(tempfile.mkdtemp(prefix=f"stage4-{generation_id}-"))
    output = staging / "output"
    output.mkdir()
    generation = root / generation_id
    publication: Path | None = None
    try:
        command = [
            docker,
            "run",
            "--rm",
            "--network",
            "none",
            "--pull",
            "never",
            "--mount",
            f"type=bind,source={frozen},target=/frozen-k,readonly",
            "--mount",
            (
                f"type=bind,source={discovery.path},"
                "target=/discovery-manifest.json,readonly"
            ),
            "--mount",
            f"type=bind,source={output},target=/output",
            "--env",
            f"PROBLEM_ID={problem}",
            "--env",
            f"GENERATOR_IMAGE_ID={image_id}",
            IMAGE,
        ]
        result = subprocess.run(command)
        after = audit_contract.stage2_eligibility(repo, run_id, problem)
        if after != eligibility:
            raise Stage4RunnerError(
                "Stage 2 selected audit changed during Klean generation"
            )
        if pipeline_contract.sha256_tree(frozen) != frozen_hash:
            raise Stage4RunnerError(
                "finalized Stage 1 workspace changed during Klean generation"
            )
        after_discovery = _protected_stage3_discovery(task)
        if after_discovery != discovery:
            raise Stage4RunnerError(
                "protected Stage 3 evidence changed during Klean generation"
            )
        produced = output / "generation"
        if not produced.is_dir() or produced.is_symlink():
            raise Stage4RunnerError(
                "Klean container did not preserve a generation result"
            )
        if generation.exists() or generation.is_symlink():
            raise Stage4RunnerError(
                "Klean generation destination appeared during execution"
            )
        produced_hash = pipeline_contract.sha256_tree(produced)
        publication = Path(
            tempfile.mkdtemp(prefix=f".{generation_id}-", dir=root)
        )
        publication.rmdir()
        shutil.copytree(produced, publication)
        if pipeline_contract.sha256_tree(publication) != produced_hash:
            raise Stage4RunnerError(
                "Klean generation changed while copying for publication"
            )
        publication.rename(generation)
        publication = None
    finally:
        if publication is not None and publication.exists():
            shutil.rmtree(publication)
        if staging.exists():
            shutil.rmtree(staging)

    if not generation.is_dir() or generation.is_symlink():
        raise Stage4RunnerError(
            "Klean container did not preserve a generation result"
        )
    preflight = pipeline_contract._read_regular_json(
        generation / "preflight.json", "Stage 4 Klean preflight"
    )
    _validate_terminal_preflight(
        generation,
        preflight,
        result.returncode,
        stage1_workspace_sha256=stage1_workspace_sha256,
        stage3_discovery_manifest_sha256=discovery.sha256,
    )
    candidate_sha256 = pipeline_contract.sha256_tree(generation)
    if audit_contract.stage2_eligibility(
        repo, run_id, problem
    ) != eligibility:
        raise Stage4RunnerError(
            "Stage 2 selected audit changed before Stage 4 selection"
        )
    if pipeline_contract.sha256_tree(frozen) != frozen_hash or (
        klean_export.tree_digest(frozen) != stage1_workspace_sha256
    ):
        raise Stage4RunnerError(
            "finalized Stage 1 workspace changed before Stage 4 selection"
        )
    if _protected_stage3_discovery(task) != discovery:
        raise Stage4RunnerError(
            "protected Stage 3 evidence changed before Stage 4 selection"
        )
    candidate_sha256 = _validated_candidate_sha256(
        generation,
        result.returncode,
        expected_candidate_sha256=candidate_sha256,
        problem=problem,
        stage1_workspace_sha256=stage1_workspace_sha256,
        stage3_discovery_manifest_sha256=discovery.sha256,
    )
    return pipeline_contract.select_stage_output(
        repo,
        run_id,
        problem,
        "04-klean-generation",
        generation_id,
        expected_candidate_sha256=candidate_sha256,
        replace_selected=replace_selected,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--print-config", action="store_true")
    parser.add_argument("--replace-selected", action="store_true")
    parser.add_argument("run_id")
    parser.add_argument("problem")
    arguments = parser.parse_args(argv)
    try:
        if arguments.print_config:
            print(json.dumps(inspect_stage4(
                arguments.repo, arguments.run_id, arguments.problem
            ), indent=2, sort_keys=True))
            return 0
        selected = run_stage4(
            arguments.repo,
            arguments.run_id,
            arguments.problem,
            replace_selected=arguments.replace_selected,
        )
    except (
        audit_contract.AuditContractError,
        pipeline_contract.PipelineContractError,
        Stage4RunnerError,
    ) as error:
        print(f"Stage 4 failed: {error}", file=sys.stderr)
        return 2
    return (
        0
        if selected["status"] in {"PASS", "KLEAN_NO_OBLIGATIONS"}
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
