# Essential audit commands

All commands ran from the copied workspaces named below. `script -q -e -c`
captured complete terminal output and the command exit status in the cited log.

## Hash, inventory, bijection, and target checks

```sh
PYTHONPATH=/reference python /audit-output/evidence/independent_checks.py
```

Result: exit 0; see
`independent-hash-inventory-target-checks-final.log`.

## Stage 4 trusted preflight

The direct first run exposed the sandbox PID/proc mismatch:

```sh
PYTHONPATH=/reference python /audit-output/evidence/run_preflight.py
```

Result: exit 1 at `lake clean`; see `stage4-preflight-rerun.log`.

The source-recorded PID shim was compiled and the same trusted check rerun:

```sh
cc -shared -fPIC -O2 \
  -o /tmp/audit-work/hostpid_shim.so \
  /audit-output/evidence/hostpid_shim.c
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so \
  PYTHONPATH=/reference \
  python /audit-output/evidence/run_preflight.py
```

Result: exit 0, status `PASS`; see
`stage4-preflight-rerun-with-hostpid.log`.

## Fresh proof copy and clean build

The fresh proof workspace was `/tmp/audit-work/proof-audit`; the immutable
generated project was copied to its `Base/` directory.

```sh
cd /tmp/audit-work/proof-audit/Base
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so lake clean
cd /tmp/audit-work/proof-audit
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so lake build
```

Results: all exit 0; see `proof-base-lake-clean.log`,
`proof-lake-clean.log`, and `proof-lake-build.log`.

## Trusted Stage 5 mechanical gate

```sh
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so \
  PYTHONPATH=/reference \
  python /audit-output/evidence/run_proof_gate.py
```

Result: exit 0, status `PASS`; see `proof-mechanical-gate.log`.

## Exact theorem and axiom check

```sh
cd /tmp/audit-work/proof-audit
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so \
  lake env lean /audit-output/evidence/proof_identity.lean
```

Result: exit 0; exact output is in `proof-identity-and-axioms.log` and
`proof-print-axioms.log`.

## Operational-bridge adversarial checks

```sh
cd /tmp/audit-work/proof-audit
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so \
  lake env lean /audit-output/evidence/operational_bridge_tests.lean
```

Result: exit 0; see `operational-bridge-tests.log`.

For nonempty membership/deletion cases, an inspection copy changed only the
two helper declarations from `private noncomputable def` to
`noncomputable def`; the bodies and theorem were unchanged:

```sh
cd /tmp/audit-work/operational-inspect
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so lake build
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so \
  lake env lean /audit-output/evidence/operational_nonempty_tests.lean
```

Results: exit 0; see `operational-inspect-only-diff.log`,
`operational-inspect-build.log`, and `operational-nonempty-tests.log`.

## Candidate source and frozen target checks

```sh
rg -n '\b(sorry|admit|unsafe|axiom|opaque)\b|targetStatement|^(noncomputable )?def |^theorem final' \
  /candidate --glob '*.lean'
sha256sum \
  /reference/klean-generation/generated/Klean70StrangeSortList/Lemmas.lean \
  /tmp/audit-work/proof-audit/Base/Klean70StrangeSortList/Lemmas.lean
cmp \
  /reference/klean-generation/generated/Klean70StrangeSortList/Lemmas.lean \
  /tmp/audit-work/proof-audit/Base/Klean70StrangeSortList/Lemmas.lean
```

Results: no forbidden token or target redeclaration; `cmp` exit 0. See
`candidate-source-audit.log` and `proof-target-file-identity.log`.
