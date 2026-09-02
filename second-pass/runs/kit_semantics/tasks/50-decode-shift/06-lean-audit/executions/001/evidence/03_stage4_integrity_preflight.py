#!/usr/bin/env python3
"""Authenticate Stage 4 producers, verify hashes, and rerun preflight."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from tools import (
    klean_export,
    klean_preflight,
    pipeline_contract,
    stage6_resolution_contract,
)


EVIDENCE = Path("/audit-output/evidence")
OUTPUT = EVIDENCE / "03_stage4_integrity_preflight.json"
LEAN_TOOLCHAIN_BIN = Path(
    "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin"
)
LEAN_APP_PATH_SHIM = Path("/tmp/audit-work/fix_lean_app_path.so")
AUDIT_INPUT_PATH = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK_PATH = Path("/reference/klean-toolchain.lock.json")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = load_json(AUDIT_INPUT_PATH)
resolution, resolved_input_sha256 = (
    stage6_resolution_contract.verify_audit_input(audit_input)
)
generator_manifest = load_json(GENERATION / "generator-manifest.json")
input_manifest = load_json(GENERATION / "input-manifest.json")
export_result = load_json(GENERATION / "export-result.json")
obligation_map = load_json(GENERATED / "obligation-map.json")
source_manifest = load_json(PRODUCERS / "source-manifest.json")
toolchain_lock = load_json(LOCK_PATH)

producer_file_hashes = {
    "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    "klean.py": sha256_file(PRODUCERS / "klean.py"),
}
source_manifest_hashes = source_manifest.get("files")
generator_image_id = generator_manifest.get("provenance", {}).get(
    "generator_image_id"
)
source_image_id = source_manifest.get("generator_image_id")
audit_producer_component = Path(
    resolution["generation_producer_sources"]
).name

producer_checks = {
    "source_manifest_has_exact_producer_set": (
        isinstance(source_manifest_hashes, dict)
        and set(source_manifest_hashes) == set(producer_file_hashes)
    ),
    "producer_files_match_source_manifest": (
        source_manifest_hashes == producer_file_hashes
    ),
    "klean_export_matches_generator_manifest": (
        producer_file_hashes["klean_export.py"]
        == generator_manifest.get("exporter_sha256")
    ),
    "klean_py_matches_generator_manifest": (
        producer_file_hashes["klean.py"]
        == generator_manifest.get("klean_py_sha256")
    ),
    "generator_image_matches_source_manifest": (
        generator_image_id == source_image_id
    ),
    "generator_image_matches_audit_input_path": (
        isinstance(generator_image_id, str)
        and generator_image_id.startswith("sha256:")
        and audit_producer_component == generator_image_id.removeprefix("sha256:")
    ),
}

producer_tree_sha256 = pipeline_contract.sha256_tree(PRODUCERS)
hash_observations = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": producer_tree_sha256,
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
recorded_hashes = resolution["hashes"]
hash_comparison = {
    key: {
        "recorded": recorded_hashes.get(key),
        "observed": value,
        "matches": recorded_hashes.get(key) == value,
    }
    for key, value in hash_observations.items()
}

stage1_expected = resolution["stage1_source_hashes"]
stage1_entries = klean_export._tree_entries(WORKSPACE)
stage1_actual_files = {
    relative: sha256_file(path)
    for relative, kind, path in stage1_entries
    if kind == "file"
}
stage1_missing = sorted(set(stage1_expected) - set(stage1_actual_files))
stage1_extra = sorted(set(stage1_actual_files) - set(stage1_expected))
stage1_mismatches = sorted(
    relative
    for relative in set(stage1_expected) & set(stage1_actual_files)
    if stage1_expected[relative] != stage1_actual_files[relative]
)

target_statement = klean_export.target_statement(GENERATED)
stage4_checks = {
    "audit_input_contract_valid": True,
    "audit_mode_environment_matches_resolution": (
        os.environ.get("AUDIT_MODE") == resolution["mode"]
    ),
    "classification_only_mode": resolution["mode"] == "CLASSIFICATION_ONLY",
    "candidate_absent": not Path("/candidate").exists(),
    "all_recorded_hashes_match": all(
        item["matches"] for item in hash_comparison.values()
    ),
    "all_stage1_source_hashes_match": (
        not stage1_missing and not stage1_extra and not stage1_mismatches
    ),
    "generator_toolchain_matches_lock": (
        generator_manifest.get("toolchain") == toolchain_lock
    ),
    "generator_inventory_hash_matches_stage3": (
        generator_manifest.get("provenance", {}).get("inventory_sha256")
        == input_manifest.get("inventory_sha256")
        == load_json(DISCOVERY).get("inventory_sha256")
    ),
    "generator_obligation_map_hash_matches": (
        generator_manifest.get("obligation_map_sha256")
        == sha256_file(GENERATED / "obligation-map.json")
    ),
    "zero_source_rules": input_manifest.get("source_rules") == [],
    "zero_obligations": obligation_map.get("obligations") == [],
    "zero_trust_parameters": obligation_map.get("trust_parameters") == [],
    "source_rule_obligation_bijection": (
        input_manifest.get("source_rules")
        == obligation_map.get("source_rules")
        == []
    ),
    "generator_obligation_count_zero": (
        generator_manifest.get("obligation_count") == 0
        and export_result.get("obligation_count") == 0
    ),
    "no_generated_target": (
        generator_manifest.get("target") is None
        and resolution.get("target") is None
        and target_statement is None
    ),
    "status_is_no_obligations": (
        resolution.get("selections", {})
        .get("klean_generation", {})
        .get("status")
        == "KLEAN_NO_OBLIGATIONS"
        and export_result.get("status") == "KLEAN_NO_OBLIGATIONS"
    ),
}

producer_ok = all(producer_checks.values()) and hash_comparison[
    "generation_producer_sources_sha256"
]["matches"]

partial: dict[str, Any] = {
    "command": (
        "PYTHONPATH=/reference python3 "
        "/audit-output/evidence/03_stage4_integrity_preflight.py"
    ),
    "resolved_input_sha256": resolved_input_sha256,
    "audit_mode_environment": os.environ.get("AUDIT_MODE"),
    "audit_mode_resolution": resolution["mode"],
    "producer_authentication": {
        "producer_file_hashes": producer_file_hashes,
        "source_manifest_file_hashes": source_manifest_hashes,
        "generator_manifest_exporter_sha256": generator_manifest.get(
            "exporter_sha256"
        ),
        "generator_manifest_klean_py_sha256": generator_manifest.get(
            "klean_py_sha256"
        ),
        "source_manifest_generator_image_id": source_image_id,
        "generator_manifest_generator_image_id": generator_image_id,
        "audit_input_producer_path_component": audit_producer_component,
        "producer_tree_sha256": producer_tree_sha256,
        "checks": producer_checks,
        "authenticated": producer_ok,
    },
    "recorded_hash_comparison": hash_comparison,
    "stage1_source_hash_comparison": {
        "recorded_file_count": len(stage1_expected),
        "observed_file_count": len(stage1_actual_files),
        "missing": stage1_missing,
        "extra": stage1_extra,
        "mismatches": stage1_mismatches,
    },
    "stage4_structural_checks_before_preflight": stage4_checks,
}

if not producer_ok:
    partial["status"] = "AUDIT_ERROR"
    partial["error"] = "generation-time producer authentication failed"
    OUTPUT.write_text(json.dumps(partial, indent=2, sort_keys=True) + "\n")
    print(json.dumps(partial, indent=2, sort_keys=True))
    raise SystemExit(2)


preflight_run = 0


def recording_run(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    global preflight_run
    preflight_run += 1
    try:
        command_environment = dict(os.environ)
        command_environment["PATH"] = (
            str(LEAN_TOOLCHAIN_BIN)
            + os.pathsep
            + command_environment.get("PATH", "")
        )
        command_environment["LD_PRELOAD"] = str(LEAN_APP_PATH_SHIM)
        completed = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            env=command_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        code = completed.returncode
        output = completed.stdout
    except subprocess.TimeoutExpired as error:
        code = 124
        output = (
            (error.stdout or "")
            + (error.stderr or "")
            + f"\nTIMEOUT after {timeout}s\n"
        )
    log_path = EVIDENCE / f"03c_preflight_command_{preflight_run}.log"
    log_path.write_text(
        "COMMAND: "
        + " ".join(command)
        + "\nCWD: "
        + str(cwd)
        + "\nTOOLCHAIN_BIN_PREPENDED_TO_PATH: "
        + str(LEAN_TOOLCHAIN_BIN)
        + "\nLEAN_APP_PATH_SHIM: "
        + str(LEAN_APP_PATH_SHIM)
        + f"\nEXIT_CODE: {code}\nOUTPUT_BEGIN\n"
        + output
        + ("" if output.endswith("\n") or not output else "\n")
        + "OUTPUT_END\n"
    )
    return code, output


try:
    returned_preflight = klean_preflight.check_generation(
        WORKSPACE,
        DISCOVERY,
        GENERATION,
        toolchain_lock=LOCK_PATH,
        run_command=recording_run,
    )
except Exception as error:
    partial["status"] = "PREFLIGHT_ERROR"
    partial["error"] = f"{type(error).__name__}: {error}"
    OUTPUT.write_text(json.dumps(partial, indent=2, sort_keys=True) + "\n")
    print(json.dumps(partial, indent=2, sort_keys=True))
    raise

partial["returned_preflight"] = returned_preflight
partial["returned_preflight_matches_recorded"] = (
    returned_preflight == resolution["stage4_preflight"]
    == load_json(GENERATION / "preflight.json")
)
partial["status"] = "PASS"
OUTPUT.write_text(json.dumps(partial, indent=2, sort_keys=True) + "\n")
print(json.dumps(partial, indent=2, sort_keys=True))
