#!/usr/bin/env python3
"""Independent launcher-envelope and Stage 4 producer-integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-output/audit-input.json")
GENERATION = Path("/reference/klean-generation")
PRODUCERS = Path("/reference/generation-tools")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, condition: bool) -> None:
    print(f"CHECK {label}: {'PASS' if condition else 'FAIL'}")
    if not condition:
        raise SystemExit(1)


envelope = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    envelope
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)

print(f"resolved_input_sha256={resolved_digest}")
print(f"AUDIT_MODE={os.environ.get('AUDIT_MODE')}")
for key in ("run_id", "problem_id", "condition", "mode", "semantics_mode"):
    print(f"resolution.{key}={resolution[key]}")
print(f"resolution.target={resolution['target']!r}")
print(f"resolution.lean_workspace={resolution['lean_workspace']!r}")
print(f"resolution.lean_invocation={resolution['lean_invocation']!r}")
print(
    "resolution.selection.status="
    f"{resolution['selections']['klean_generation']['status']}"
)

check("environment mode matches signed resolution", os.environ.get("AUDIT_MODE") == resolution["mode"])
check("problem identity", resolution["problem_id"] == "67-fruit-distribution")
check("condition identity", resolution["condition"] == "kit-semantics")
check("semantics mode", resolution["semantics_mode"] == "SUPPLIED_SEMANTICS")
check("classification-only has no signed target", resolution["target"] is None)
check("classification-only has no Stage 5 paths", resolution["lean_workspace"] is None and resolution["lean_invocation"] is None)
check("candidate mount absent", not Path("/candidate").exists())

entries = sorted(
    (path.relative_to(PRODUCERS).as_posix(), stat.S_IFMT(path.lstat().st_mode))
    for path in PRODUCERS.iterdir()
)
print(f"producer_entries={entries!r}")
check(
    "producer bundle exact file set",
    [name for name, _kind in entries]
    == ["klean.py", "klean_export.py", "source-manifest.json"]
    and all(kind == stat.S_IFREG for _name, kind in entries),
)

observed_exporter = sha256(PRODUCERS / "klean_export.py")
observed_klean = sha256(PRODUCERS / "klean.py")
observed_bundle = pipeline_contract.sha256_tree(PRODUCERS)
expected_image = generator_manifest["provenance"]["generator_image_id"]
audit_bundle_basename = Path(resolution["generation_producer_sources"]).name

print(f"observed.klean_export.py.sha256={observed_exporter}")
print(f"observed.klean.py.sha256={observed_klean}")
print(f"observed.producer_bundle.sha256={observed_bundle}")
print(f"generator_manifest.exporter_sha256={generator_manifest['exporter_sha256']}")
print(f"generator_manifest.klean_py_sha256={generator_manifest['klean_py_sha256']}")
print(f"generator_manifest.generator_image_id={expected_image}")
print(f"source_manifest={json.dumps(source_manifest, sort_keys=True)}")
print(
    "audit_input.generation_producer_sources_sha256="
    f"{resolution['hashes']['generation_producer_sources_sha256']}"
)
print(f"audit_input.producer_bundle_basename={audit_bundle_basename}")

check(
    "klean_export.py hash matches generator manifest",
    observed_exporter == generator_manifest["exporter_sha256"],
)
check(
    "klean.py hash matches generator manifest",
    observed_klean == generator_manifest["klean_py_sha256"],
)
check(
    "source manifest hashes match observed producers",
    source_manifest.get("files")
    == {"klean_export.py": observed_exporter, "klean.py": observed_klean},
)
check(
    "source manifest image matches generator manifest",
    source_manifest.get("generator_image_id") == expected_image,
)
check(
    "audit-input producer path binds generator image",
    expected_image == f"sha256:{audit_bundle_basename}",
)
check(
    "audit-input producer tree hash",
    observed_bundle
    == resolution["hashes"]["generation_producer_sources_sha256"],
)

print("RESULT: PASS")
