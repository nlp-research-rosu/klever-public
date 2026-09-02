#!/usr/bin/env python3
"""Independent hash and provenance reconciliation for the 159-eat audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
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
                raise AssertionError(f"linked or unsupported entry: {path}")
    return sorted(entries)


def pipeline_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in regular_entries(root):
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
    for relative, kind, path in regular_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def check_equal(label: str, observed: object, expected: object) -> None:
    state = "MATCH" if observed == expected else "MISMATCH"
    print(f"{label}: {state}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if observed != expected:
        raise AssertionError(label)


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    recorded = resolution["hashes"]
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    preflight = json.loads((GENERATION / "preflight.json").read_text())

    check_equal("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
    check_equal("problem", resolution["problem_id"], "159-eat")
    check_equal("condition", resolution["condition"], "kit-semantics")
    check_equal("semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
    check_equal("Stage 5 result", resolution["stage5_result"], None)
    check_equal("Lean workspace hash", recorded["lean_workspace_sha256"], None)
    check_equal("Lean invocation hash", recorded["lean_invocation_sha256"], None)
    check_equal("candidate absent", Path("/candidate").exists(), False)

    pipeline_checks = {
        "Stage 1 full workspace": (K_PROOF, recorded["k_workspace_sha256"]),
        "Stage 2 selected audit": (K_AUDIT, recorded["k_audit_sha256"]),
        "Stage 4 selected generation": (
            GENERATION,
            recorded["klean_generation_sha256"],
        ),
        "Stage 4 producer bundle": (
            PRODUCERS,
            recorded["generation_producer_sources_sha256"],
        ),
    }
    for label, (path, expected) in pipeline_checks.items():
        check_equal(label + " pipeline tree SHA-256", pipeline_tree_digest(path), expected)

    check_equal(
        "Stage 1 export tree SHA-256",
        export_tree_digest(K_PROOF),
        recorded["stage1_export_sha256"],
    )
    check_equal(
        "generated project tree SHA-256",
        export_tree_digest(GENERATED),
        recorded["generated_tree_sha256"],
    )
    check_equal(
        "generated tree vs generator manifest",
        export_tree_digest(GENERATED),
        generator["generated_tree_sha256"],
    )
    check_equal(
        "discovery manifest SHA-256",
        sha256_bytes(DISCOVERY.read_bytes()),
        recorded["discovery_manifest_sha256"],
    )
    stage1_export_hash = export_tree_digest(K_PROOF)
    discovery_hash = sha256_bytes(DISCOVERY.read_bytes())
    verification_hash = sha256_bytes((K_PROOF / "verification.k").read_bytes())
    inventory_hash = json.loads(DISCOVERY.read_text())["inventory_sha256"]
    for label, observed in {
        "input frozen_input_sha256": input_manifest["frozen_input_sha256"],
        "input stage1_workspace_sha256": input_manifest["stage1_workspace_sha256"],
        "generator provenance stage1_workspace_sha256": generator["provenance"]["stage1_workspace_sha256"],
        "export frozen_input_sha256": export_result["frozen_input_sha256"],
        "preflight frozen_input_sha256": preflight["frozen_input_sha256"],
        "preflight stage1_workspace_sha256": preflight["stage1_workspace_sha256"],
    }.items():
        check_equal(label, observed, stage1_export_hash)
    for label, observed in {
        "input discovery SHA-256": input_manifest["stage3_discovery_manifest_sha256"],
        "generator provenance discovery SHA-256": generator["provenance"]["stage3_discovery_manifest_sha256"],
        "export discovery SHA-256": export_result["stage3_discovery_manifest_sha256"],
        "preflight discovery SHA-256": preflight["stage3_discovery_manifest_sha256"],
    }.items():
        check_equal(label, observed, discovery_hash)
    check_equal("input verification SHA-256", input_manifest["verification_sha256"], verification_hash)
    check_equal("input inventory SHA-256", input_manifest["inventory_sha256"], inventory_hash)
    check_equal(
        "generator provenance inventory SHA-256",
        generator["provenance"]["inventory_sha256"],
        inventory_hash,
    )
    for diagnostic in preflight["diagnostics"]:
        check_equal(
            "recorded diagnostic output SHA-256 for " + " ".join(diagnostic["command"]),
            sha256_bytes(diagnostic["output_tail"].encode()),
            diagnostic["output_sha256"],
        )

    actual_source_hashes = {
        relative: sha256_bytes(path.read_bytes())
        for relative, kind, path in regular_entries(K_PROOF)
        if kind == "file"
    }
    expected_source_hashes = resolution["stage1_source_hashes"]
    print(f"Stage 1 per-file hashes: expected_count={len(expected_source_hashes)} actual_count={len(actual_source_hashes)}")
    missing = sorted(set(expected_source_hashes) - set(actual_source_hashes))
    extra = sorted(set(actual_source_hashes) - set(expected_source_hashes))
    changed = sorted(
        name
        for name in set(expected_source_hashes) & set(actual_source_hashes)
        if expected_source_hashes[name] != actual_source_hashes[name]
    )
    print(f"  missing={missing}")
    print(f"  extra={extra}")
    print(f"  changed={changed}")
    if missing or extra or changed:
        raise AssertionError("Stage 1 per-file hashes")

    producer_names = {
        relative
        for relative, kind, _path in regular_entries(PRODUCERS)
        if kind == "file"
    }
    check_equal(
        "producer source exact file set",
        producer_names,
        {"klean_export.py", "klean.py", "source-manifest.json"},
    )
    producer_hashes = {
        name: sha256_bytes((PRODUCERS / name).read_bytes())
        for name in ("klean_export.py", "klean.py")
    }
    check_equal("producer file hashes vs source manifest", producer_hashes, source_manifest["files"])
    check_equal(
        "producer exporter hash vs generator manifest",
        producer_hashes["klean_export.py"],
        generator["exporter_sha256"],
    )
    check_equal(
        "producer klean.py hash vs generator manifest",
        producer_hashes["klean.py"],
        generator["klean_py_sha256"],
    )
    image_id = generator["provenance"]["generator_image_id"]
    check_equal("generator image vs source manifest", image_id, source_manifest["generator_image_id"])
    check_equal(
        "generator image vs audit-input producer path key",
        image_id.removeprefix("sha256:"),
        Path(resolution["generation_producer_sources"]).name,
    )

    check_equal("audit target vs generator target", resolution["target"], generator["target"])
    check_equal("generator target absent", generator["target"], None)
    assert resolution["stage4_preflight"] == preflight
    check_equal(
        "audit preflight vs mounted preflight canonical SHA-256",
        sha256_bytes(json.dumps(resolution["stage4_preflight"], sort_keys=True, separators=(",", ":")).encode()),
        sha256_bytes(json.dumps(preflight, sort_keys=True, separators=(",", ":")).encode()),
    )
    check_equal("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
    check_equal("generator obligation count", generator["obligation_count"], 0)
    check_equal("preflight obligation count", preflight["obligation_count"], 0)
    check_equal("export obligation count", export_result["obligation_count"], 0)
    check_equal(
        "trust inventory SHA-256",
        sha256_bytes((GENERATION / "trust-inventory.json").read_bytes()),
        export_result["trust_inventory_sha256"],
    )
    check_equal(
        "obligation map SHA-256",
        sha256_bytes((GENERATED / "obligation-map.json").read_bytes()),
        generator["obligation_map_sha256"],
    )
    print("INTEGRITY_RESULT: PASS")


if __name__ == "__main__":
    main()
