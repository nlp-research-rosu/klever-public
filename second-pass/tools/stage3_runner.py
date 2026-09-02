#!/usr/bin/env python3
"""Resume the Stage 1 Codex session for isolated lemma discovery."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import (
    audit_contract,
    k_rule_inventory,
    lemma_discovery_contract,
    pipeline_contract,
)
from tools.stage1_runner import (
    Stage1RunnerError,
    _container_name,
    _inspect_container,
    _read_entry_metrics,
)


class Stage3RunnerError(RuntimeError):
    pass


STAGE = "03-lemma-discovery"
RESULT_PATTERN = re.compile(
    r"RESULT: LEMMA_DISCOVERY_COMPLETE — (\S(?:.*\S)?)"
)


@dataclass(frozen=True)
class InvocationOutcome:
    exit_code: int
    duration_s: int
    timeout_marker: bool
    oom_killed: bool
    image_id: str


@dataclass(frozen=True)
class ProtectedManifest:
    path: Path
    data: bytes
    sha256: str
    live_path: Path
    live_identity: tuple[int, int]
    protected_identity: tuple[int, int]


def parse_stage3_result(path: Path) -> str:
    path = pipeline_contract.require_regular_file(
        Path(path), "Stage 3 final message"
    )
    try:
        lines = path.read_text().splitlines()
    except OSError as error:
        raise Stage3RunnerError(
            f"cannot read Stage 3 final message: {path}"
        ) from error
    result_lines = [line for line in lines if line.startswith("RESULT:")]
    if len(result_lines) != 1:
        raise Stage3RunnerError(
            "Stage 3 final message must contain exactly one RESULT marker"
        )
    match = RESULT_PATTERN.fullmatch(result_lines[0])
    if match is None:
        raise Stage3RunnerError("Stage 3 RESULT marker is malformed")
    return match.group(1)


def _selected_legit_stage2(
    repo: Path, run_id: str, problem: str
) -> dict[str, object]:
    try:
        eligibility = audit_contract.stage2_eligibility(
            repo, run_id, problem
        )
    except audit_contract.AuditContractError as error:
        raise Stage3RunnerError(
            "Stage 3 requires a selected LEGIT Stage 2 PASS or CONCERNS"
        ) from error
    if (
        eligibility.get("eligible") is not True
        or eligibility.get("legitimacy") != "LEGIT"
        or eligibility.get("verdict") not in {"PASS", "CONCERNS"}
    ):
        raise Stage3RunnerError(
            "Stage 3 requires a selected LEGIT Stage 2 PASS or CONCERNS"
        )
    return eligibility


def _stage1_workspace_hash(task: Path) -> tuple[Path, str]:
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
        raise Stage3RunnerError(
            "finalized Stage 1 workspace does not match its successful result"
        )
    return workspace, current


def _inventory_path(task: Path) -> Path:
    return task / STAGE / "rule-inventory.json"


def _prepare_rule_inventory(task: Path, workspace: Path) -> tuple[Path, str]:
    try:
        inventory = k_rule_inventory.inventory_verification(workspace)
    except k_rule_inventory.KRuleInventoryError as error:
        raise Stage3RunnerError(str(error)) from error
    path = _inventory_path(task)
    if path.exists() or path.is_symlink():
        existing = pipeline_contract._read_regular_json(
            path, "Stage 3 canonical rule inventory"
        )
        if existing != inventory:
            raise Stage3RunnerError(
                "Stage 3 canonical rule inventory changed after publication"
            )
    else:
        pipeline_contract.write_json_atomic(path, inventory)
        path.chmod(0o444)
    path = pipeline_contract.require_regular_file(
        path, "Stage 3 canonical rule inventory"
    )
    return path, pipeline_contract.sha256_file(path)


def _prepare_auth_infrastructure_retry(
    repo: Path, run_id: str, problem: str
) -> pipeline_contract.Invocation:
    task, state, run_manifest = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    stage_root = pipeline_contract.require_real_directory(
        task / STAGE, "Stage 3 root"
    )
    invocations = pipeline_contract.require_real_directory(
        stage_root / "invocations", "Stage 3 invocations"
    )
    existing = pipeline_contract._invocation_directories(invocations)
    if [path.name for path in existing] != ["001-initial"]:
        raise Stage3RunnerError(
            "Stage 3 auth infrastructure retry requires exactly one initial invocation"
        )
    previous = existing[0]
    document = pipeline_contract._read_regular_json(
        previous / "invocation.json", "failed Stage 3 invocation"
    )
    session_id = pipeline_contract._read_session_state(state)["session_id"]
    if (
        document.get("stage") != STAGE
        or document.get("kind") != "stage-resume"
        or document.get("status") != "FAILED"
        or document.get("exit_code") != 70
        or document.get("session_id") != session_id
    ):
        raise Stage3RunnerError(
            "Stage 3 auth infrastructure retry requires a finalized pre-model failure"
        )
    output_log = pipeline_contract.require_regular_file(
        previous / "codex-output.log", "failed Stage 3 Codex output"
    )
    output_hash = pipeline_contract.sha256_file(output_log)
    outputs = document.get("outputs")
    evidence = outputs.get("evidence") if isinstance(outputs, dict) else None
    if (
        not isinstance(evidence, dict)
        or evidence.get("codex-output.log") != output_hash
    ):
        raise Stage3RunnerError(
            "Stage 3 auth failure evidence changed after finalization"
        )
    try:
        output = output_log.read_bytes()
    except OSError as error:
        raise Stage3RunnerError(
            "cannot read failed Stage 3 Codex output"
        ) from error
    if not (
        b"token_invalidated" in output
        and b"refresh_token_invalidated" in output
    ):
        raise Stage3RunnerError(
            "Stage 3 infrastructure retry requires token invalidation evidence"
        )
    workspace_hash = pipeline_contract.sha256_tree(stage_root / "workspace")
    inputs = document.get("inputs")
    if (
        not isinstance(inputs, dict)
        or inputs.get("workspace_sha256") != workspace_hash
        or not isinstance(outputs, dict)
        or outputs.get("workspace_sha256") != workspace_hash
    ):
        raise Stage3RunnerError(
            "Stage 3 auth retry requires an unchanged discovery workspace"
        )
    allocation_s = document.get("allocation_s")
    if not isinstance(allocation_s, int) or allocation_s <= 0:
        raise Stage3RunnerError("failed Stage 3 allocation is malformed")
    destination = invocations / "002-infrastructure-retry"
    try:
        destination.mkdir()
    except FileExistsError as error:
        raise Stage3RunnerError(
            "Stage 3 auth infrastructure retry already exists"
        ) from error
    retry_document = {
        "schema_version": pipeline_contract.SCHEMA_VERSION,
        "stage": STAGE,
        "name": destination.name,
        "kind": "infrastructure-retry",
        "status": "PREPARED",
        "allocation_s": allocation_s,
        "session_id": session_id,
        "retry_of": previous.name,
        "infrastructure_error": {
            "kind": "codex-auth-token-invalidated",
            "evidence": "001-initial/codex-output.log",
            "evidence_sha256": output_hash,
        },
        "prompt_sha256": None,
        "inputs": {"workspace_sha256": workspace_hash},
        "outputs": None,
    }
    try:
        pipeline_contract.write_json_atomic(
            destination / "invocation.json", retry_document
        )
        pipeline_contract._append_ledger(
            state,
            {
                "event": "invocation_prepared",
                "stage": STAGE,
                "invocation": destination.name,
                "kind": "infrastructure-retry",
                "allocation_s": allocation_s,
                "retry_of": previous.name,
                "infrastructure_error": "codex-auth-token-invalidated",
            },
        )
    except BaseException:
        destination.rmdir()
        raise
    return pipeline_contract.Invocation(
        stage=STAGE,
        name=destination.name,
        kind="infrastructure-retry",
        path=destination.resolve(strict=True),
        allocation_s=allocation_s,
        session_id=session_id,
    )


def inspect_stage3(
    repo: Path, run_id: str, problem: str
) -> dict[str, Any]:
    repo = pipeline_contract.require_real_directory(Path(repo), "repository")
    task, state, run_manifest = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    pipeline_contract.require_task_unblocked(task, "Stage 3")
    eligibility = _selected_legit_stage2(repo, run_id, problem)
    workspace, _workspace_hash = _stage1_workspace_hash(task)
    session = pipeline_contract._read_session_state(state)
    try:
        timeout_s = int(run_manifest["timeouts"]["lemma_initial_s"])
    except (KeyError, TypeError, ValueError) as error:
        raise Stage3RunnerError("Stage 3 timeout policy is malformed") from error
    if timeout_s <= 0:
        raise Stage3RunnerError("Stage 3 timeout policy is malformed")
    return {
        "run_id": run_id,
        "problem": problem,
        "eligible": True,
        "stage2_verdict": eligibility["verdict"],
        "session_id": session["session_id"],
        "timeout_s": timeout_s,
        "k_reference": str(workspace),
        "rule_inventory": str(_inventory_path(task)),
        "workspace": str(task / f"{STAGE}/workspace"),
        "prompt": "lemma-discovery.md",
    }


def _read_regular_nofollow(
    path: Path, label: str
) -> tuple[bytes, tuple[int, int]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Stage3RunnerError(
            f"{label} must be a real regular file: {path}"
        ) from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise Stage3RunnerError(
                f"{label} must be a real regular file: {path}"
            )
        try:
            path_before = path.lstat()
        except OSError as error:
            raise Stage3RunnerError(
                f"cannot inspect {label}: {path}"
            ) from error
        identity = (before.st_dev, before.st_ino)
        if (
            not stat.S_ISREG(path_before.st_mode)
            or (path_before.st_dev, path_before.st_ino) != identity
        ):
            raise Stage3RunnerError(
                f"{label} changed while it was opened: {path}"
            )
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        stable_fields = (
            "st_dev",
            "st_ino",
            "st_mode",
            "st_size",
            "st_mtime_ns",
            "st_ctime_ns",
        )
        if any(
            getattr(before, field) != getattr(after, field)
            for field in stable_fields
        ):
            raise Stage3RunnerError(
                f"{label} changed while it was read: {path}"
            )
        data = b"".join(chunks)
        if len(data) != after.st_size:
            raise Stage3RunnerError(
                f"{label} size changed while it was read: {path}"
            )
        try:
            path_after = path.lstat()
        except OSError as error:
            raise Stage3RunnerError(
                f"cannot re-inspect {label}: {path}"
            ) from error
        if (
            not stat.S_ISREG(path_after.st_mode)
            or (path_after.st_dev, path_after.st_ino) != identity
        ):
            raise Stage3RunnerError(
                f"{label} changed while it was read: {path}"
            )
        return data, identity
    finally:
        os.close(descriptor)


def _publish_protected_manifest(
    live_manifest: Path, invocation: Path
) -> ProtectedManifest:
    data, live_identity = _read_regular_nofollow(
        live_manifest, "Stage 3 trust-boundary manifest"
    )
    destination = invocation / "validated-trust-boundary.json"
    if destination.exists() or destination.is_symlink():
        raise Stage3RunnerError(
            "protected Stage 3 trust-boundary evidence already exists"
        )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".validated-trust-boundary.",
        dir=invocation,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(0o444)
        try:
            os.link(temporary, destination)
        except FileExistsError as error:
            raise Stage3RunnerError(
                "protected Stage 3 trust-boundary evidence appeared "
                "during publication"
            ) from error
    except OSError as error:
        raise Stage3RunnerError(
            "cannot publish protected Stage 3 trust-boundary evidence"
        ) from error
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    protected_path = pipeline_contract.require_regular_file(
        destination, "protected Stage 3 trust-boundary evidence"
    )
    protected_data, protected_identity = _read_regular_nofollow(
        protected_path, "protected Stage 3 trust-boundary evidence"
    )
    if protected_data != data:
        raise Stage3RunnerError(
            "protected Stage 3 trust-boundary evidence changed "
            "during publication"
        )
    return ProtectedManifest(
        path=protected_path,
        data=data,
        sha256=hashlib.sha256(data).hexdigest(),
        live_path=live_manifest,
        live_identity=live_identity,
        protected_identity=protected_identity,
    )


def _validate_discovery(
    workspace: Path, k_reference: Path, invocation: Path
) -> ProtectedManifest:
    parse_stage3_result(invocation / "codex-last.txt")
    discovery = pipeline_contract.require_regular_file(
        workspace / "DISCOVERY.md", "Stage 3 discovery report"
    )
    try:
        if not discovery.read_text().strip():
            raise Stage3RunnerError("Stage 3 discovery report is empty")
    except OSError as error:
        raise Stage3RunnerError(
            f"cannot read Stage 3 discovery report: {discovery}"
        ) from error
    live_manifest = workspace / "trust-boundary.json"
    protected = _publish_protected_manifest(live_manifest, invocation)
    try:
        lemma_discovery_contract.validate_trust_boundary(
            k_reference, protected.path
        )
    except lemma_discovery_contract.LemmaDiscoveryContractError as error:
        raise Stage3RunnerError(str(error)) from error
    live_data, live_identity = _read_regular_nofollow(
        live_manifest, "Stage 3 trust-boundary manifest"
    )
    if (
        live_identity != protected.live_identity
        or hashlib.sha256(live_data).hexdigest() != protected.sha256
    ):
        raise Stage3RunnerError(
            "Stage 3 trust-boundary manifest changed after snapshot"
        )
    return protected


def _verify_post_model_integrity(
    repo: Path,
    run_id: str,
    problem: str,
    state: Path,
    invocation: pipeline_contract.Invocation,
    k_reference: Path,
    expected_k_hash: str,
    inventory_path: Path,
    expected_inventory_hash: str,
    eligibility: dict[str, object],
    *,
    require_trace: bool,
    protected: ProtectedManifest | None,
) -> None:
    if pipeline_contract.sha256_tree(k_reference) != expected_k_hash:
        raise Stage3RunnerError(
            "finalized Stage 1 workspace changed during Stage 3"
        )
    if (
        pipeline_contract.sha256_file(inventory_path)
        != expected_inventory_hash
    ):
        raise Stage3RunnerError(
            "canonical rule inventory changed during Stage 3"
        )
    if _selected_legit_stage2(repo, run_id, problem) != eligibility:
        raise Stage3RunnerError(
            "selected Stage 2 audit changed during Stage 3"
        )
    persisted_session = pipeline_contract._read_session_state(state)[
        "session_id"
    ]
    if (
        invocation.session_id != persisted_session
        or invocation.kind
        not in {"stage-resume", "timeout-resume", "infrastructure-retry"}
    ):
        raise Stage3RunnerError(
            "Stage 3 invocation does not resume the persisted session"
        )
    trace = invocation.path / "codex-trace"
    if trace.exists() or trace.is_symlink():
        if pipeline_contract.extract_session_uuid(trace) != persisted_session:
            raise Stage3RunnerError(
                "Stage 3 trace session does not match persisted session"
            )
    elif require_trace:
        raise Stage3RunnerError(
            "successful Stage 3 invocation has no session trace"
        )
    if protected is not None:
        live_data, live_identity = _read_regular_nofollow(
            protected.live_path,
            "Stage 3 trust-boundary manifest",
        )
        if (
            live_identity != protected.live_identity
            or live_data != protected.data
        ):
            raise Stage3RunnerError(
                "Stage 3 trust-boundary manifest changed after validation"
            )
        protected_data, protected_identity = _read_regular_nofollow(
            protected.path,
            "protected Stage 3 trust-boundary evidence",
        )
        if (
            protected_identity != protected.protected_identity
            or protected_data != protected.data
        ):
            raise Stage3RunnerError(
                "protected Stage 3 trust-boundary evidence changed"
            )


def _run_one(
    repo: Path,
    run_id: str,
    problem: str,
    invocation: pipeline_contract.Invocation,
    run_manifest: dict[str, Any],
    state: Path,
    k_reference: Path,
    inventory_path: Path,
    *,
    docker: str,
    kit_skills: Path | None = None,
) -> InvocationOutcome:
    prompt = repo / "prompts/lemma-discovery.md"
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
            str(
                repo
                / "docker/codex/docker-compose.lemma-discovery.yml"
            ),
        ]
    )
    container_name = _container_name(
        run_id, problem, f"lemma-{invocation.name}"
    )
    command.extend(["run", "--name", container_name, "-T", "runner"])
    environment = os.environ.copy()
    environment.update(
        {
            "WORKSPACE_DIR": str(workspace),
            "INVOCATION_DIR": str(invocation.path),
            "CODEX_HOME_DIR": str(state / "codex-home"),
            "PROMPT_PATH": str(prompt),
            "K_REFERENCE_DIR": str(k_reference),
            "RULE_INVENTORY_PATH": str(inventory_path),
            "INVOCATION_KIND": invocation.kind,
            "SESSION_ID": invocation.session_id or "",
            "MODEL": str(run_manifest["model"]),
            "EFFORT": str(run_manifest["effort"]),
            "TIMEOUT_S": str(invocation.allocation_s),
            "KIT": "1" if kit else "0",
        }
    )
    if kit and kit_skills is not None:
        environment["KIT_SKILLS_PATH"] = str(kit_skills)
    run_result = subprocess.run(command, env=environment)
    try:
        try:
            inspection = _inspect_container(docker, container_name)
        except Stage1RunnerError:
            return InvocationOutcome(
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
        return InvocationOutcome(
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
    timeout_marker = metrics["timeout_marker"] if consistent else False
    oom_killed = inspection["oom_killed"] or metrics["oom_killed"]
    return InvocationOutcome(
        exit_code=exit_code,
        duration_s=metrics["duration_s"],
        timeout_marker=timeout_marker,
        oom_killed=oom_killed,
        image_id=inspection["image_id"],
    )


def run_stage3(
    repo: Path,
    run_id: str,
    problem: str,
    *,
    docker: str = "docker",
    retry_auth_infrastructure: bool = False,
) -> dict[str, Any]:
    repo = pipeline_contract.require_real_directory(Path(repo), "repository")
    task, state, run_manifest = pipeline_contract._resolve_task_state(
        repo, run_id, problem
    )
    pipeline_contract.require_task_unblocked(task, "Stage 3")
    kit_skills = (
        pipeline_contract.resolve_stage_kit_skills(repo, run_id, problem)
        if bool(run_manifest["condition"]["kit"])
        else None
    )
    eligibility = _selected_legit_stage2(repo, run_id, problem)
    k_reference, expected_k_hash = _stage1_workspace_hash(task)
    inventory_path, expected_inventory_hash = _prepare_rule_inventory(
        task, k_reference
    )
    try:
        lemma_total_s = int(run_manifest["timeouts"]["lemma_total_s"])
    except (KeyError, TypeError, ValueError) as error:
        raise Stage3RunnerError("Stage 3 timeout policy is malformed") from error
    first_iteration = True
    while True:
        if retry_auth_infrastructure and first_iteration:
            invocation = _prepare_auth_infrastructure_retry(
                repo, run_id, problem
            )
        else:
            invocation = pipeline_contract.prepare_invocation(
                repo, run_id, problem, STAGE
            )
        first_iteration = False
        outcome = _run_one(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            k_reference,
            inventory_path,
            docker=docker,
            kit_skills=kit_skills,
        )
        exit_code = outcome.exit_code
        timeout_marker = outcome.timeout_marker
        protected: ProtectedManifest | None = None
        candidate_success = (
            exit_code == 0
            and not timeout_marker
            and not outcome.oom_killed
        )
        if candidate_success:
            try:
                protected = _validate_discovery(
                    task / f"{STAGE}/workspace",
                    k_reference,
                    invocation.path,
                )
            except (
                Stage3RunnerError,
                pipeline_contract.PipelineContractError,
            ):
                exit_code = 1
        successful = (
            exit_code == 0
            and not timeout_marker
            and not outcome.oom_killed
            and protected is not None
        )
        metadata: dict[str, Any] | None = None
        expected_evidence: dict[str, str] | None = None
        if successful:
            artifact = protected.path.relative_to(task / STAGE).as_posix()
            evidence_path = protected.path.relative_to(
                invocation.path
            ).as_posix()
            metadata = {
                "trust_boundary_sha256": protected.sha256,
                "trust_boundary_artifact": artifact,
            }
            expected_evidence = {
                evidence_path: protected.sha256,
            }

        def prepublication_guard() -> None:
            _verify_post_model_integrity(
                repo,
                run_id,
                problem,
                state,
                invocation,
                k_reference,
                expected_k_hash,
                inventory_path,
                expected_inventory_hash,
                eligibility,
                require_trace=successful,
                protected=protected,
            )

        result = pipeline_contract.finalize_invocation(
            repo,
            run_id,
            problem,
            STAGE,
            invocation.name,
            exit_code=exit_code,
            duration_s=outcome.duration_s,
            timeout_marker=timeout_marker,
            oom_killed=outcome.oom_killed,
            image_id=outcome.image_id,
            result_metadata=metadata,
            prepublication_guard=prepublication_guard,
            expected_evidence=expected_evidence,
        )
        if (
            result["status"] == "TIMEOUT"
            and invocation.name == "001-initial"
            and lemma_total_s > invocation.allocation_s
        ):
            continue
        return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--print-config", action="store_true")
    parser.add_argument("--retry-auth-infrastructure", action="store_true")
    parser.add_argument("run_id")
    parser.add_argument("problem")
    arguments = parser.parse_args(argv)
    try:
        if arguments.print_config:
            print(
                json.dumps(
                    inspect_stage3(
                        arguments.repo,
                        arguments.run_id,
                        arguments.problem,
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        result = run_stage3(
            arguments.repo,
            arguments.run_id,
            arguments.problem,
            retry_auth_infrastructure=arguments.retry_auth_infrastructure,
        )
    except (
        audit_contract.AuditContractError,
        k_rule_inventory.KRuleInventoryError,
        lemma_discovery_contract.LemmaDiscoveryContractError,
        pipeline_contract.PipelineContractError,
        Stage3RunnerError,
    ) as error:
        print(f"Stage 3 failed: {error}", file=sys.stderr)
        return 2
    return 0 if result["status"] == "SUCCEEDED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
