#!/usr/bin/env python3
"""Independent, read-only Stage 3/4 audit checks for the mounted evidence."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from tools import klean_export
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.stage6_resolution_contract import canonical_json_sha256 as resolution_sha256


K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")
OUTPUT_AUDIT_INPUT = Path("/audit-output/audit-input.json")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def regular_tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"unsafe tree root: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"unsafe tree entry: {path}")
    return sorted(entries)


def pipeline_tree_digest(root: Path) -> str:
    """Independent implementation of the selected-artifact tree hash."""

    digest = hashlib.sha256()
    for relative, kind, path in regular_tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def export_tree_digest(root: Path) -> str:
    """Independent implementation of the Stage 4 exporter tree hash."""

    digest = hashlib.sha256()
    for relative, kind, path in regular_tree_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def check(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def main() -> None:
    checks: dict[str, bool] = {}
    audit_input = load_json(AUDIT_INPUT)
    resolution = audit_input["resolution"]
    recorded_hashes = resolution["hashes"]

    check(
        os.environ.get("AUDIT_MODE") == "CLASSIFICATION_ONLY",
        "environment audit mode is CLASSIFICATION_ONLY",
        checks,
    )
    check(
        resolution["mode"] == os.environ.get("AUDIT_MODE"),
        "launcher and environment audit modes agree",
        checks,
    )
    check(
        resolution["condition"] == "bare"
        and resolution["problem_id"] == "136-largest-smallest-integers"
        and resolution["semantics_mode"] == "GENERATED_SEMANTICS",
        "problem, condition, and semantics mode match the requested audit",
        checks,
    )
    check(
        resolution_sha256(resolution) == audit_input["resolved_input_sha256"],
        "signed resolution canonical hash matches",
        checks,
    )
    check(
        AUDIT_INPUT.read_bytes() == OUTPUT_AUDIT_INPUT.read_bytes(),
        "launcher and output audit-input copies are byte-identical",
        checks,
    )

    pipeline_k_hash = pipeline_tree_digest(K_WORKSPACE)
    export_k_hash = export_tree_digest(K_WORKSPACE)
    pipeline_audit_hash = pipeline_tree_digest(K_AUDIT)
    pipeline_generation_hash = pipeline_tree_digest(GENERATION)
    export_generated_hash = export_tree_digest(GENERATED)
    check(
        pipeline_k_hash == recorded_hashes["k_workspace_sha256"],
        "Stage 1 selected-artifact tree hash matches",
        checks,
    )
    check(
        export_k_hash == recorded_hashes["stage1_export_sha256"],
        "Stage 1 exporter tree hash matches",
        checks,
    )
    check(
        pipeline_audit_hash == recorded_hashes["k_audit_sha256"],
        "Stage 2 selected-artifact tree hash matches",
        checks,
    )
    check(
        pipeline_generation_hash == recorded_hashes["klean_generation_sha256"],
        "Stage 4 selected-artifact tree hash matches",
        checks,
    )
    check(
        export_generated_hash == recorded_hashes["generated_tree_sha256"],
        "generated project tree hash matches",
        checks,
    )
    check(
        klean_export.tree_digest(K_WORKSPACE) == export_k_hash
        and klean_export.tree_digest(GENERATED) == export_generated_hash,
        "independent exporter hashes agree with trusted implementation",
        checks,
    )

    source_hashes = {
        relative: sha256_file(path)
        for relative, kind, path in regular_tree_entries(K_WORKSPACE)
        if kind == "file"
    }
    check(
        source_hashes == resolution["stage1_source_hashes"],
        "all Stage 1 per-file source hashes match exactly",
        checks,
    )
    check(
        sha256_file(DISCOVERY) == recorded_hashes["discovery_manifest_sha256"],
        "Stage 3 discovery file hash matches",
        checks,
    )
    check(
        recorded_hashes["lean_workspace_sha256"] is None
        and recorded_hashes["lean_invocation_sha256"] is None,
        "Stage 5 hashes are absent in classification-only mode",
        checks,
    )
    check(
        resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None,
        "Stage 5 paths and result are absent",
        checks,
    )
    check(
        not Path("/candidate").exists(),
        "no Stage 5 candidate is mounted",
        checks,
    )

    # Canonical inventory from the trusted inventory implementation.
    inventory = inventory_verification(K_WORKSPACE)
    protected = load_json(DISCOVERY)
    validated = validate_trust_boundary(K_WORKSPACE, DISCOVERY)
    rules = inventory["rules"]
    classified_entries = protected["rules"]
    source_lines = (K_WORKSPACE / "verification.k").read_text().splitlines()

    check(
        inventory["verification_module"] == "VERIFICATION"
        and inventory["verification_modules"] == ["VERIFICATION"],
        "local verification-module closure is exactly VERIFICATION",
        checks,
    )
    check(len(rules) == 11, "canonical inventory contains 11 rules", checks)
    check(
        inventory["verification_sha256"]
        == resolution["stage1_source_hashes"]["verification.k"],
        "inventory verification.k hash matches frozen source hash",
        checks,
    )
    check(
        inventory["inventory_sha256"] == protected["inventory_sha256"],
        "protected inventory hash matches reconstruction",
        checks,
    )
    check(
        canonical_json_sha256(rules) == inventory["inventory_sha256"],
        "whole reconstructed inventory canonical hash matches",
        checks,
    )
    canonical_ids = [rule["source_rule_id"] for rule in rules]
    protected_ids = [entry["source_rule_id"] for entry in classified_entries]
    check(
        len(protected_ids) == len(set(protected_ids)),
        "protected classification has no duplicate identities",
        checks,
    )
    check(
        protected_ids == canonical_ids,
        "protected classification identities are a complete ordered bijection",
        checks,
    )

    independent_roles_by_start = {
        15: ("DEFINITION", "empty negative-fold recurrence equation"),
        16: ("DEFINITION", "nonempty negative-fold recurrence equation"),
        18: ("DEFINITION", "empty positive-fold recurrence equation"),
        19: ("DEFINITION", "nonempty positive-fold recurrence equation"),
        22: ("DEFINITION", "negative-step helper equation"),
        27: ("DEFINITION", "negative-candidate None equation"),
        28: ("DEFINITION", "negative-candidate integer equation"),
        34: ("DEFINITION", "positive-step helper equation"),
        39: ("DEFINITION", "positive-candidate None equation"),
        40: ("DEFINITION", "positive-candidate integer equation"),
        47: ("DEFINITION", "solutionProgram macro equation"),
    }
    classification_rows: list[dict[str, Any]] = []
    for index, (rule, protected_entry) in enumerate(zip(rules, classified_entries)):
        sliced = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized_hash = sha256_bytes(
            " ".join(rule["text"].split()).encode()
        )
        expected_role, independent_reason = independent_roles_by_start[
            rule["start_line"]
        ]
        check(
            sliced == rule["text"],
            f"rule {index + 1} source span is exact",
            checks,
        )
        check(
            normalized_hash == rule["normalized_sha256"],
            f"rule {index + 1} normalized source hash matches",
            checks,
        )
        check(
            rule["source_rule_id"] == f"rule-{normalized_hash}",
            f"rule {index + 1} source_rule_id matches normalized hash",
            checks,
        )
        check(
            protected_entry["classification"] == expected_role,
            f"rule {index + 1} independent classification agrees",
            checks,
        )
        check(
            "simplification" not in rule["attributes"]
            or expected_role in {"DEFINITION", "DOMAIN_LEMMA"},
            f"rule {index + 1} simplification policy is satisfied",
            checks,
        )
        classification_rows.append(
            {
                "ordinal": index + 1,
                "source_rule_id": rule["source_rule_id"],
                "source_span": {
                    "start_line": rule["start_line"],
                    "end_line": rule["end_line"],
                },
                "normalized_sha256": normalized_hash,
                "attributes": rule["attributes"],
                "independent_classification": expected_role,
                "independent_reason": independent_reason,
                "protected_classification": protected_entry["classification"],
            }
        )
    check(
        set(independent_roles_by_start) == {rule["start_line"] for rule in rules},
        "every reconstructed rule has an independent classification",
        checks,
    )
    check(
        len(validated["definitions"]) == 11
        and not validated["operational_rules"]
        and not validated["proved_derived_lemmas"]
        and not validated["domain_lemmas"],
        "validated partition is 11 definitions and no other rules",
        checks,
    )

    input_manifest = load_json(GENERATION / "input-manifest.json")
    generator_manifest = load_json(GENERATION / "generator-manifest.json")
    export_result = load_json(GENERATION / "export-result.json")
    obligation_map = load_json(GENERATED / "obligation-map.json")
    stored_preflight = load_json(GENERATION / "preflight.json")
    trust_inventory = load_json(GENERATION / "trust-inventory.json")
    toolchain = load_json(TOOLCHAIN_LOCK)

    check(
        input_manifest["definitions"] == validated["definitions"],
        "Stage 4 input definitions exactly match reconstructed classifications",
        checks,
    )
    check(
        input_manifest["operational_rules"] == []
        and input_manifest["proved_derived_lemmas"] == []
        and input_manifest["source_rules"] == [],
        "Stage 4 input has no operational, proved-derived, or domain source rules",
        checks,
    )
    check(
        input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
        "Stage 4 input inventory hash matches",
        checks,
    )
    check(
        input_manifest["verification_sha256"]
        == sha256_file(K_WORKSPACE / "verification.k"),
        "Stage 4 verification.k hash matches",
        checks,
    )
    check(
        input_manifest["frozen_input_sha256"] == export_k_hash
        and input_manifest["stage1_workspace_sha256"] == export_k_hash,
        "Stage 4 input Stage 1 tree bindings match",
        checks,
    )
    check(
        input_manifest["stage3_discovery_manifest_sha256"]
        == sha256_file(DISCOVERY),
        "Stage 4 input Stage 3 binding matches",
        checks,
    )
    check(
        obligation_map
        == {
            "schema_version": 3,
            "source_rules": [],
            "obligations": [],
            "trust_parameters": [],
        },
        "obligation map is the exact empty source/obligation bijection",
        checks,
    )
    check(
        generator_manifest["obligation_count"] == 0
        and generator_manifest["target"] is None,
        "generator manifest records zero obligations and no target",
        checks,
    )
    check(
        generator_manifest["obligation_map_sha256"]
        == sha256_file(GENERATED / "obligation-map.json"),
        "generator obligation-map hash matches",
        checks,
    )
    check(
        generator_manifest["generated_tree_sha256"] == export_generated_hash,
        "generator generated-tree hash matches",
        checks,
    )
    check(
        generator_manifest["provenance"]
        == {
            "generator_image_id": generator_manifest["provenance"][
                "generator_image_id"
            ],
            "inventory_sha256": inventory["inventory_sha256"],
            "stage1_workspace_sha256": export_k_hash,
            "stage3_discovery_manifest_sha256": sha256_file(DISCOVERY),
        },
        "generator provenance hashes match immutable inputs",
        checks,
    )
    check(
        generator_manifest["toolchain"] == toolchain,
        "generator toolchain exactly matches trusted lock",
        checks,
    )
    check(
        all(
            isinstance(generator_manifest[field], str)
            and len(generator_manifest[field]) == 64
            and set(generator_manifest[field]) <= set("0123456789abcdef")
            for field in ("exporter_sha256", "klean_py_sha256")
        ),
        "historical generator-image source hashes are well formed",
        checks,
    )
    check(
        klean_export.target_statement(GENERATED) is None,
        "generated project has no target declaration",
        checks,
    )
    check(
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and export_result["obligation_count"] == 0,
        "export result is no-obligations with count zero",
        checks,
    )
    check(
        export_result["frozen_input_sha256"] == export_k_hash
        and export_result["stage3_discovery_manifest_sha256"]
        == sha256_file(DISCOVERY)
        and export_result["generated_tree_sha256"] == export_generated_hash
        and export_result["trust_inventory_sha256"]
        == sha256_file(GENERATION / "trust-inventory.json"),
        "export-result provenance hashes match",
        checks,
    )
    check(
        stored_preflight == resolution["stage4_preflight"],
        "signed and selected preflight records are identical",
        checks,
    )
    check(
        stored_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and stored_preflight["obligation_count"] == 0
        and stored_preflight["target"] is None,
        "stored preflight records genuine empty-domain status",
        checks,
    )
    check(
        stored_preflight["trust_declaration_count"]
        == len(trust_inventory["allowlist"])
        == 47,
        "trust declaration count matches allowlist",
        checks,
    )
    check(
        resolution["target"] is None
        and resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS",
        "signed target and selected Stage 4 status are no-obligations",
        checks,
    )
    check(
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == pipeline_generation_hash
        and resolution["selections"]["k_audit"]["artifact_sha256"]
        == pipeline_audit_hash,
        "selected artifact hashes match reconstructed tree hashes",
        checks,
    )

    result = {
        "audit_identity": {
            "AUDIT_MODE": os.environ.get("AUDIT_MODE"),
            "problem_id": resolution["problem_id"],
            "condition": resolution["condition"],
            "semantics_mode": resolution["semantics_mode"],
        },
        "hashes": {
            "resolved_input_sha256": resolution_sha256(resolution),
            "k_workspace_pipeline_sha256": pipeline_k_hash,
            "stage1_export_sha256": export_k_hash,
            "k_audit_pipeline_sha256": pipeline_audit_hash,
            "discovery_manifest_sha256": sha256_file(DISCOVERY),
            "klean_generation_pipeline_sha256": pipeline_generation_hash,
            "generated_tree_sha256": export_generated_hash,
            "verification_sha256": inventory["verification_sha256"],
            "inventory_sha256": inventory["inventory_sha256"],
            "obligation_map_sha256": sha256_file(
                GENERATED / "obligation-map.json"
            ),
            "trust_inventory_sha256": sha256_file(
                GENERATION / "trust-inventory.json"
            ),
            "historical_generator_exporter_sha256": generator_manifest[
                "exporter_sha256"
            ],
            "historical_generator_klean_py_sha256": generator_manifest[
                "klean_py_sha256"
            ],
            "audit_time_klean_export_sha256": sha256_file(
                Path("/reference/tools/klean_export.py")
            ),
            "audit_time_klean_py_sha256": sha256_file(
                Path("/reference/tools/klean.py")
            ),
            "audit_time_mechanical_checker_lock_sha256": audit_input["audit"][
                "mechanical_checker_lock_sha256"
            ],
        },
        "provenance_scope_note": (
            "The historical generator source files and the aggregate audit-time "
            "mechanical-checker lock preimage are not separately mounted. Their "
            "recorded digests are retained as provenance; all mounted file/tree "
            "referents are rehashed above."
        ),
        "inventory": inventory,
        "independent_classifications": classification_rows,
        "domain_rule_ids": [],
        "target": None,
        "candidate_present": Path("/candidate").exists(),
        "checks": checks,
        "check_count": len(checks),
        "all_checks_passed": all(checks.values()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
