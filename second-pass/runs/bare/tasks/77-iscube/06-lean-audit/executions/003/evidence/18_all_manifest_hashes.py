import hashlib
import json
from pathlib import Path

from tools import klean_export


def load(path: str):
    return json.loads(Path(path).read_text())


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load("/audit-input.json")
resolution = audit["resolution"]
generator = load("/reference/klean-generation/generator-manifest.json")
export_result = load("/reference/klean-generation/export-result.json")
recorded_preflight = load("/reference/klean-generation/preflight.json")
replayed_preflight = load(
    "/audit-output/evidence/06_check_generation_returned.json"
)
lock = load("/reference/klean-toolchain.lock.json")

stage1_observed = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}
stage1_recorded = resolution["stage1_source_hashes"]

sidecars = {
    "obligation-map.json": file_sha(
        Path(
            "/reference/klean-generation/generated/obligation-map.json"
        )
    ),
    "trust-inventory.json": file_sha(
        Path("/reference/klean-generation/trust-inventory.json")
    ),
}

report = {
    "stage1_source_hashes": {
        "recorded": stage1_recorded,
        "observed": stage1_observed,
        "exact_map_match": stage1_recorded == stage1_observed,
    },
    "stage4_sidecars": {
        "observed": sidecars,
        "generator_obligation_map_sha256": generator[
            "obligation_map_sha256"
        ],
        "export_result_trust_inventory_sha256": export_result[
            "trust_inventory_sha256"
        ],
        "obligation_map_matches": (
            sidecars["obligation-map.json"]
            == generator["obligation_map_sha256"]
        ),
        "trust_inventory_matches": (
            sidecars["trust-inventory.json"]
            == export_result["trust_inventory_sha256"]
        ),
    },
    "toolchain_lock_exact": generator["toolchain"] == lock,
    "generated_tree_matches_generator_and_audit": (
        klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        )
        == generator["generated_tree_sha256"]
        == resolution["hashes"]["generated_tree_sha256"]
    ),
    "selected_preflight_equals_launcher_copy": (
        recorded_preflight == resolution["stage4_preflight"]
    ),
    "replayed_preflight_equals_selected": (
        replayed_preflight == recorded_preflight
    ),
    "stage5_workspace_hash_consistent": (
        resolution["stage5_result"]["outputs"]["workspace_sha256"]
        == resolution["hashes"]["lean_workspace_sha256"]
    ),
    "unmounted_recorded_artifacts": {
        "lean_invocation_sha256": resolution["hashes"][
            "lean_invocation_sha256"
        ],
        "note": (
            "No Lean invocation tree is mounted; the signed audit envelope "
            "was validated, but this one tree hash cannot be recomputed from "
            "the supplied filesystem inputs."
        ),
    },
}

print(json.dumps(report, indent=2, sort_keys=True))
