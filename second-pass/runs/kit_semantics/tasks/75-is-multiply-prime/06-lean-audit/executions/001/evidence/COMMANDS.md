# Audit command record

All commands were run from `/audit-output`. The numbered `.txt` files in this
directory are the raw combined stdout/stderr results.

## Producer authentication

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
```

Results: `00_environment_and_producer_auth.txt` and
`01_manifest_contents.txt`.

## Canonical Stage 3 inventory

```bash
export PYTHONPATH=/reference
python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), sort_keys=True, indent=2))'
python3 -c 'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), sort_keys=True, indent=2))'
```

Result: `03_inventory_reconstruction.txt`.

## Trusted Stage 4 preflight

The direct default invocation was attempted first and is preserved in
`04_check_generation.txt`. It failed because this runner's numeric procfs PID
namespace makes Lean 4.22's `/proc/<getpid()>/exe` lookup return `ENOENT`.
`19_procfs_compatibility_evidence.txt` records the failing lookup.

The compatibility library only retries a failed `/proc/*/exe` `readlink` as
`/proc/self/exe`. Its complete source is `proc_exe_compat.c`. It was built and
the public `run_command` callback of `check_generation` was used to select the
pinned Lake binary:

```bash
cc -shared -fPIC -O2 \
  -o /tmp/audit-work/proc_exe_compat.so \
  /audit-output/evidence/proc_exe_compat.c -ldl
export PYTHONPATH=/reference
python3 /audit-output/evidence/run_check_generation.py
```

Inside `check_generation`, the callback ran these exact commands in its fresh
temporary project copy, with the pinned toolchain environment and the procfs
compatibility library:

```bash
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake clean
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake build
```

Complete successful result: `13_check_generation_completed.txt`.

## Recorded hash reconciliation

```bash
export PYTHONPATH=/reference
python3 /audit-output/evidence/verify_recorded_hashes.py
```

Result: `14_recorded_hash_reconciliation.txt`.

## Obligation bijection and target

```bash
export PYTHONPATH=/reference
sha256sum /reference/klean-generation/generated/obligation-map.json
python3 -c 'import json; from pathlib import Path; from tools import klean_export; g=Path("/reference/klean-generation/generated"); m=json.loads((g/"obligation-map.json").read_text()); print("expected_target_definition=", repr(klean_export.expected_target_definition(m))); print("observed_target_statement=", repr(klean_export.target_statement(g))); print("source_rule_ids=", [r.get("source_rule_id") for r in m["source_rules"]]); print("obligation_ids=", [o.get("source_rule_id") for o in m["obligations"]]); print("trust_parameters=", m["trust_parameters"])'
```

Results: `15_obligation_target_and_candidate.txt` and
`17_exact_bijection_and_target.txt`.

## Independent program/postcondition check

```bash
python3 /audit-output/evidence/check_frozen_program_math.py
```

Result: `18_frozen_program_math.txt`.
