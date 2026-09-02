#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def canonical_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def generator_binding_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"PASS: {label}")


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)
inventory = inventory_verification(Path("/reference/k-proof"))

require(
    canonical_hash(resolution) == audit["resolved_input_sha256"],
    "resolved audit input canonical hash",
)

recorded_tree_hashes = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
}
for key, observed in recorded_tree_hashes.items():
    require(observed == resolution["hashes"][key], f"recorded {key}")

require(
    tree_digest(Path("/reference/k-proof"))
    == resolution["hashes"]["stage1_export_sha256"],
    "recorded Stage 1 export digest",
)
require(
    tree_digest(Path("/reference/klean-generation/generated"))
    == resolution["hashes"]["generated_tree_sha256"],
    "recorded generated-tree digest",
)
require(
    file_hash(Path("/reference/lemma-discovery.json"))
    == resolution["hashes"]["discovery_manifest_sha256"],
    "recorded discovery-manifest file hash",
)

stage1_hashes = resolution["stage1_source_hashes"]
require(
    all(
        file_hash(Path("/reference/k-proof") / relative) == expected
        for relative, expected in stage1_hashes.items()
    ),
    f"all {len(stage1_hashes)} recorded Stage 1 per-file hashes",
)

producer_actual = {
    name: file_hash(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
require(
    producer_actual == source_manifest["files"],
    "producer files match source manifest",
)
require(
    producer_actual["klean_export.py"] == generator["exporter_sha256"]
    and producer_actual["klean.py"] == generator["klean_py_sha256"],
    "producer files match generator manifest",
)
image_id = source_manifest["generator_image_id"]
require(
    image_id == generator["provenance"]["generator_image_id"],
    "producer image ID matches generator manifest",
)
require(
    resolution["generation_producer_sources"].rstrip("/").endswith(
        image_id.removeprefix("sha256:")
    ),
    "producer image ID matches launcher-recorded immutable source path",
)

canonical_rules = inventory["rules"]
classified = discovery["rules"]
require(
    inventory["inventory_sha256"] == discovery["inventory_sha256"],
    "whole rule-inventory hash",
)
require(
    [entry["source_rule_id"] for entry in classified]
    == [rule["source_rule_id"] for rule in canonical_rules],
    "Stage 3 rule identities are ordered bijectively",
)
require(
    len({entry["source_rule_id"] for entry in classified})
    == len(classified)
    == len(canonical_rules),
    "Stage 3 has no omitted, duplicate, or extra identities",
)
for rule in canonical_rules:
    require(
        rule["source_rule_id"]
        == f"rule-{rule['normalized_sha256']}",
        f"source_rule_id derives from normalized hash at "
        f"{rule['start_line']}-{rule['end_line']}",
    )

domain_ids = [
    entry["source_rule_id"]
    for entry in classified
    if entry["classification"] == "DOMAIN_LEMMA"
]
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
require(
    domain_ids
    == [entry["source_rule_id"] for entry in input_manifest["source_rules"]]
    == [entry["source_rule_id"] for entry in source_rules]
    == [entry["source_rule_id"] for entry in obligations],
    "domain-rule/source-rule/obligation ordered bijection",
)
require(
    len(domain_ids) == len(set(domain_ids)) == len(obligations) == 2,
    "exactly two unique, nonempty obligations",
)
for source_rule, obligation in zip(source_rules, obligations, strict=True):
    require(
        obligation["source_span"]
        == {
            "start_line": source_rule["start_line"],
            "end_line": source_rule["end_line"],
        },
        f"obligation span for {source_rule['source_rule_id']}",
    )
    require(
        obligation["normalized_sha256"]
        == source_rule["normalized_sha256"],
        f"obligation normalized hash for {source_rule['source_rule_id']}",
    )
    require(
        text_hash(obligation["lean_conjunct"])
        == obligation["lean_conjunct_sha256"],
        f"obligation conjunct hash for {source_rule['source_rule_id']}",
    )
    require(
        obligation["lean_conjunct"].strip()
        not in {"True", "False", "true", "false"},
        f"obligation is not a literal vacuous conjunct for "
        f"{source_rule['source_rule_id']}",
    )

parameters = obligation_map["trust_parameters"]
for parameter in parameters:
    binding = {
        key: parameter[key]
        for key in ("kore_symbol", "name", "type", "source_rule_ids")
    }
    require(
        generator_binding_hash(binding) == parameter["binding_sha256"],
        f"target binding hash for {parameter['name']}",
    )
    require(
        set(parameter["source_rule_ids"]).issubset(domain_ids),
        f"target binding source IDs for {parameter['name']}",
    )

expected_lines = ["def targetStatement"]
for parameter in parameters:
    expected_lines.append(
        f"    ({parameter['name']} : {parameter['type']})"
    )
expected_lines.extend(
    (
        "    : Prop :=",
        "    "
        + "\n    ∧ ".join(
            f"({obligation['lean_conjunct']})"
            for obligation in obligations
        ),
    )
)
expected_definition = "\n".join(expected_lines)
lean_text = Path(
    "/reference/klean-generation/generated/"
    "Klean76IsSimplePower/Lemmas.lean"
).read_text()
match = re.search(
    r"(?ms)^\s*def\s+targetStatement\b.*?"
    r"(?=^\s*end\s+\S+\s*$)",
    lean_text,
)
require(match is not None, "generated target declaration exists")
actual_definition = match.group(0).strip()
require(
    actual_definition == expected_definition,
    "generated target is the exact conjunction of obligations",
)
target = generator["target"]
require(
    text_hash(actual_definition) == target["definition_sha256"],
    "generated target definition hash",
)
statement = " ".join(
    (target["declaration"], *(parameter["name"] for parameter in parameters))
)
require(statement == target["statement"], "generated target application")
require(
    text_hash(statement) == target["statement_sha256"],
    "generated target statement hash",
)
require(
    target == resolution["target"]
    == resolution["stage4_preflight"]["target"],
    "target identity agrees across generator manifest and audit input",
)
require(
    tree_digest(Path("/tmp/audit-work/lean-proof-audit/Base"))
    == generator["generated_tree_sha256"],
    "fresh proof Base equals immutable generated tree",
)

proof_text = Path("/tmp/audit-work/lean-proof-audit/Proof.lean").read_text()
require(
    re.search(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", proof_text)
    is None,
    "candidate Proof.lean has no forbidden trust token",
)
require(
    len(re.findall(r"(?m)^\s*(?:def|theorem)\s+targetStatement\b", proof_text))
    == 0,
    "candidate does not shadow targetStatement",
)
require(
    len(re.findall(r"(?m)^\s*theorem\s+final\b", proof_text)) == 1,
    "candidate has exactly one Proof.final theorem",
)
