# Audit command ledger

All paths are the immutable mounts named by the launcher unless they are below
`/audit-output` or `/tmp/audit-work`.

## Mode and immutable inputs

```sh
printenv AUDIT_MODE
sed -n '1,260p' /audit-input.json
rg --files /reference/k-proof /reference/k-audit \
  /reference/klean-generation /reference/generation-tools \
  /reference/tools | sort
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
```

Results: `00-audit-mode.txt`, `01-audit-input.json`,
`02-mounted-files.txt`, and `03-generation-producer-hashes.txt`.

## Canonical Stage 3 inventory

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'

PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; x=validate_trust_boundary(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json")); print(json.dumps({"inventory_sha256":x["inventory_sha256"],"ordered_source_rule_ids":[r["source_rule_id"] for r in x["rules"]],"definitions":[r["source_rule_id"] for r in x["definitions"]],"operational_rules":[r["source_rule_id"] for r in x["operational_rules"]],"proved_derived_lemmas":[r["source_rule_id"] for r in x["proved_derived_lemmas"]],"domain_lemmas":[r["source_rule_id"] for r in x["domain_lemmas"]]},indent=2))'
```

Results: `07-reconstructed-rule-inventory.json` and
`12-trust-boundary-validation.json`. The frozen sources inspected for the
independent semantic judgment are in `09-frozen-stage1-sources.txt`; the
independently parsed Python AST is in `75-source-solution-ast.txt`.

## Hash and manifest cross-check

```sh
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools"))); print(sha256_tree(Path("/reference/k-proof"))); print(sha256_tree(Path("/reference/klean-generation")))'

PYTHONPATH=/reference python3 /audit-output/evidence/70-structural-cross-check.py
```

Results: `63-recomputed-contract-tree-digests.txt` and
`78-structural-cross-check-final.json`. The cross-check source is preserved as
`70-structural-cross-check.py`.

## Trusted Stage 4 preflight rerun

The first exact call exposed the audit sandbox's PID/proc mismatch:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; x=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(x,indent=2,sort_keys=True))'
```

Lean reported `failed to locate application` because the sandbox reported PID
`3` to the process but `/proc/3` did not exist. Evidence:
`79-preflight-without-proc-shim-failure.txt`,
`24-manual-lake-clean.txt`, `45-proc-pid-exe.txt`,
`46-proc-numeric-exe-ls.txt`, and `47-pid-namespace-observation.txt`.

The narrow `readlink` shim preserved at `proc_self_exe_shim.c` changes only
lookups shaped as `/proc/<pid>/exe` to `/proc/self/exe`. It was built and
validated with:

```sh
gcc -shared -fPIC -Wall -Wextra -Werror \
  /tmp/audit-work/proc_self_exe_shim.c -ldl \
  -o /tmp/audit-work/proc_self_exe_shim.so
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so lean --version
```

Results: `56-build-proc-self-shim.txt` and
`57-lean-version-with-proc-shim.txt`.

The successful required rerun was:

```sh
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; x=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(x,indent=2,sort_keys=True))'
```

The complete returned evidence is
`59-rerun-check-generation-final.json`.
