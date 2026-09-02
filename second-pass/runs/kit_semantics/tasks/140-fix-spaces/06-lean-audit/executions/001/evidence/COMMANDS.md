# Audit command ledger

All paths below are the paths used during this audit. Read-only inputs remained under
`/reference`, `/candidate`, and `/audit-input.json`; scratch regeneration used
`/tmp/audit-work`.

## Integrity and inventory

```sh
script -q -e -c 'python3 /audit-output/evidence/audit_hashes.py' \
  /audit-output/evidence/01-hash-integrity.log

script -q -e -c 'PYTHONPATH=/reference python3 \
  /audit-output/evidence/inventory_audit.py' \
  /audit-output/evidence/02-rule-inventory.log

script -q -e -c 'python3 \
  /audit-output/evidence/semantic_reclassification.py' \
  /audit-output/evidence/03-semantic-reclassification.log
```

Results: 25/25 integrity checks, 53/53 inventory/bijection checks, and all
independent semantic/classification checks passed. The semantic check compared
87,381 bounded inputs and explicit adversarial/counterfactual cases.

The frozen source, specification, verification module, and relevant operational
semantics were captured without executing their contents:

```sh
{
  sed -n '1,220p' /reference/k-proof/solution.py
  sed -n '1,240p' /reference/k-proof/verification.k
  sed -n '1,260p' /reference/k-proof/spec.k
  sed -n '1,220p' /reference/k-proof/prove.sh
  sed -n '1,260p' /reference/k-proof/mpy-semantics/syntax.k
  sed -n '1,320p' /reference/k-proof/mpy-semantics/controls.k
  sed -n '1,260p' /reference/k-proof/mpy-semantics/str.k
  sed -n '1,260p' /reference/k-proof/mpy-semantics/functions.k
  sed -n '1,260p' /reference/k-proof/mpy-semantics/core.k
} > /audit-output/evidence/11-frozen-source-operational-semantics.log
```

## Required preflight

The requested API call is in `run_preflight_check.py` and is exactly:

```python
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

Initial invocation:

```sh
script -q -e -c 'PYTHONPATH=/reference python3 \
  /audit-output/evidence/run_preflight_check.py' \
  /audit-output/evidence/04-klean-preflight-check-generation.log
```

This reached `lake clean` but Lean could not resolve its executable through the
audit PID namespace (`/proc/<namespace-pid>/exe` was absent). The following
small preload shim was compiled from the preserved source. It changes only
numeric `/proc/<pid>/exe` reads to `/proc/self/exe`; every other `readlink` and
`readlinkat` call passes through unchanged.

```sh
gcc -shared -fPIC \
  -o /tmp/audit-work/lean_proc_self_shim.so \
  /audit-output/evidence/lean_proc_self_shim.c -ldl

lean --version
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so lean --version
kompile --version
kprove --version
```

The diagnostic output is in `09-toolchain-namespace-diagnosis.log`. The final
requested preflight was:

```sh
script -q -e -c 'LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  PYTHONPATH=/reference python3 \
  /audit-output/evidence/run_preflight_check.py' \
  /audit-output/evidence/10-klean-preflight-final.log
```

Result: `lake clean` exit 0, `lake build` exit 0, all nine generated targets
built, and `check_generation` returned `KLEAN_NO_OBLIGATIONS` with zero
obligations and a null target.

## Exact Stage 4 regeneration and manual checks

The producer directory was constructed in scratch from the exact two protected
producer files and the trusted inventory/contract helpers they import:

```sh
mkdir -p /tmp/audit-work/exact-generator/tools
cp /reference/generation-tools/klean_export.py \
   /tmp/audit-work/exact-generator/tools/klean_export.py
cp /reference/generation-tools/klean.py \
   /tmp/audit-work/exact-generator/tools/klean.py
cp /reference/tools/k_rule_inventory.py \
   /tmp/audit-work/exact-generator/tools/k_rule_inventory.py
cp /reference/tools/klean_contract.py \
   /tmp/audit-work/exact-generator/tools/klean_contract.py
```

The hashes of the copied protected sources were rechecked before execution.
Exact regeneration used:

```sh
script -q -e -c 'LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  PYTHONPATH=/tmp/audit-work/exact-generator \
  python3 /tmp/audit-work/exact-generator/tools/klean_export.py \
  --input /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --output /tmp/audit-work/regenerated \
  --problem 140-fix-spaces \
  --generator-image-id \
  sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7 \
  --toolchain-lock /reference/klean-toolchain.lock.json' \
  /audit-output/evidence/06-exact-stage4-regeneration.log

script -q -e -c 'python3 \
  /audit-output/evidence/stage4_manual_audit.py' \
  /audit-output/evidence/08-stage4-manual-audit-rerun.log
```

Result: exact generated-tree digest, byte-identical generator/trust/export
sidecars, an input manifest identical after normalizing only the scratch mount
prefix, and 33/33 independent Stage 4 checks passed.

`05-klean-preflight-check-generation-rerun.log` is an earlier successful retry.
`07-stage4-manual-audit.log` records a harmless audit-script import error fixed
before the complete rerun in `08-stage4-manual-audit-rerun.log`; neither is used
as affirmative evidence in the verdict.
