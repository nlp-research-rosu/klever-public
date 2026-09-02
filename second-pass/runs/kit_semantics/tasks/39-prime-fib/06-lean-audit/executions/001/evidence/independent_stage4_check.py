import hashlib
import json
import os
import re
import stat
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


def hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def hash_text(value: str) -> str:
    return hash_bytes(value.encode())


def tree_digest(root: Path) -> str:
    entries = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError((relative, "unsafe tree entry"))
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


root = Path("/reference/klean-generation")
generated = root / "generated"
input_manifest = json.loads((root / "input-manifest.json").read_text())
generator_manifest = json.loads((root / "generator-manifest.json").read_text())
export_result = json.loads((root / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
discovery_path = Path("/reference/lemma-discovery.json")
discovery = json.loads(discovery_path.read_text())
inventory = inventory_verification(Path("/reference/k-proof"))
audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]

print("HASHES")
hash_checks = {
    "stage1_tree": (
        tree_digest(Path("/reference/k-proof")),
        input_manifest["stage1_workspace_sha256"],
    ),
    "discovery_file": (
        hash_bytes(discovery_path.read_bytes()),
        input_manifest["stage3_discovery_manifest_sha256"],
    ),
    "generated_tree": (
        tree_digest(generated),
        generator_manifest["generated_tree_sha256"],
    ),
    "obligation_map_file": (
        hash_bytes((generated / "obligation-map.json").read_bytes()),
        generator_manifest["obligation_map_sha256"],
    ),
    "trust_inventory_file": (
        hash_bytes((root / "trust-inventory.json").read_bytes()),
        export_result["trust_inventory_sha256"],
    ),
}
for label, (observed, expected) in hash_checks.items():
    print(label, observed, expected, "match", observed == expected)
print(
    "audit generated hash match",
    hash_checks["generated_tree"][0]
    == audit_input["hashes"]["generated_tree_sha256"],
)
print(
    "audit discovery hash match",
    hash_checks["discovery_file"][0]
    == audit_input["hashes"]["discovery_manifest_sha256"],
)
print(
    "inventory hash match",
    inventory["inventory_sha256"]
    == discovery["inventory_sha256"]
    == input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
)
print(
    "verification file hash match",
    hash_bytes(Path("/reference/k-proof/verification.k").read_bytes())
    == input_manifest["verification_sha256"]
    == inventory["verification_sha256"],
)
print(
    "producer file hashes",
    hash_bytes(Path("/reference/generation-tools/klean_export.py").read_bytes())
    == generator_manifest["exporter_sha256"],
    hash_bytes(Path("/reference/generation-tools/klean.py").read_bytes())
    == generator_manifest["klean_py_sha256"],
)

print("SOURCE/OBLIGATION BIJECTION")
by_id = {rule["source_rule_id"]: rule for rule in inventory["rules"]}
class_by_id = {
    rule["source_rule_id"]: rule for rule in discovery["rules"]
}
domain_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
input_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    rule["source_rule_id"] for rule in obligation_map["obligations"]
]
print("domain ids", domain_ids)
print("input ids", input_ids)
print("map source ids", map_source_ids)
print("obligation ids", obligation_ids)
print(
    "exact ordered bijection",
    domain_ids == input_ids == map_source_ids == obligation_ids
    and len(obligation_ids) == len(set(obligation_ids)),
)
for index, (source, obligation) in enumerate(
    zip(obligation_map["source_rules"], obligation_map["obligations"]), 1
):
    rule_id = source["source_rule_id"]
    raw_rule = by_id[rule_id]
    classification = class_by_id[rule_id]
    print(
        "obligation",
        index,
        "id",
        rule_id,
        "span match",
        obligation["source_span"]
        == {
            "start_line": raw_rule["start_line"],
            "end_line": raw_rule["end_line"],
        },
        "normalized hash match",
        obligation["normalized_sha256"] == raw_rule["normalized_sha256"],
        "classification",
        classification["classification"],
        "conjunct hash match",
        hash_text(obligation["lean_conjunct"])
        == obligation["lean_conjunct_sha256"],
    )
print(
    "obligation counts",
    len(domain_ids),
    len(obligation_ids),
    generator_manifest["obligation_count"],
    export_result["obligation_count"],
)

print("TARGET")
parameters = obligation_map["trust_parameters"]
for parameter in parameters:
    binding = {
        key: parameter[key]
        for key in ("kore_symbol", "name", "type", "source_rule_ids")
    }
    observed = hash_text(
        json.dumps(binding, sort_keys=True, separators=(",", ":"))
    )
    print(
        "binding",
        parameter["name"],
        observed,
        parameter["binding_sha256"],
        "match",
        observed == parameter["binding_sha256"],
        "all rules domain",
        set(parameter["source_rule_ids"]) <= set(domain_ids),
    )
expected_lines = ["def targetStatement"]
expected_lines.extend(
    f"    ({parameter['name']} : {parameter['type']})"
    for parameter in parameters
)
expected_lines.extend(
    [
        "    : Prop :=",
        "    "
        + "\n    ∧ ".join(
            f"({obligation['lean_conjunct']})"
            for obligation in obligation_map["obligations"]
        ),
    ]
)
expected_definition = "\n".join(expected_lines)
lemmas = (generated / generator_manifest["target"]["file"]).read_text()
match = re.search(
    r"(?ms)^def targetStatement\b.*?(?=^end\s+\S+\s*$)", lemmas
)
assert match is not None
actual_definition = match.group(0).strip()
statement = " ".join(
    [generator_manifest["target"]["declaration"]]
    + [parameter["name"] for parameter in parameters]
)
print(
    "actual equals generated-from-map exact",
    actual_definition == expected_definition,
)
print(
    "actual definition hash",
    hash_text(actual_definition),
    generator_manifest["target"]["definition_sha256"],
    "match",
    hash_text(actual_definition)
    == generator_manifest["target"]["definition_sha256"],
)
print(
    "statement exact",
    statement == generator_manifest["target"]["statement"],
)
print(
    "statement hash",
    hash_text(statement),
    generator_manifest["target"]["statement_sha256"],
    "match",
    hash_text(statement) == generator_manifest["target"]["statement_sha256"],
)
print(
    "exactly one target declaration",
    sum(
        len(
            re.findall(
                r"(?m)^\s*def\s+targetStatement\b", path.read_text()
            )
        )
        for path in generated.rglob("*.lean")
    ),
)
print(
    "target manifest equals recorded preflight target",
    generator_manifest["target"]
    == json.loads((root / "preflight.json").read_text())["target"],
)
print("CONJUNCTS")
for obligation in obligation_map["obligations"]:
    print(obligation["source_rule_id"], obligation["lean_conjunct"])
