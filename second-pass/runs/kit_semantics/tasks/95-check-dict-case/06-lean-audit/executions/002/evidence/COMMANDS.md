# Command index

All mounted inputs were treated as read-only evidence. Commands which invoke Lean use a
narrow `readlink(2)` compatibility preload because this container exposes
`/proc/self/exe` but not Lean's numeric `/proc/<pid>/exe` lookup. The diagnosed failure,
shim source behavior, and successful pinned toolchain gate are recorded in evidence
10--28. `LEAN_SYSROOT` and `LAKE_HOME` point to the immutable locked Lean 4.22.0
toolchain.

## Producer provenance and inventories

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 -c \
  'from tools.k_rule_inventory import inventory_verification; import json; print(json.dumps(inventory_verification("/reference/k-proof"), indent=2, sort_keys=True))'
```

The producer comparison results are in `01-producer-provenance.txt` and
`02-producer-provenance-summary.txt`. The trusted reconstructed inventory is in
`05-reconstructed-inventory.json.txt`; the protected entries and bijection comparison
are in `06-protected-classification.txt` and `07-inventory-bijection.txt`.

## Frozen generation preflight

```sh
export LD_PRELOAD=/tmp/audit-work/proc_self_exe_fix.so
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
PYTHONPATH=/reference python3 - <<'PY'
import json
from tools.klean_preflight import check_generation
print(json.dumps(check_generation(
    '/reference/k-proof',
    '/reference/lemma-discovery.json',
    '/reference/klean-generation'), indent=2, sort_keys=True))
PY
```

The full returned evidence is `29-preflight-rerun-success.txt`. Independent tree,
resolved-source, target, and obligation-map hash recomputations are in evidence
32--37.

## Exact predecessor K proof

```sh
cd /reference/k-proof
kprove connection-spec.k --definition connection-kompiled \
  --spec-module CONNECTION-SPEC --claims CONNECTION-SPEC.isinstance
```

Complete output: `53-derived-lemma-kprove.txt` (`#Top`, exit 0).

## Fresh Lean proof build

The generated project was copied to the fresh directory
`/tmp/audit-work/lean-proof-audit.Y1Auq5/Base`, and candidate proof sources were copied
alongside it. The copy inventory and before-build hashes are in
`44-fresh-project-assembly.txt`.

```sh
cd /tmp/audit-work/lean-proof-audit.Y1Auq5
export LD_PRELOAD=/tmp/audit-work/proc_self_exe_fix.so
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
lake clean
lake build
lake env lean AuditAxioms.lean
```

Complete command outputs are `45-fresh-lake-clean.txt`, `46-fresh-lake-build.txt`, and
`48-print-axioms-proof-final-success.txt`.

## Trusted final mechanical gate

```sh
export LD_PRELOAD=/tmp/audit-work/proc_self_exe_fix.so
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
PYTHONPATH=/reference python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation --candidate /candidate
```

Complete JSON result: `52-trusted-stage5-mechanical-check.txt` (`status: PASS`).

## Operational bridge adversarial checks

`AuditOperational.lean` was an audit-only file in the fresh temporary project. It was
not copied into `Base` or the candidate.

```sh
cd /tmp/audit-work/lean-proof-audit.Y1Auq5
export LD_PRELOAD=/tmp/audit-work/proc_self_exe_fix.so
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
lake env lean AuditOperational.lean
```

Complete evaluated boundary and mutation results: `54-operational-adversarial-tests.txt`.
