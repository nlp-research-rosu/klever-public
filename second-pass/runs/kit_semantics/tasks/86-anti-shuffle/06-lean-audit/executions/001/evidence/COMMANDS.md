# Material audit commands

The corresponding complete outputs are the numbered evidence files named
below.  Mounted inputs were read only; generated scratch material was confined
to `/tmp/audit-work` and `/audit-output/evidence`.

## Launcher and mounted-input inspection

```sh
printf "AUDIT_MODE=%s\n" "$AUDIT_MODE"
sed -n '1,260p' /audit-input.json
rg --files /reference/tools | sort
find /reference -mindepth 1 -maxdepth 2 -printf '%y %p\n' | sort
find /candidate -mindepth 1 -maxdepth 3 -printf '%y %p\n' | sort
```

Output: `00_environment.txt`.

## Producer authentication

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.klean_export import tree_digest; print(tree_digest(Path("/reference/generation-tools")))'
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

The JSON comparison in `04_producer_authentication.txt` additionally compared
both file hashes and the image ID against `source-manifest.json`,
`generator-manifest.json`, and `/audit-input.json`.  Outputs:
`04_producer_authentication.txt`, `10_recorded_tree_hashes.txt`, and
`38_hash_and_structure_verification.txt`.

## Canonical inventory reconstruction and bijection

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
```

Output: `09_reconstructed_inventory.txt`.

## Launcher, source, sidecar, and tree-hash verification

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/verify_hashes_and_structure.py
```

Output: `38_hash_and_structure_verification.txt`.

## Supplied-semantics singleton comparison claims

```sh
kprove --version
kprove lemma-spec.k --definition lemma-kompiled --spec-module LEMMA-SPEC
```

Working directory: `/reference/k-proof`. Output:
`39_bridge_free_strlt_claims.txt`.

## Required trusted preflight

Initial command (failed only when Lean could not resolve `/proc/<pid>/exe` in
the audit PID namespace):

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Output: `11_rerun_klean_preflight.txt`.

The namespace mismatch was confirmed with:

```sh
python3 -c 'import os; p=os.getpid(); print(p); print(os.readlink(f"/proc/{p}/exe"))'
cat /proc/self/status
```

Outputs: `44_proc_pid_exe_test.txt` and `45_proc_namespace_identity.txt`.
The compatibility shim source and wrapper are preserved as
`/tmp/audit-work/host_pid_shim.c` and `/tmp/audit-work/shim-bin/lake`; their
build and smoke-test output is `46_proc_compatibility_shim.txt`.  The successful
preflight command was:

```sh
PATH=/tmp/audit-work/shim-bin:$PATH PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Output: `47_rerun_klean_preflight_success.txt`.

## Generated target and candidate absence

```sh
find /reference/klean-generation/generated -maxdepth 3 -type f -printf '%p\n' | sort
nl -ba /reference/klean-generation/generated/Klean86AntiShuffle/Lemmas.lean
rg -n 'Target|target|Proof\.final|theorem final|def final|opaque final|axiom final' \
  /reference/klean-generation/generated
python3 -m json.tool \
  /reference/klean-generation/generated/obligation-map.json
test -e /candidate
```

Outputs: `48_generated_target_absence.txt` and
`49_recorded_target_identity.txt`.
