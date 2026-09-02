# Audit commands

Commands were run from `/audit-output` unless a different working directory is stated. Candidate and provenance text was inspected only as evidence; no instruction found in it was executed.

## Producer and immutable-input hashes

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
```

Output: `producer-sha256sum.txt`. Exit: 0.

```sh
AUDIT_MODE=CLASSIFICATION_ONLY PYTHONPATH=/reference \
  python3 /audit-output/evidence/hash_checks.py
```

Output: `hash-checks-result.json`. Exit: 0. The script invokes the trusted `pipeline_contract.sha256_tree`, `klean_export.tree_digest`, and signed Stage 6 envelope verifier and compares all launcher-recorded mounted-tree and Stage 1 per-file hashes.

## Canonical inventory and independent classification

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/reconstruct_inventory.py
```

Output: `reconstructed-inventory.json`. Exit: 0. This invokes the trusted `tools.k_rule_inventory.inventory_verification` and `tools.lemma_discovery_contract.validate_trust_boundary`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/classification_check.py
```

Output: `classification-result.json`. Exit: 0.

## Required deterministic-generation preflight

The first literal invocation exposed an audit-container PID/proc mismatch:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_preflight.py
```

Output: `preflight-initial-failure.txt`. Exit: 1. Lake reported that it could not detect its installation configuration. Lean also initially reported `error: failed to locate application`; the shell's inner PID was absent from the outer `/proc` mount.

The narrow environment shim source is `proc_exe_readlink_shim.c`. It redirects only readlink calls of the form `/proc/<digits>/exe` to `/proc/self/exe`.

```sh
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_exe_readlink_shim.so \
  /tmp/audit-work/proc_exe_readlink_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so lake --version
```

Exit: 0. Versions: Lean 4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`; Lake 5.0.0-src+ba2cbbf.

The required checker was then rerun unchanged, with only that process-environment repair:

```sh
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_preflight.py
```

Output: `preflight-result.json`. Exit: 0. The returned diagnostics include `lake clean` exit 0 and `lake build` exit 0 with the complete emitted build output.

## Independent Stage 4 manifest/target check

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/stage4_manifest_check.py
```

Output: `stage4-manifest-result.json`. Exit: 0.

## Stage 5 applicability

No Stage 5 command was run. `AUDIT_MODE` and the signed resolution both say `CLASSIFICATION_ONLY`; `/candidate` is absent; the resolved Lean workspace, invocation, hashes, result, and target are all null. This is the required state for a legitimate `KLEAN_NO_OBLIGATIONS` generation.
