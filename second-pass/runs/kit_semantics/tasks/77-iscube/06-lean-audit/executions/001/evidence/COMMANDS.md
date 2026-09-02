# Audit commands and result files

All mounted inputs were read-only. Scratch K definitions and the Lean runtime
compatibility library were created only below `/tmp/audit-work`.

## Producer and provenance hashes

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

Result: exit 0; `producer_hash_gate.log`.

```bash
PYTHONPATH=/reference python3 evidence/hash_verification.py
```

Result: exit 0; `hash_verification.log`. Every launcher resolution hash,
selection hash, sidecar binding, and all 814 Stage 1 per-file hashes match.

## Rule inventory and structural bijection

```bash
PYTHONPATH=/reference python3 evidence/structural_bijection.py
PYTHONPATH=/reference python3 evidence/proof_local_closure_inventory.py
PYTHONPATH=/reference python3 evidence/connection_transition_check.py
sed -n '16,44p' /reference/k-proof/prove.sh
```

Results: exit 0; `structural_bijection.log`,
`proof_local_closure_inventory.log`, and
`connection_transition_and_order.log`.

The first script invokes the trusted canonical inventory and Stage 3 contract.
The second applies the same trusted lexical span/hash routines across the
cross-file proof-local import closure that operational K actually loads.

## Required Stage 4 preflight

Initial exact invocation:

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r, indent=2, sort_keys=True))'
```

Result: exit 1 before project compilation because Lake could not detect its
installation; `preflight_initial_environment_failure.log`.

The namespace diagnosis and exact compatibility source are in
`lean_environment_diagnosis.txt` and `proc_self_exe_shim.c`. The shim changes
only `readlink("/proc/<digits>/exe")` to `readlink("/proc/self/exe")`, working
around this sandbox's PID/proc mismatch.

```bash
cc -shared -fPIC -ldl \
  -o /tmp/audit-work/proc_self_exe_shim.so \
  evidence/proc_self_exe_shim.c
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r, indent=2, sort_keys=True))'
```

Result: exit 0, `KLEAN_NO_OBLIGATIONS`; `preflight_success.log`. Its clean and
build output hashes exactly equal the launcher-recorded preflight hashes.

## Fresh bridge-free K check

Scratch setup copied only `verification-base.k`, `connection-spec.k`, and the
supplied `reference-semantics` tree to `/tmp/audit-work/k-fresh`.

```bash
kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-base-review-kompiled
kprove connection-spec.k \
  --definition verification-base-review-kompiled \
  --spec-module CONNECTION
```

Results: both exit 0 and the proof prints `#Top`;
`kompile_bridge_free_base.log` and `kprove_bridge_free_connection.log`.

## Domain-lemma removal checks

The exact deletions are in `domain_lemma_removals.diff`. Each variant was
freshly compiled before proving the unchanged connection claim.

```bash
# Exit equality lemma removed
kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-base-no-exit-review-kompiled
kprove connection-spec.k \
  --definition verification-base-no-exit-review-kompiled \
  --spec-module CONNECTION

# Scope-map deletion lemma removed
kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-base-no-map-review-kompiled
kprove connection-spec.k \
  --definition verification-base-no-map-review-kompiled \
  --spec-module CONNECTION
```

Both compiles exit 0. Both proofs exit 1 with `WarnStuckClaimState` at the
respective missing equality: `kprove_without_exit_domain_lemma.log` and
`kprove_without_map_domain_lemma.log`. Compile outputs are in the correspondingly
named `kompile_without_*` logs.
