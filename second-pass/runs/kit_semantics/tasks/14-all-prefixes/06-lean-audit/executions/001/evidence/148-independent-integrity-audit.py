#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


ROOT = Path("/reference")
OUTPUT = Path("/audit-output")


def load(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_bytes())
    assert isinstance(document, dict), path
    return document


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                hashes[relative] = file_sha256(path)
            else:
                raise AssertionError(f"non-regular Stage 1 entry: {relative}")
    return dict(sorted(hashes.items()))


checks: list[dict[str, Any]] = []


def display(value: Any) -> Any:
    if isinstance(value, set):
        value = sorted(value)
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
    except TypeError:
        return repr(value)
    if len(encoded) <= 1000:
        return value
    return {
        "summary_type": type(value).__name__,
        "item_count": len(value) if hasattr(value, "__len__") else None,
        "canonical_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
    }


def check(name: str, observed: Any, expected: Any) -> None:
    passed = observed == expected
    checks.append(
        {
            "name": name,
            "passed": passed,
            "observed": display(observed),
            "expected": display(expected),
        }
    )
    if not passed:
        raise AssertionError(
            f"{name}: observed {observed!r}, expected {expected!r}"
        )


audit_input = load(Path("/audit-input.json"))
resolution = audit_input["resolution"]
source_manifest = load(ROOT / "generation-tools/source-manifest.json")
generator_manifest = load(ROOT / "klean-generation/generator-manifest.json")
input_manifest = load(ROOT / "klean-generation/input-manifest.json")
export_result = load(ROOT / "klean-generation/export-result.json")
obligation_map = load(
    ROOT / "klean-generation/generated/obligation-map.json"
)
trust_inventory = load(ROOT / "klean-generation/trust-inventory.json")
discovery = load(ROOT / "lemma-discovery.json")
toolchain_lock = load(ROOT / "klean-toolchain.lock.json")
mechanical_lock_path = Path(
    "/opt/humaneval/data/klean-audit-tools.lock.json"
)
mechanical_lock = load(mechanical_lock_path)
rerun_preflight = load(
    OUTPUT / "evidence/122-rerun-check-generation-shimmed.json"
)

# Launcher envelope and mode.
check("audit input schema", audit_input["schema_version"], 4)
check(
    "resolved input canonical digest",
    hashlib.sha256(
        json.dumps(
            resolution,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    ).hexdigest(),
    audit_input["resolved_input_sha256"],
)
check("launcher mode versus environment", resolution["mode"], os.environ["AUDIT_MODE"])
check("problem id", resolution["problem_id"], "14-all-prefixes")
check("condition", resolution["condition"], "kit-semantics")
check("semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
check(
    "mechanical checker lock hash",
    file_sha256(mechanical_lock_path),
    audit_input["audit"]["mechanical_checker_lock_sha256"],
)
check("mechanical checker lock schema", mechanical_lock["schema_version"], 1)
check(
    "mechanical checker lock bundle",
    mechanical_lock["bundle"],
    "stage6-mechanical-checker",
)
for relative, expected_hash in sorted(mechanical_lock["files"].items()):
    check(
        f"mechanical checker file {relative}",
        file_sha256(ROOT / relative),
        expected_hash,
    )

# Canonical mounted-tree and file hashes in the signed launcher resolution.
signed_hashes = resolution["hashes"]
check(
    "Stage 1 mounted tree hash",
    sha256_tree(ROOT / "k-proof"),
    signed_hashes["k_workspace_sha256"],
)
check(
    "Stage 2 mounted tree hash",
    sha256_tree(ROOT / "k-audit"),
    signed_hashes["k_audit_sha256"],
)
check(
    "Stage 4 mounted tree hash",
    sha256_tree(ROOT / "klean-generation"),
    signed_hashes["klean_generation_sha256"],
)
check(
    "producer bundle tree hash",
    sha256_tree(ROOT / "generation-tools"),
    signed_hashes["generation_producer_sources_sha256"],
)
check(
    "Stage 1 frozen export digest",
    tree_digest(ROOT / "k-proof"),
    signed_hashes["stage1_export_sha256"],
)
check(
    "generated project digest",
    tree_digest(ROOT / "klean-generation/generated"),
    signed_hashes["generated_tree_sha256"],
)
check(
    "discovery manifest file hash",
    file_sha256(ROOT / "lemma-discovery.json"),
    signed_hashes["discovery_manifest_sha256"],
)
check("Lean workspace hash absent", signed_hashes["lean_workspace_sha256"], None)
check("Lean invocation hash absent", signed_hashes["lean_invocation_sha256"], None)

stage1_hashes = regular_file_hashes(ROOT / "k-proof")
check(
    "Stage 1 per-file hash key set",
    sorted(stage1_hashes),
    sorted(resolution["stage1_source_hashes"]),
)
check(
    "Stage 1 per-file hashes",
    stage1_hashes,
    resolution["stage1_source_hashes"],
)

# Exact Stage 4 producer provenance.
producer_files = {
    path.name
    for path in (ROOT / "generation-tools").iterdir()
    if path.is_file() and not path.is_symlink()
}
check(
    "producer bundle exact files",
    producer_files,
    {"klean.py", "klean_export.py", "source-manifest.json"},
)
check(
    "producer source manifest keys",
    set(source_manifest),
    {"schema_version", "generator_image_id", "files"},
)
check("producer source manifest schema", source_manifest["schema_version"], 1)
check(
    "klean_export.py producer hash",
    file_sha256(ROOT / "generation-tools/klean_export.py"),
    generator_manifest["exporter_sha256"],
)
check(
    "klean.py producer hash",
    file_sha256(ROOT / "generation-tools/klean.py"),
    generator_manifest["klean_py_sha256"],
)
check(
    "source-manifest producer hashes",
    source_manifest["files"],
    {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
)
check(
    "generator image id across manifests",
    source_manifest["generator_image_id"],
    generator_manifest["provenance"]["generator_image_id"],
)
check(
    "generator image id versus launcher producer path",
    source_manifest["generator_image_id"].removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)

# Canonical K rule inventory, including source spans and hashes.
inventory = inventory_verification(ROOT / "k-proof")
check("verification closure", inventory["verification_modules"], ["VERIFICATION"])
check(
    "verification.k hash",
    inventory["verification_sha256"],
    file_sha256(ROOT / "k-proof/verification.k"),
)
verification_lines = (ROOT / "k-proof/verification.k").read_text().splitlines()
for index, rule in enumerate(inventory["rules"]):
    source_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    check(f"rule {index} exact source span", source_text, rule["text"])
    normalized_hash = hashlib.sha256(
        " ".join(source_text.split()).encode()
    ).hexdigest()
    check(
        f"rule {index} normalized source hash",
        normalized_hash,
        rule["normalized_sha256"],
    )
    check(
        f"rule {index} source_rule_id",
        rule["source_rule_id"],
        f"rule-{normalized_hash}",
    )
check(
    "whole inventory hash",
    canonical_json_sha256(inventory["rules"]),
    inventory["inventory_sha256"],
)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check("Stage 3 rule count", len(discovery_ids), len(canonical_ids))
check("Stage 3 ordered identity bijection", discovery_ids, canonical_ids)
check("Stage 3 unique identities", len(set(discovery_ids)), len(discovery_ids))
check(
    "Stage 3 inventory hash",
    discovery["inventory_sha256"],
    inventory["inventory_sha256"],
)

# These are the audit's independent semantic classifications, entered only
# after inspecting the frozen declarations, source program, loop invariant,
# and the relevant fixed operational rules for iteration, concatenation, and
# list append.
independent_classifications = [
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
]
check(
    "independent classifications versus Stage 3",
    [rule["classification"] for rule in discovery["rules"]],
    independent_classifications,
)
check(
    "all simplification classifications allowed",
    [
        discovery["rules"][index]["classification"]
        for index, rule in enumerate(inventory["rules"])
        if "simplification" in rule["attributes"]
    ],
    [],
)
independent_domain_ids: list[str] = []

classified_inventory = [
    {
        **rule,
        "classification": discovery["rules"][index]["classification"],
        "rationale": discovery["rules"][index]["rationale"],
    }
    for index, rule in enumerate(inventory["rules"])
]
check(
    "Stage 4 copied definition records",
    input_manifest["definitions"],
    classified_inventory,
)
check("Stage 4 operational records", input_manifest["operational_rules"], [])
check(
    "Stage 4 proved-derived records",
    input_manifest["proved_derived_lemmas"],
    [],
)
check("Stage 4 domain source records", input_manifest["source_rules"], [])

# Generation manifests and the independent empty-set bijection.
discovery_hash = file_sha256(ROOT / "lemma-discovery.json")
frozen_digest = tree_digest(ROOT / "k-proof")
generated_digest = tree_digest(ROOT / "klean-generation/generated")
check(
    "input manifest frozen digest",
    input_manifest["frozen_input_sha256"],
    frozen_digest,
)
check(
    "input manifest Stage 1 digest",
    input_manifest["stage1_workspace_sha256"],
    frozen_digest,
)
check(
    "input manifest discovery hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
check(
    "input manifest verification hash",
    input_manifest["verification_sha256"],
    inventory["verification_sha256"],
)
check(
    "input manifest inventory hash",
    input_manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)
check("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)
check(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    frozen_digest,
)
check(
    "generator Stage 3 provenance",
    generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    discovery_hash,
)
check(
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "generator generated-tree hash",
    generator_manifest["generated_tree_sha256"],
    generated_digest,
)
check(
    "generator obligation-map hash",
    generator_manifest["obligation_map_sha256"],
    file_sha256(ROOT / "klean-generation/generated/obligation-map.json"),
)
check("independent domain set", independent_domain_ids, [])
check("obligation-map schema", obligation_map["schema_version"], 3)
check("obligation source rules", obligation_map["source_rules"], [])
check("obligation list", obligation_map["obligations"], [])
check("trust parameter list", obligation_map["trust_parameters"], [])
check("generator obligation count", generator_manifest["obligation_count"], 0)
check("export obligation count", export_result["obligation_count"], 0)
check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check(
    "export frozen digest",
    export_result["frozen_input_sha256"],
    frozen_digest,
)
check(
    "export discovery hash",
    export_result["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
check(
    "export generated-tree hash",
    export_result["generated_tree_sha256"],
    generated_digest,
)
check(
    "export trust-inventory hash",
    export_result["trust_inventory_sha256"],
    file_sha256(ROOT / "klean-generation/trust-inventory.json"),
)

# Fixed generated target: the empty obligation set must produce no target.
target_definitions: list[str] = []
for lean_file in sorted((ROOT / "klean-generation/generated").rglob("*.lean")):
    for match in re.finditer(
        r"(?m)^\s*def\s+targetStatement\b", lean_file.read_text()
    ):
        target_definitions.append(
            f"{lean_file.relative_to(ROOT / 'klean-generation/generated')}:{match.start()}"
        )
check("generated target declaration count", target_definitions, [])
check("generator target", generator_manifest["target"], None)
check("signed launcher target", resolution["target"], None)
check("signed Stage 4 preflight target", resolution["stage4_preflight"]["target"], None)
check("signed Stage 4 obligation count", resolution["stage4_preflight"]["obligation_count"], 0)
check("signed Stage 4 status", resolution["stage4_preflight"]["status"], "KLEAN_NO_OBLIGATIONS")
check(
    "selected Stage 4 status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)
check("Stage 5 result absent", resolution["stage5_result"], None)
check("Lean workspace absent", resolution["lean_workspace"], None)
check("Lean invocation absent", resolution["lean_invocation"], None)
check("candidate mount absent", Path("/candidate").exists(), False)

# The fresh preflight rerun must reproduce the signed structural result.
check(
    "fresh preflight exact result",
    rerun_preflight,
    resolution["stage4_preflight"],
)
check(
    "fresh preflight clean exit",
    rerun_preflight["diagnostics"][0]["exit_code"],
    0,
)
check(
    "fresh preflight build exit",
    rerun_preflight["diagnostics"][1]["exit_code"],
    0,
)
check(
    "fresh preflight trust declaration count",
    rerun_preflight["trust_declaration_count"],
    len(trust_inventory["allowlist"]),
)

print(
    json.dumps(
        {
            "status": "PASS",
            "check_count": len(checks),
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
