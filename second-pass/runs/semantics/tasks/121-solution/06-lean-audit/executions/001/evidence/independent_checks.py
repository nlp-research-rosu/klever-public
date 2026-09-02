#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import expected_target_definition, target_statement


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entries(root: Path) -> list[tuple[str, str, Path]]:
    root_mode = root.stat(follow_symlinks=False).st_mode
    assert stat.S_ISDIR(root_mode), f"not a real directory: {root}"
    result: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                result.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return sorted(result)


def pipeline_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def export_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def check_equal(label: str, observed: Any, expected: Any) -> dict[str, Any]:
    assert observed == expected, (
        f"{label} mismatch:\nobserved={observed!r}\nexpected={expected!r}"
    )
    return {"label": label, "status": "MATCH", "value": observed}


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    hashes = resolution["hashes"]
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    trust_inventory = GENERATION / "trust-inventory.json"
    recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
    discovery = json.loads(DISCOVERY.read_text())
    lock = json.loads(LOCK.read_text())
    result: dict[str, Any] = {"checks": []}

    checks = result["checks"]
    checks.append(
        check_equal("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
    )
    checks.append(
        check_equal(
            "resolved_input_sha256",
            canonical_json_sha256(resolution),
            audit["resolved_input_sha256"],
        )
    )

    pipeline_trees = {
        "k_workspace_sha256": K_PROOF,
        "k_audit_sha256": K_AUDIT,
        "klean_generation_sha256": GENERATION,
        "generation_producer_sources_sha256": PRODUCERS,
    }
    for field, root in pipeline_trees.items():
        checks.append(
            check_equal(field, pipeline_tree_sha256(root), hashes[field])
        )
    checks.append(
        check_equal(
            "stage1_export_sha256",
            export_tree_sha256(K_PROOF),
            hashes["stage1_export_sha256"],
        )
    )
    checks.append(
        check_equal(
            "generated_tree_sha256",
            export_tree_sha256(GENERATED),
            hashes["generated_tree_sha256"],
        )
    )
    checks.append(
        check_equal(
            "discovery_manifest_sha256",
            file_sha256(DISCOVERY),
            hashes["discovery_manifest_sha256"],
        )
    )
    checks.append(check_equal("lean_workspace_sha256", None, hashes["lean_workspace_sha256"]))
    checks.append(
        check_equal("lean_invocation_sha256", None, hashes["lean_invocation_sha256"])
    )

    observed_stage1_files = {
        relative: file_sha256(path)
        for relative, kind, path in entries(K_PROOF)
        if kind == "file"
    }
    checks.append(
        check_equal(
            "stage1_source_hashes",
            observed_stage1_files,
            resolution["stage1_source_hashes"],
        )
    )

    producer_names = sorted({
        relative for relative, kind, _path in entries(PRODUCERS) if kind == "file"
    })
    checks.append(
        check_equal(
            "producer file set",
            producer_names,
            ["klean.py", "klean_export.py", "source-manifest.json"],
        )
    )
    producer_file_hashes = {
        "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
        "klean.py": file_sha256(PRODUCERS / "klean.py"),
    }
    checks.append(
        check_equal(
            "producer source manifest hashes",
            producer_file_hashes,
            source_manifest["files"],
        )
    )
    checks.append(
        check_equal(
            "producer hashes in generator manifest",
            producer_file_hashes,
            {
                "klean_export.py": generator["exporter_sha256"],
                "klean.py": generator["klean_py_sha256"],
            },
        )
    )
    generator_image_id = generator["provenance"]["generator_image_id"]
    checks.append(
        check_equal(
            "generator image ID: source manifest",
            source_manifest["generator_image_id"],
            generator_image_id,
        )
    )
    recorded_source_path = Path(resolution["generation_producer_sources"])
    checks.append(
        check_equal(
            "generator image ID: audit input path",
            "sha256:" + recorded_source_path.name,
            generator_image_id,
        )
    )

    inventory = inventory_verification(K_PROOF)
    result["inventory"] = inventory
    rules = inventory["rules"]
    for rule in rules:
        source_lines = (K_PROOF / "verification.k").read_text().splitlines()
        span_text = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized_hash = hashlib.sha256(
            " ".join(span_text.split()).encode()
        ).hexdigest()
        assert span_text == rule["text"], (
            f"source span text mismatch for {rule['source_rule_id']}"
        )
        assert normalized_hash == rule["normalized_sha256"]
        assert rule["source_rule_id"] == f"rule-{normalized_hash}"
    checks.append(
        {
            "label": "inventory span/hash/source_rule_id reconstruction",
            "status": "MATCH",
            "value": len(rules),
        }
    )
    checks.append(
        check_equal(
            "inventory_sha256",
            canonical_json_sha256(rules),
            inventory["inventory_sha256"],
        )
    )
    checks.append(
        check_equal(
            "discovery inventory_sha256",
            discovery["inventory_sha256"],
            inventory["inventory_sha256"],
        )
    )
    inventory_ids = [rule["source_rule_id"] for rule in rules]
    discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    assert len(discovery_ids) == len(set(discovery_ids))
    checks.append(
        check_equal(
            "ordered inventory/discovery identity bijection",
            discovery_ids,
            inventory_ids,
        )
    )

    classification_by_id = {
        entry["source_rule_id"]: entry for entry in discovery["rules"]
    }
    categories = {
        "definitions": "DEFINITION",
        "operational_rules": "OPERATIONAL_RULE",
        "proved_derived_lemmas": "PROVED_DERIVED_LEMMA",
        "source_rules": "DOMAIN_LEMMA",
    }
    classified_counts: dict[str, int] = {}
    for manifest_field, classification in categories.items():
        expected = []
        for rule in rules:
            classified = classification_by_id[rule["source_rule_id"]]
            if classified["classification"] == classification:
                expected.append({**rule, **classified})
        checks.append(
            check_equal(
                f"input manifest {manifest_field}",
                input_manifest[manifest_field],
                expected,
            )
        )
        classified_counts[classification] = len(expected)
    result["classification_counts"] = classified_counts
    simplification_ids = [
        rule["source_rule_id"]
        for rule in rules
        if "simplification" in rule["attributes"]
    ]
    result["simplification_rule_ids"] = simplification_ids
    for source_rule_id in simplification_ids:
        assert classification_by_id[source_rule_id]["classification"] in {
            "DEFINITION",
            "DOMAIN_LEMMA",
        }

    domain_entries = input_manifest["source_rules"]
    checks.append(
        check_equal("obligation map source rules", obligation_map["source_rules"], domain_entries)
    )
    obligation_ids = [
        obligation["source_rule_id"]
        for obligation in obligation_map["obligations"]
    ]
    domain_ids = [entry["source_rule_id"] for entry in domain_entries]
    assert len(obligation_ids) == len(set(obligation_ids))
    checks.append(
        check_equal("source-rule/obligation identity bijection", obligation_ids, domain_ids)
    )
    checks.append(
        check_equal(
            "generator obligation count",
            generator["obligation_count"],
            len(obligation_map["obligations"]),
        )
    )
    checks.append(
        check_equal(
            "obligation map SHA-256",
            file_sha256(GENERATED / "obligation-map.json"),
            generator["obligation_map_sha256"],
        )
    )

    expected_definition = expected_target_definition(obligation_map)
    observed_target = target_statement(GENERATED)
    checks.append(check_equal("expected generated target", expected_definition, None))
    checks.append(check_equal("generated target statement", observed_target, None))
    checks.append(check_equal("generator manifest target", generator["target"], None))
    checks.append(check_equal("audit input target", resolution["target"], None))
    checks.append(
        check_equal("audit input Stage 4 target", resolution["stage4_preflight"]["target"], None)
    )

    checks.append(check_equal("generator toolchain lock", generator["toolchain"], lock))
    checks.append(
        check_equal(
            "generator generated-tree hash",
            generator["generated_tree_sha256"],
            hashes["generated_tree_sha256"],
        )
    )
    checks.append(
        check_equal(
            "input manifest Stage 1 hash",
            input_manifest["stage1_workspace_sha256"],
            hashes["stage1_export_sha256"],
        )
    )
    checks.append(
        check_equal(
            "input manifest discovery hash",
            input_manifest["stage3_discovery_manifest_sha256"],
            hashes["discovery_manifest_sha256"],
        )
    )
    checks.append(
        check_equal(
            "export-result trust inventory hash",
            export_result["trust_inventory_sha256"],
            file_sha256(trust_inventory),
        )
    )
    checks.append(
        check_equal(
            "recorded/audit preflight",
            recorded_preflight,
            resolution["stage4_preflight"],
        )
    )
    checks.append(
        check_equal(
            "KLEAN_NO_OBLIGATIONS status",
            (
                export_result["status"],
                recorded_preflight["status"],
                resolution["selections"]["klean_generation"]["status"],
            ),
            (
                "KLEAN_NO_OBLIGATIONS",
                "KLEAN_NO_OBLIGATIONS",
                "KLEAN_NO_OBLIGATIONS",
            ),
        )
    )
    checks.append(
        check_equal("Stage 5 result", resolution["stage5_result"], None)
    )
    checks.append(
        check_equal("candidate absent", Path("/candidate").exists(), False)
    )

    result["status"] = "PASS"
    if "--summary" in sys.argv[1:]:
        summary = {
            "status": result["status"],
            "check_count": len(checks),
            "classification_counts": classified_counts,
            "inventory_rule_count": len(rules),
            "inventory_sha256": inventory["inventory_sha256"],
            "simplification_rule_ids": simplification_ids,
            "domain_source_rule_ids": domain_ids,
            "obligation_source_rule_ids": obligation_ids,
            "target": observed_target,
            "candidate_present": Path("/candidate").exists(),
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
