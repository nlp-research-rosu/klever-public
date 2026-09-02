#!/usr/bin/env python3
"""Independent hash and zero-obligation consistency checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError(f"unsafe tree root: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def pipeline_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
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
    for relative, kind, path in tree_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def canonical_json_sha256(document: object) -> str:
    encoded = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def load(path: Path) -> dict:
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise RuntimeError(f"not a JSON object: {path}")
    return document


def main() -> None:
    audit_input = load(Path("/audit-input.json"))
    resolution = audit_input["resolution"]
    hashes = resolution["hashes"]
    input_manifest = load(Path("/reference/klean-generation/input-manifest.json"))
    generator_manifest = load(
        Path("/reference/klean-generation/generator-manifest.json")
    )
    export_result = load(Path("/reference/klean-generation/export-result.json"))
    obligation_map = load(
        Path("/reference/klean-generation/generated/obligation-map.json")
    )

    observed = {
        "resolved_input_sha256": canonical_json_sha256(resolution),
        "k_workspace_sha256": pipeline_tree_digest(Path("/reference/k-proof")),
        "stage1_export_sha256": export_tree_digest(Path("/reference/k-proof")),
        "k_audit_sha256": pipeline_tree_digest(Path("/reference/k-audit")),
        "klean_generation_sha256": pipeline_tree_digest(
            Path("/reference/klean-generation")
        ),
        "discovery_manifest_sha256": sha256_file(
            Path("/reference/lemma-discovery.json")
        ),
        "generated_tree_sha256": export_tree_digest(
            Path("/reference/klean-generation/generated")
        ),
        "verification_sha256": sha256_file(
            Path("/reference/k-proof/verification.k")
        ),
        "obligation_map_sha256": sha256_file(
            Path("/reference/klean-generation/generated/obligation-map.json")
        ),
        "trust_inventory_sha256": sha256_file(
            Path("/reference/klean-generation/trust-inventory.json")
        ),
        "exporter_sha256": sha256_file(Path("/reference/tools/klean_export.py")),
        "klean_py_sha256": sha256_file(Path("/reference/tools/klean.py")),
    }

    expected = {
        "resolved_input_sha256": audit_input["resolved_input_sha256"],
        "k_workspace_sha256": hashes["k_workspace_sha256"],
        "stage1_export_sha256": hashes["stage1_export_sha256"],
        "k_audit_sha256": hashes["k_audit_sha256"],
        "klean_generation_sha256": hashes["klean_generation_sha256"],
        "discovery_manifest_sha256": hashes["discovery_manifest_sha256"],
        "generated_tree_sha256": hashes["generated_tree_sha256"],
        "verification_sha256": input_manifest["verification_sha256"],
        "obligation_map_sha256": generator_manifest["obligation_map_sha256"],
        "trust_inventory_sha256": export_result["trust_inventory_sha256"],
        "exporter_sha256": generator_manifest["exporter_sha256"],
        "klean_py_sha256": generator_manifest["klean_py_sha256"],
    }

    source_files = {
        relative
        for relative, kind, _path in tree_entries(Path("/reference/k-proof"))
        if kind == "file"
    }
    source_hashes = resolution["stage1_source_hashes"]
    source_hash_observed = {
        relative: sha256_file(Path("/reference/k-proof") / relative)
        for relative in sorted(source_files)
    }

    verification_lines = Path("/reference/k-proof/verification.k").read_text().splitlines()
    rule_text = "\n".join(verification_lines[8:10])
    normalized = " ".join(rule_text.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    manual_rule = {
        "source_rule_id": f"rule-{normalized_sha256}",
        "module": "VERIFICATION",
        "start_line": 9,
        "end_line": 10,
        "normalized_sha256": normalized_sha256,
        "attributes": [],
        "text": rule_text,
    }
    manual_inventory_sha256 = canonical_json_sha256([manual_rule])
    discovery = load(Path("/reference/lemma-discovery.json"))
    discovered_rules = discovery["rules"]

    lean_sources = [
        path
        for relative, kind, path in tree_entries(
            Path("/reference/klean-generation/generated")
        )
        if kind == "file" and relative.endswith(".lean")
    ]
    target_occurrences = sum(
        source.read_text().count("targetStatement") for source in lean_sources
    )

    checks = {
        key: observed[key] == expected[key] for key in sorted(expected)
    }
    checks.update(
        {
            "stage1_source_file_set_exact": set(source_hashes) == source_files,
            "stage1_source_hashes_exact": source_hashes == source_hash_observed,
            "manual_rule_normalized_sha256": (
                normalized_sha256
                == "08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1"
            ),
            "manual_source_rule_id": (
                manual_rule["source_rule_id"]
                == "rule-08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1"
            ),
            "manual_inventory_sha256": (
                manual_inventory_sha256 == discovery["inventory_sha256"]
            ),
            "discovery_exact_single_identity": (
                len(discovered_rules) == 1
                and discovered_rules[0]["source_rule_id"]
                == manual_rule["source_rule_id"]
            ),
            "input_manifest_source_rules_empty": (
                input_manifest["source_rules"] == []
            ),
            "obligation_map_source_rules_empty": (
                obligation_map["source_rules"] == []
            ),
            "obligation_map_obligations_empty": (
                obligation_map["obligations"] == []
            ),
            "obligation_map_parameters_empty": (
                obligation_map["trust_parameters"] == []
            ),
            "generator_obligation_count_zero": (
                generator_manifest["obligation_count"] == 0
            ),
            "generator_target_null": generator_manifest["target"] is None,
            "audit_target_null": resolution["target"] is None,
            "target_declaration_absent": target_occurrences == 0,
            "candidate_absent": not Path("/candidate").exists(),
        }
    )

    result = {
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "observed": observed,
        "expected": expected,
        "manual_rule": manual_rule,
        "manual_inventory_sha256": manual_inventory_sha256,
        "source_hashes_observed": source_hash_observed,
        "target_occurrences": target_occurrences,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
