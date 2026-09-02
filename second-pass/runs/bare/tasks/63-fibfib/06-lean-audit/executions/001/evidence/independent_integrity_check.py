#!/usr/bin/env python3
"""Independent hash, provenance, obligation, and target-integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return sha256_bytes(encoded)


def regular_tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    assert root.is_dir() and not root.is_symlink(), root
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
                raise AssertionError(f"unsupported tree entry: {path}")
    return sorted(entries)


def pipeline_tree_digest(root: Path) -> str:
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
    digest = hashlib.sha256()
    for relative, kind, path in regular_tree_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


checks: list[tuple[str, Any, Any]] = []


def check(label: str, observed: Any, expected: Any) -> None:
    checks.append((label, observed, expected))


audit = json.loads(AUDIT_INPUT.read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
discovery = json.loads(DISCOVERY.read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
trust_inventory = GENERATION / "trust-inventory.json"
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

check(
    "signed resolution canonical hash",
    canonical_json_sha256(resolution),
    audit["resolved_input_sha256"],
)
check(
    "Stage 1 pipeline tree",
    pipeline_tree_digest(K_PROOF),
    hashes["k_workspace_sha256"],
)
check(
    "Stage 1 export tree",
    export_tree_digest(K_PROOF),
    hashes["stage1_export_sha256"],
)
check(
    "Stage 2 selected audit tree",
    pipeline_tree_digest(K_AUDIT),
    hashes["k_audit_sha256"],
)
check(
    "Stage 4 selected generation tree",
    pipeline_tree_digest(GENERATION),
    hashes["klean_generation_sha256"],
)
check(
    "producer-source bundle tree",
    pipeline_tree_digest(PRODUCERS),
    hashes["generation_producer_sources_sha256"],
)
check(
    "generated project export tree",
    export_tree_digest(GENERATED),
    hashes["generated_tree_sha256"],
)
check(
    "Stage 3 manifest file",
    sha256_file(DISCOVERY),
    hashes["discovery_manifest_sha256"],
)

for relative, expected in sorted(resolution["stage1_source_hashes"].items()):
    check(f"Stage 1 source {relative}", sha256_file(K_PROOF / relative), expected)

producer_file_hashes = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean.py", "klean_export.py")
}
for name, observed in producer_file_hashes.items():
    check(f"producer {name} vs source manifest", observed, source_manifest["files"][name])
check(
    "producer klean.py vs generator manifest",
    producer_file_hashes["klean.py"],
    generator_manifest["klean_py_sha256"],
)
check(
    "producer klean_export.py vs generator manifest",
    producer_file_hashes["klean_export.py"],
    generator_manifest["exporter_sha256"],
)

image_from_audit_path = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)
check(
    "generator image: source vs generator manifest",
    source_manifest["generator_image_id"],
    generator_manifest["provenance"]["generator_image_id"],
)
check(
    "generator image: audit input path vs generator manifest",
    image_from_audit_path,
    generator_manifest["provenance"]["generator_image_id"],
)

check(
    "generator toolchain lock",
    generator_manifest["toolchain"],
    toolchain_lock,
)
check(
    "verification.k direct hash",
    sha256_file(K_PROOF / "verification.k"),
    input_manifest["verification_sha256"],
)
check(
    "Stage 1 export hash in input manifest",
    export_tree_digest(K_PROOF),
    input_manifest["stage1_workspace_sha256"],
)
check(
    "Stage 1 frozen hash in input manifest",
    export_tree_digest(K_PROOF),
    input_manifest["frozen_input_sha256"],
)
check(
    "Stage 3 hash in input manifest",
    sha256_file(DISCOVERY),
    input_manifest["stage3_discovery_manifest_sha256"],
)
check(
    "inventory hash: discovery vs input manifest",
    discovery["inventory_sha256"],
    input_manifest["inventory_sha256"],
)
check(
    "inventory hash: discovery vs generator provenance",
    discovery["inventory_sha256"],
    generator_manifest["provenance"]["inventory_sha256"],
)
check(
    "obligation-map direct hash",
    sha256_file(obligation_map_path),
    generator_manifest["obligation_map_sha256"],
)
check(
    "trust-inventory direct hash",
    sha256_file(trust_inventory),
    export_result["trust_inventory_sha256"],
)

generated_hash = export_tree_digest(GENERATED)
for label, document in (
    ("generator manifest", generator_manifest),
    ("export result", export_result),
    ("saved preflight", preflight),
    ("audit-input preflight", resolution["stage4_preflight"]),
):
    check(f"generated tree in {label}", generated_hash, document["generated_tree_sha256"])
for label, document in (
    ("generator provenance", generator_manifest["provenance"]),
    ("export result", export_result),
    ("saved preflight", preflight),
    ("audit-input preflight", resolution["stage4_preflight"]),
):
    check(
        f"Stage 3 hash in {label}",
        sha256_file(DISCOVERY),
        document["stage3_discovery_manifest_sha256"],
    )

expected_domain_rule_ids: list[str] = []
classified_domain_rule_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
input_source_rule_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_source_rule_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]
check(
    "independent domain set vs Stage 3 domain set",
    classified_domain_rule_ids,
    expected_domain_rule_ids,
)
check(
    "independent domain set vs Stage 4 input source rules",
    input_source_rule_ids,
    expected_domain_rule_ids,
)
check(
    "independent domain set vs obligation-map source rules",
    mapped_source_rule_ids,
    expected_domain_rule_ids,
)
check(
    "independent domain set vs generated obligations",
    obligation_source_rule_ids,
    expected_domain_rule_ids,
)
check(
    "obligation IDs are unique",
    len(obligation_source_rule_ids),
    len(set(obligation_source_rule_ids)),
)
check(
    "obligation count in generator manifest",
    len(obligation_source_rule_ids),
    generator_manifest["obligation_count"],
)
check(
    "obligation count in export result",
    len(obligation_source_rule_ids),
    export_result["obligation_count"],
)
check(
    "obligation count in saved preflight",
    len(obligation_source_rule_ids),
    preflight["obligation_count"],
)
check("trust parameters", obligation_map["trust_parameters"], [])

target_declarations: list[str] = []
for path in sorted(GENERATED.rglob("*.lean")):
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", path.read_text()):
        target_declarations.append(
            f"{path.relative_to(GENERATED).as_posix()}:{match.start()}"
        )
check("generated target declaration count", target_declarations, [])
check("generator manifest target", generator_manifest["target"], None)
check("saved preflight target", preflight["target"], None)
check("audit-input target", resolution["target"], None)
check("Stage 5 result", resolution["stage5_result"], None)
check("Lean workspace hash", hashes["lean_workspace_sha256"], None)
check("Lean invocation hash", hashes["lean_invocation_sha256"], None)
check("candidate absent", Path("/candidate").exists(), False)
check("AUDIT_MODE agreement", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("selected Stage 4 status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
check("saved preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
check("audit-input preflight status", resolution["stage4_preflight"]["status"], "KLEAN_NO_OBLIGATIONS")
check(
    "selected Stage 2 artifact hash",
    pipeline_tree_digest(K_AUDIT),
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
check(
    "selected Stage 4 artifact hash",
    pipeline_tree_digest(GENERATION),
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)

failures = 0
for label, observed, expected in checks:
    status = "PASS" if observed == expected else "FAIL"
    print(f"{status}: {label}")
    print(f"  observed: {observed!r}")
    print(f"  expected: {expected!r}")
    failures += status == "FAIL"

print(f"\nTOTAL CHECKS: {len(checks)}")
print(f"FAILURES: {failures}")
if failures:
    raise SystemExit(1)
