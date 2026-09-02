#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.klean_preflight import check_generation
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_file, sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


AUDIT_INPUT = Path("/audit-input.json")
FROZEN = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")

audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = verify_audit_input(audit_document)
expected_hashes = resolution["hashes"]

observed_hashes = {
    "k_workspace_sha256": sha256_tree(FROZEN),
    "stage1_export_sha256": klean_export.tree_digest(FROZEN),
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(GENERATION),
    "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
assert observed_hashes == expected_hashes
assert (
    resolution["selections"]["k_audit"]["artifact_sha256"]
    == observed_hashes["k_audit_sha256"]
)
assert (
    resolution["selections"]["klean_generation"]["artifact_sha256"]
    == observed_hashes["klean_generation_sha256"]
)
assert resolution["lean_workspace"] is None
assert resolution["lean_invocation"] is None
assert resolution["stage5_result"] is None

observed_stage1_sources = {
    path.relative_to(FROZEN).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(FROZEN.rglob("*"))
    if path.is_file()
}
assert observed_stage1_sources == resolution["stage1_source_hashes"]

source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
toolchain_lock = json.loads(LOCK.read_text())

producer_hashes = {
    "klean.py": sha256_file(PRODUCERS / "klean.py"),
    "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
}
assert producer_hashes == source_manifest["files"]
assert producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"]
assert (
    producer_hashes["klean_export.py"]
    == generator_manifest["exporter_sha256"]
)
producer_image_id = source_manifest["generator_image_id"]
assert producer_image_id == generator_manifest["provenance"]["generator_image_id"]
assert producer_image_id.removeprefix("sha256:") == Path(
    resolution["generation_producer_sources"]
).name
assert generator_manifest["toolchain"] == toolchain_lock

validated = validate_trust_boundary(FROZEN, DISCOVERY)
assert input_manifest["definitions"] == validated["definitions"]
assert input_manifest["operational_rules"] == validated["operational_rules"]
assert (
    input_manifest["proved_derived_lemmas"]
    == validated["proved_derived_lemmas"]
)
domain_source_rules = klean_export._domain_source_rules(
    validated, sha256_file(DISCOVERY)
)
assert input_manifest["source_rules"] == domain_source_rules
assert obligation_map["source_rules"] == domain_source_rules
assert obligation_map["obligations"] == []
assert obligation_map["trust_parameters"] == []
assert generator_manifest["obligation_count"] == 0
assert generator_manifest["target"] is None
assert resolution["target"] is None
assert klean_export.expected_target_definition(obligation_map) is None
assert klean_export.target_statement(GENERATED) is None

preflight = check_generation(
    FROZEN,
    DISCOVERY,
    GENERATION,
    toolchain_lock=LOCK,
)
assert preflight["status"] == "KLEAN_NO_OBLIGATIONS"
assert preflight["obligation_count"] == 0
assert preflight["target"] is None
recorded_preflight = resolution["stage4_preflight"]
assert {
    key: value for key, value in preflight.items() if key != "diagnostics"
} == {
    key: value
    for key, value in recorded_preflight.items()
    if key != "diagnostics"
}
assert len(preflight["diagnostics"]) == len(recorded_preflight["diagnostics"])
for observed, recorded in zip(
    preflight["diagnostics"], recorded_preflight["diagnostics"], strict=True
):
    assert observed["command"] == recorded["command"]
    assert observed["exit_code"] == recorded["exit_code"] == 0
    assert (
        hashlib.sha256(recorded["output_tail"].encode()).hexdigest()
        == recorded["output_sha256"]
    )
    normalize_build_line = lambda line: re.sub(
        r"^✔ \[\d+/\d+\] Built ", "Built ", line
    )
    assert sorted(
        normalize_build_line(line)
        for line in observed["output_tail"].splitlines()
    ) == sorted(
        normalize_build_line(line)
        for line in recorded["output_tail"].splitlines()
    )

print(
    json.dumps(
        {
            "audit_mode_env_expected": resolution["mode"],
            "resolved_input_sha256": resolved_digest,
            "observed_hashes": observed_hashes,
            "stage1_source_hashes": observed_stage1_sources,
            "producer_file_hashes": producer_hashes,
            "producer_image_id": producer_image_id,
            "producer_identity": "PASS",
            "input_manifest_classification_arrays": "EXACT_MATCH",
            "domain_source_rule_count": len(domain_source_rules),
            "obligation_source_rule_ids": [
                item["source_rule_id"] for item in domain_source_rules
            ],
            "generated_obligation_count": len(obligation_map["obligations"]),
            "generated_target": klean_export.target_statement(GENERATED),
            "launcher_stage4_preflight_structural_match": True,
            "launcher_stage4_preflight_diagnostics_exact_match": (
                preflight["diagnostics"] == recorded_preflight["diagnostics"]
            ),
            "preflight_returned_evidence": preflight,
        },
        indent=2,
        sort_keys=True,
    )
)
