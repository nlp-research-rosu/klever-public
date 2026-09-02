# Reviewer evidence index

All candidate artifacts were treated as read-only. Builds and generated K inputs
were created in `/tmp/audit-work`; this directory contains reviewer-authored
scripts/specifications and bounded logs copied or emitted for the audit.

## Environment and provenance

- `00-toolchain.log`: `/usr/bin/{kompile,kprove,krun}` and K `v7.1.293`.
- `provenance_check.py`, `01-provenance.log`: symlink-safe type/content
  comparison of prompt, translator, and the complete supplied-semantics tree.
  Exit `0`, zero failures.
- `generation_claims_digest.py`, `01-generation-claims.log`: bounded digest of
  all four untrusted generation records and the complete 813-line structured
  trace. Exit `0`, zero JSON parse failures.

## Program fidelity and independent execution

- `differential_test.py`, `run_stage2.sh`, `02-program-fidelity.log`: trusted
  translation identity and 12,015-case canonical differential. Exit `0`, zero
  mismatches. The log also records the excluded negative-input divergence.
- `concrete_harness.py`, `run_stage3.sh`, `03a-*` through `03c-*`: fresh LLVM
  compile and twelve concrete K assertions. All exits `0`; final `.K`, `NoExc`,
  exit code `0`.

## Positive proof reconstruction

- `03d-kompile-verification-base.log`: fresh Haskell base build, exit `0`.
- `03e-kprove-loop.log`: isolated `LOOP-SPEC.outer-loop`, `#Top`, exit `0`.
- `03f-kompile-verification-full.log`: fresh Haskell full build, exit `0`.
- `03g-kprove-entry.log`: isolated `SPEC.entry`, `#Top`, exit `0`.

## Adequacy and bridge sensitivity

- `spec-concrete-adequacy.k`, `run_adequacy.sh`, `04-kprove-*.log`: empty
  specialization closes; concrete `[1]` and `[2]` result specializations fail
  with residual oracle assignments. Statuses `0`, `1`, `1`, as expected.
- `audit-no-condition-bridge.k`, `spec-no-condition-bridge.k`,
  `run_bridge_control.sh`, `05a-*` through `05c-*`: fixed-semantics control
  definition that omits the candidate condition bridge. Fresh build and both
  concrete ground claims print `#Top`; all exits `0`.

## Static inventory

- `inventory_k.py`, `run_inventory.sh`, `05-rule-inventory.log`,
  `05-rule-inventory.tsv`: exhaustive 968-entry inventory (plus header/summary):
  one configuration, five contexts, 227 supplied syntax declarations, 695
  supplied rules, ten candidate syntax declarations, twenty candidate rules,
  and two claims. Generation exits `0`.

## Fresh non-vacuity mutation

- `spec-fresh-vacuity.k`, `run_fresh_vacuity.sh`,
  `06a-fresh-vacuity-dry-run.log`, `06b-fresh-vacuity-proof.log`: the empty
  input is falsely required to produce `[1]`. Dry-run/build exits `0`; proof
  reaches the expected result/heap mismatch and exits `1`.
