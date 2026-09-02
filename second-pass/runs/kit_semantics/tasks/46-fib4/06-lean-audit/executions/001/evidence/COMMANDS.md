# Audit command ledger

All commands ran from `/audit-output`. The referenced Python programs are
preserved beside this ledger and contain the complete comparison logic.

## Mounted inputs and audit mode

```sh
printf 'AUDIT_MODE=%s\n' "${AUDIT_MODE-<unset>}"
find /reference/k-proof -maxdepth 2 -type f -printf '%P\n' | sort
find /reference/k-audit -maxdepth 3 -type f -printf '%P\n' | sort
find /reference/klean-generation -maxdepth 4 -type f -printf '%P\n' | sort
find /reference/generation-tools -maxdepth 2 -type f -printf '%P\n' | sort
test -e /candidate && find /candidate -maxdepth 3 -printf '%P %y\n' | sort || echo ABSENT
```

Result: [00-mounted-files.txt](/audit-output/evidence/00-mounted-files.txt).

## Producer and provenance authentication

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/trust-inventory.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k
PYTHONPATH=/reference python3 /audit-output/evidence/verify_hashes.py
```

Results: [01-critical-file-hashes.txt](/audit-output/evidence/01-critical-file-hashes.txt),
[03-hash-and-producer-authentication.txt](/audit-output/evidence/03-hash-and-producer-authentication.txt),
and [17-final-immutability-rehash.txt](/audit-output/evidence/17-final-immutability-rehash.txt).

## Frozen source and operational semantics

```sh
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/spec-body-mutation.k
nl -ba /reference/k-proof/spec-vacuity.k
nl -ba /reference/k-proof/prove.sh
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k
rg -n 'applyBin.*\+|applyCmp.*<|_\+Int_|_<Int_' /reference/k-proof/reference-semantics/semantics/*.k
```

Results: [02-frozen-source-and-spec.txt](/audit-output/evidence/02-frozen-source-and-spec.txt)
and [16-relevant-operational-semantics.txt](/audit-output/evidence/16-relevant-operational-semantics.txt).

## Stage 3 inventory and semantic checks

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
python3 /audit-output/evidence/stage3_semantic_checks.py
```

Results: [04-inventory-reconstruction.txt](/audit-output/evidence/04-inventory-reconstruction.txt)
and [15-stage3-semantic-counterfactuals.txt](/audit-output/evidence/15-stage3-semantic-counterfactuals.txt).

## Trusted Stage 4 preflight

The audit sandbox's PID namespace is not reflected in its `/proc` mount. Lean
therefore initially failed to resolve `/proc/<namespace-pid>/exe`. The narrow
shim below retries only a missing numeric process-executable lookup through
`/proc/self/exe`.

```sh
gcc -shared -fPIC -ldl -o /tmp/proc_exe_compat.so \
  /audit-output/evidence/proc_exe_compat.c
LD_PRELOAD=/tmp/proc_exe_compat.so lean --version
LD_PRELOAD=/tmp/proc_exe_compat.so lake --version
PYTHONPATH=/reference LD_PRELOAD=/tmp/proc_exe_compat.so \
  python3 /audit-output/evidence/run_preflight_check.py
```

The final command calls `tools.klean_preflight.check_generation` directly with
`/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and `/reference/klean-toolchain.lock.json`.
Results: [08-proc-exe-shim-validation.txt](/audit-output/evidence/08-proc-exe-shim-validation.txt)
and [12-check-generation-success.txt](/audit-output/evidence/12-check-generation-success.txt).
The pre-shim and pseudo-terminal failures are retained in
[05-rerun-check-generation.txt](/audit-output/evidence/05-rerun-check-generation.txt),
[09-rerun-check-generation-with-shim.txt](/audit-output/evidence/09-rerun-check-generation-with-shim.txt),
and [11-rerun-check-generation-final.txt](/audit-output/evidence/11-rerun-check-generation-final.txt).

## Independent Stage 4 bijection and target scan

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/audit_stage4.py
find /reference/klean-generation/generated -type f -name '*.lean' -printf '%P\n' | sort
rg -n 'theorem|lemma|Proof\.final|KleanTarget|target' \
  /reference/klean-generation/generated --glob '*.lean'
rg -n '\b(axiom|opaque|sorry|admit|unsafe)\b' \
  /reference/klean-generation/generated --glob '*.lean'
rg -n 'fib4Spec' /reference/klean-generation/generated --glob '*.lean'
```

Results: [13-generated-target-and-source-scan.txt](/audit-output/evidence/13-generated-target-and-source-scan.txt)
and [14-stage4-bijection-and-target.txt](/audit-output/evidence/14-stage4-bijection-and-target.txt).
