#!/usr/bin/env python3
"""Independent hash reconciliation for the mounted Stage 3/4 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
STAGE1 = Path("/reference/k-proof")
STAGE2 = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> dict[str, object]:
    return {
        "label": label,
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(document)
hashes = resolution["hashes"]
generator = json.loads((GENERATION / "generator-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
toolchain_lock = json.loads(TOOLCHAIN_LOCK.read_text())

checks: list[dict[str, object]] = []
checks.extend(
    [
        check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"]),
        check(
            "resolved_input_sha256",
            resolved_digest,
            document["resolved_input_sha256"],
        ),
        check(
            "k_workspace_sha256 (pipeline tree)",
            pipeline_contract.sha256_tree(STAGE1),
            hashes["k_workspace_sha256"],
        ),
        check(
            "stage1_export_sha256 (Klean tree)",
            klean_export.tree_digest(STAGE1),
            hashes["stage1_export_sha256"],
        ),
        check(
            "k_audit_sha256 (pipeline tree)",
            pipeline_contract.sha256_tree(STAGE2),
            hashes["k_audit_sha256"],
        ),
        check(
            "discovery_manifest_sha256",
            sha256_file(DISCOVERY),
            hashes["discovery_manifest_sha256"],
        ),
        check(
            "klean_generation_sha256 (pipeline tree)",
            pipeline_contract.sha256_tree(GENERATION),
            hashes["klean_generation_sha256"],
        ),
        check(
            "generation_producer_sources_sha256 (pipeline tree)",
            pipeline_contract.sha256_tree(PRODUCERS),
            hashes["generation_producer_sources_sha256"],
        ),
        check(
            "generated_tree_sha256 (Klean tree)",
            klean_export.tree_digest(GENERATED),
            hashes["generated_tree_sha256"],
        ),
        check("lean_workspace_sha256", hashes["lean_workspace_sha256"], None),
        check("lean_invocation_sha256", hashes["lean_invocation_sha256"], None),
        check("classification-only target", resolution["target"], None),
        check("classification-only Stage 5 result", resolution["stage5_result"], None),
        check("candidate absent", Path("/candidate").exists(), False),
    ]
)

stage1_expected = resolution["stage1_source_hashes"]
stage1_actual = {
    path.relative_to(STAGE1).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(STAGE1, "Stage 1")
}
stage1_missing = sorted(set(stage1_expected) - set(stage1_actual))
stage1_extra = sorted(set(stage1_actual) - set(stage1_expected))
stage1_mismatches = sorted(
    name
    for name in set(stage1_expected) & set(stage1_actual)
    if stage1_expected[name] != stage1_actual[name]
)
checks.extend(
    [
        check("Stage 1 source file count", len(stage1_actual), len(stage1_expected)),
        check("Stage 1 missing files", stage1_missing, []),
        check("Stage 1 extra files", stage1_extra, []),
        check("Stage 1 per-file SHA-256 mismatches", stage1_mismatches, []),
    ]
)

image_id = generator["provenance"]["generator_image_id"]
checks.extend(
    [
        check(
            "producer image ID: source manifest",
            source_manifest["generator_image_id"],
            image_id,
        ),
        check(
            "producer image ID: audit-input path",
            "sha256:" + Path(resolution["generation_producer_sources"]).name,
            image_id,
        ),
        check(
            "klean_export.py producer SHA-256",
            sha256_file(PRODUCERS / "klean_export.py"),
            generator["exporter_sha256"],
        ),
        check(
            "klean.py producer SHA-256",
            sha256_file(PRODUCERS / "klean.py"),
            generator["klean_py_sha256"],
        ),
        check(
            "producer file map",
            source_manifest["files"],
            {
                "klean_export.py": generator["exporter_sha256"],
                "klean.py": generator["klean_py_sha256"],
            },
        ),
        check(
            "producer bundle file set",
            sorted(path.name for path in PRODUCERS.iterdir()),
            ["klean.py", "klean_export.py", "source-manifest.json"],
        ),
    ]
)

discovery_sha = sha256_file(DISCOVERY)
stage1_klean_sha = klean_export.tree_digest(STAGE1)
generated_sha = klean_export.tree_digest(GENERATED)
trust_sha = sha256_file(GENERATION / "trust-inventory.json")
checks.extend(
    [
        check(
            "input frozen_input_sha256",
            input_manifest["frozen_input_sha256"],
            stage1_klean_sha,
        ),
        check(
            "input stage1_workspace_sha256",
            input_manifest["stage1_workspace_sha256"],
            stage1_klean_sha,
        ),
        check(
            "input discovery SHA-256",
            input_manifest["stage3_discovery_manifest_sha256"],
            discovery_sha,
        ),
        check(
            "input verification.k SHA-256",
            input_manifest["verification_sha256"],
            sha256_file(STAGE1 / "verification.k"),
        ),
        check(
            "generator generated tree SHA-256",
            generator["generated_tree_sha256"],
            generated_sha,
        ),
        check(
            "generator obligation-map SHA-256",
            generator["obligation_map_sha256"],
            sha256_file(GENERATED / "obligation-map.json"),
        ),
        check("generator toolchain lock", generator["toolchain"], toolchain_lock),
        check(
            "export frozen input SHA-256",
            export_result["frozen_input_sha256"],
            stage1_klean_sha,
        ),
        check(
            "export discovery SHA-256",
            export_result["stage3_discovery_manifest_sha256"],
            discovery_sha,
        ),
        check(
            "export generated tree SHA-256",
            export_result["generated_tree_sha256"],
            generated_sha,
        ),
        check(
            "export trust-inventory SHA-256",
            export_result["trust_inventory_sha256"],
            trust_sha,
        ),
        check(
            "Stage 4 selection artifact SHA-256",
            resolution["selections"]["klean_generation"]["artifact_sha256"],
            hashes["klean_generation_sha256"],
        ),
        check(
            "Stage 2 selection artifact SHA-256",
            resolution["selections"]["k_audit"]["artifact_sha256"],
            hashes["k_audit_sha256"],
        ),
    ]
)

status_expected = "OK" if obligation_map["obligations"] else "KLEAN_NO_OBLIGATIONS"
checks.extend(
    [
        check("export status", export_result["status"], status_expected),
        check("generator obligation count", generator["obligation_count"], len(obligation_map["obligations"])),
        check("export obligation count", export_result["obligation_count"], len(obligation_map["obligations"])),
        check("generator target for empty obligations", generator["target"], None),
    ]
)

failed = [item for item in checks if not item["match"]]
print(
    json.dumps(
        {
            "schema_version": 1,
            "check_count": len(checks),
            "failed_count": len(failed),
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(1 if failed else 0)
