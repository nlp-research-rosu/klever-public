#!/usr/bin/env bash
set -eu

printf '%s\n' '$ build and probe narrow PID-namespace compatibility shim'
cc -shared -fPIC -ldl \
  /audit-output/evidence/proc_exe_compat.c \
  -o /tmp/audit-work/proc_exe_compat.so
printf 'namespace_pid=%s\n' "$$"
if readlink "/proc/$$/exe"; then
  printf '%s\n' 'unexpected: numeric PID executable path exists'
else
  printf '%s\n' 'numeric PID executable path is absent as expected'
fi
readlink /proc/self/exe
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lean --version
export LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so

printf '%s\n' '$ PYTHONPATH=/reference python3 - (tools.klean_preflight.check_generation with complete build output)'
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation

def logged_run(command, *, cwd, timeout):
    print(
        "BEGIN PREFLIGHT COMMAND "
        + json.dumps({"command": command, "cwd": str(cwd), "timeout": timeout}),
        flush=True,
    )
    result = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout, end="", flush=True)
    print(
        "END PREFLIGHT COMMAND "
        + json.dumps({"command": command, "exit_code": result.returncode}),
        flush=True,
    )
    return result.returncode, result.stdout

returned = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
recorded = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
print("BEGIN RETURNED PREFLIGHT EVIDENCE")
print(json.dumps(returned, indent=2, sort_keys=True))
print("END RETURNED PREFLIGHT EVIDENCE")
print("returned_preflight_equals_recorded=" + str(returned == recorded).lower())
returned_core = {key: value for key, value in returned.items() if key != "diagnostics"}
recorded_core = {key: value for key, value in recorded.items() if key != "diagnostics"}
returned_command_results = [
    (item["command"], item["exit_code"]) for item in returned["diagnostics"]
]
recorded_command_results = [
    (item["command"], item["exit_code"]) for item in recorded["diagnostics"]
]
print(
    "returned_preflight_core_equals_recorded="
    + str(returned_core == recorded_core).lower()
)
print(
    "returned_command_results_equal_recorded="
    + str(returned_command_results == recorded_command_results).lower()
)
if (
    returned_core != recorded_core
    or returned_command_results != recorded_command_results
):
    raise SystemExit(1)
PY

printf '%s\n' '$ PYTHONPATH=/reference python3 - (independent Stage 4 hash, source/obligation, and target audit)'
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import verify_audit_input

stage1 = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(audit_document)
discovery = json.loads(discovery_path.read_text())
inventory = inventory_verification(stage1)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory = json.loads(
    (generation / "trust-inventory.json").read_text()
)
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

file_sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
stage1_hash = tree_digest(stage1)
stage1_pipeline_hash = sha256_tree(stage1)
discovery_hash = file_sha(discovery_path)
generated_hash = tree_digest(generated)
generation_hash = sha256_tree(generation)
k_audit_hash = sha256_tree(Path("/reference/k-audit"))
obligation_map_hash = file_sha(obligation_map_path)
trust_inventory_hash = file_sha(generation / "trust-inventory.json")

classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
ordered_inventory_ids = [
    entry["source_rule_id"] for entry in inventory["rules"]
]
independently_confirmed_domain_ids = []
manifest_domain_ids = [
    source_rule_id
    for source_rule_id in ordered_inventory_ids
    if classification_by_id[source_rule_id] == "DOMAIN_LEMMA"
]
source_rule_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
lean_sources = sorted(generated.rglob("*.lean"))
lean_text = "\n".join(path.read_text() for path in lean_sources)
target = target_statement(generated)

checks = {
    "signed_resolution_digest_valid": resolved_digest
    == audit_document["resolved_input_sha256"],
    "stage1_tree_all_bindings": stage1_hash
    == resolution["hashes"]["stage1_export_sha256"]
    == input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == generator_manifest["provenance"]["stage1_workspace_sha256"]
    == export_result["frozen_input_sha256"]
    == preflight["frozen_input_sha256"]
    == preflight["stage1_workspace_sha256"],
    "stage1_pipeline_tree_audit_binding": stage1_pipeline_hash
    == resolution["hashes"]["k_workspace_sha256"],
    "discovery_hash_all_bindings": discovery_hash
    == resolution["hashes"]["discovery_manifest_sha256"]
    == input_manifest["stage3_discovery_manifest_sha256"]
    == generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == export_result["stage3_discovery_manifest_sha256"]
    == preflight["stage3_discovery_manifest_sha256"],
    "inventory_hash_all_bindings": inventory["inventory_sha256"]
    == discovery["inventory_sha256"]
    == input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
    "verification_hash_binding": inventory["verification_sha256"]
    == input_manifest["verification_sha256"],
    "generated_tree_all_bindings": generated_hash
    == resolution["hashes"]["generated_tree_sha256"]
    == generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"]
    == preflight["generated_tree_sha256"],
    "generation_tree_audit_binding": generation_hash
    == resolution["hashes"]["klean_generation_sha256"],
    "selected_generation_artifact_binding": generation_hash
    == resolution["selections"]["klean_generation"]["artifact_sha256"],
    "selected_k_audit_artifact_binding": k_audit_hash
    == resolution["hashes"]["k_audit_sha256"]
    == resolution["selections"]["k_audit"]["artifact_sha256"],
    "obligation_map_hash_binding": obligation_map_hash
    == generator_manifest["obligation_map_sha256"],
    "trust_inventory_hash_binding": trust_inventory_hash
    == export_result["trust_inventory_sha256"],
    "toolchain_lock_exact": generator_manifest["toolchain"]
    == toolchain_lock,
    "independent_domain_set_empty": independently_confirmed_domain_ids == [],
    "stage3_domain_set_empty": manifest_domain_ids == [],
    "source_rule_set_empty": obligation_map["source_rules"] == [],
    "obligation_set_empty": obligation_map["obligations"] == [],
    "source_obligation_ordered_bijection": source_rule_ids
    == obligation_ids
    == independently_confirmed_domain_ids,
    "no_duplicate_source_rule_ids": len(source_rule_ids)
    == len(set(source_rule_ids)),
    "no_duplicate_obligation_ids": len(obligation_ids)
    == len(set(obligation_ids)),
    "no_vacuous_conjuncts": all(
        isinstance(item.get("lean_conjunct"), str)
        and item["lean_conjunct"].strip()
        and item["lean_conjunct"].strip() not in {"True", "(True)"}
        for item in obligation_map["obligations"]
    ),
    "obligation_counts_zero": generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == preflight["obligation_count"]
    == resolution["stage4_preflight"]["obligation_count"]
    == 0,
    "statuses_no_obligations": generator_manifest["target"] is None
    and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    and resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "fixed_target_absent_everywhere": target is None
    and generator_manifest["target"] is None
    and preflight["target"] is None
    and resolution["target"] is None
    and resolution["stage4_preflight"]["target"] is None,
    "no_generated_target_module": not (generated / "Klean49Modp/Target.lean").exists(),
    "no_target_declaration_text": re.search(
        r"(?m)^\\s*(?:def|theorem|lemma)\\s+target\\b", lean_text
    )
    is None,
    "no_stage5_paths_or_result": resolution["mode"] == "CLASSIFICATION_ONLY"
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None
    and resolution["hashes"]["lean_workspace_sha256"] is None
    and resolution["hashes"]["lean_invocation_sha256"] is None,
    "no_candidate_mount": not Path("/candidate").exists(),
    "trust_counts_structurally_recorded": len(trust_inventory["allowlist"])
    == preflight["trust_declaration_count"]
    == resolution["stage4_preflight"]["trust_declaration_count"],
    "recorded_preflight_exact_audit_binding": preflight
    == resolution["stage4_preflight"],
}

print(
    json.dumps(
        {
            "digests": {
                "resolved_input_sha256": resolved_digest,
                "stage1_tree_sha256": stage1_hash,
                "stage1_pipeline_tree_sha256": stage1_pipeline_hash,
                "discovery_sha256": discovery_hash,
                "inventory_sha256": inventory["inventory_sha256"],
                "verification_sha256": inventory["verification_sha256"],
                "generated_tree_sha256": generated_hash,
                "generation_tree_sha256": generation_hash,
                "k_audit_tree_sha256": k_audit_hash,
                "obligation_map_sha256": obligation_map_hash,
                "trust_inventory_sha256": trust_inventory_hash,
            },
            "independently_confirmed_domain_ids": independently_confirmed_domain_ids,
            "manifest_domain_ids": manifest_domain_ids,
            "source_rule_ids": source_rule_ids,
            "obligation_ids": obligation_ids,
            "target_statement": target,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
PY

printf '%s\n' '$ find generated project and candidate mount state'
find /reference/klean-generation/generated -type f -printf '%P\n' | sort
if [ -e /candidate ]; then
  find /candidate -maxdepth 3 -printf '%y %P\n' | sort
else
  printf '%s\n' '/candidate ABSENT'
fi
