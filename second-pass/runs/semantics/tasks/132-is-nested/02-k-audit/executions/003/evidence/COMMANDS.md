# Reviewer command record

All commands ran from `/tmp/audit-work/reconstruction` unless a different
working directory is stated. Definitions were newly produced below
`/tmp/audit-work`; none came from `/candidate`.

| Evidence | Exact command | Actual status/result |
|---|---|---|
| `01-provenance.log` | `python3 /audit-output/evidence/provenance_check.py` | 0; all required records, direct hashes, workspace tree hashes, JSONL records, prompt/translator equality, and supplied-semantics comparisons passed |
| `02-regeneration.log` | `python3 py2mpy.py solution.py > solution.regenerated.mpy` then `cmp -s solution.regenerated.mpy solution.mpy` | 0, 0; byte identity |
| `03-differential-final.log` | `python3 /audit-output/evidence/differential_test.py /reference/canonical.py /tmp/audit-work/reconstruction/solution.py` | 0; 34,797 checks, zero mismatches |
| `04-toolchain.log` | `command -v kompile; command -v krun; command -v kprove; kompile --version; krun --version; kprove --version` | 0; all v7.1.293 |
| `05-concrete-harness-fidelity.log` | Python `ast.dump(..., include_attributes=False)` equality check between `solution.py:is_nested` and `concrete_harness.py:is_nested` | 0; identical |
| `06-kompile-llvm.log` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 |
| `07-krun-concrete.log` | `python3 py2mpy.py /audit-output/evidence/concrete_harness.py > audit-concrete.mpy` then `krun audit-concrete.mpy --definition audit-runtime-kompiled --output pretty` | 0, 0; `.K`, `NoExc`, exit code 0 |
| `08-kompile-proof-base.log` | `kompile verification.k --backend haskell --main-module IS-NESTED-VERIFICATION --syntax-module IS-NESTED-VERIFICATION --output-definition audit-verification-kompiled` | 0 |
| `09-kprove-loop.log` | `kprove --definition audit-verification-kompiled --spec-module IS-NESTED-LOOP-SPEC spec.k` | 0, `#Top` |
| `10-kompile-proof-lemma.log` | `kompile verification.k --backend haskell --main-module IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA --syntax-module IS-NESTED-VERIFICATION --output-definition audit-verification-with-lemma-kompiled` | 0 |
| `11-kprove-empty.log` | `kprove --definition audit-verification-with-lemma-kompiled --spec-module IS-NESTED-TOP-SPEC --claims IS-NESTED-TOP-SPEC.empty-input spec.k` | 0, `#Top` |
| `12-kprove-universal.log` | `kprove --definition audit-verification-with-lemma-kompiled --spec-module IS-NESTED-TOP-SPEC --claims IS-NESTED-TOP-SPEC.all-bracket-strings spec.k` | 0, `#Top` |
| `13b-kprove-source-pinning.log` | `kprove --definition audit-verification-kompiled --spec-module SOURCE-PINNING-SPEC source-pinning-spec.k` | 0, `#Top`; both constructor-equality claims compile to trivial equality |
| `14-claim-witnesses.log` | `python3 /audit-output/evidence/claim_witnesses.py` | 0; every listed ground substitution agrees |
| `15-body-mutation.diff` | `diff -u /tmp/audit-work/reconstruction/verification.k /tmp/audit-work/body-mutation/verification.k` | 1 as expected for one body change: code point 91 to 93 |
| `16-kompile-body-mutant.log` | `kompile verification.k --backend haskell --main-module IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA --syntax-module IS-NESTED-VERIFICATION --output-definition body-mutant-kompiled` (cwd `/tmp/audit-work/body-mutation`) | 0 |
| `17-kprove-body-mutant-pinning.log` | `kprove --definition body-mutant-kompiled --spec-module SOURCE-PINNING-SPEC source-pinning-spec.k` | 1 expected; `WarnStuckClaimState` exposes code point 93 |
| `18-kprove-body-mutant-universal.log` | `kprove --definition body-mutant-kompiled --spec-module IS-NESTED-TOP-SPEC --claims IS-NESTED-TOP-SPEC.all-bracket-strings spec.k` | 1 expected; residual fixes `BS` to `[[]]` and computed `false` |
| `19-rule-inventory-status.log` | `python3 /audit-output/evidence/inventory_k.py > /audit-output/evidence/rule-inventory.tsv` | 0; 953 records |
| `20-kprove-bridge-witness-fixed.log` | `kprove --definition audit-verification-kompiled --spec-module BRIDGE-WITNESS-FIXED-SPEC bridge-witness-spec.k` | 0, `#Top`; fixed semantics returns `false` |
| `21-kprove-bridge-witness-extended.log` | `kprove --definition audit-verification-with-lemma-kompiled --spec-module BRIDGE-WITNESS-EXTENDED-SPEC bridge-witness-spec.k` | 0, `#Top`; unsound bridge returns `true` from the same state |
| `22-vacuity-dry-run.log` | `kprove --dry-run --definition audit-verification-with-lemma-kompiled --spec-module SPEC-VACUITY spec-vacuity.k` | 0; mutation parsed and emitted backend command |
| `23-kprove-vacuity.log` | `kprove --definition audit-verification-with-lemma-kompiled --spec-module SPEC-VACUITY spec-vacuity.k` | 1 expected; `WarnStuckClaimState` shows computed `false` against required `true` |

Two retained reviewer-development logs are not candidate failures:

- `03-differential.log` and `03-differential-fast.log` used an initially wrong
  expected value for the long alternating string. An alternating string does
  have `[[]]` as a non-contiguous subsequence across adjacent pairs. The
  corrected script and authoritative result are
  `differential_test.py` and `03-differential-final.log`.
- `13-kprove-source-pinning.log` attempted raw functional reachability claims;
  the Haskell backend reports that form unsupported. Wrapping the same
  constructor equalities in full configurations produced
  `13b-kprove-source-pinning.log` with status 0 and `#Top`.
