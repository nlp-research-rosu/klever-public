# Audit command and status index

All relative K commands below ran with working directory
`/tmp/audit-work/reconstruction` unless another directory is stated. Full
bounded output is in the named log.

## Provenance and program fidelity

| Command | Exit | Log |
|---|---:|---|
| `python3 /audit-output/evidence/provenance_check.py` | 0 | `stage1-provenance.log` |
| `python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/regenerated-solution.mpy; cmp -s /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/reconstruction/solution.mpy` | 0, 0 | `stage2-translation-success.log` |
| `python3 /audit-output/evidence/differential_test.py` | 0 | `stage2-differential.log` |
| `kompile --version; kprove --version; krun --version; python3 --version` | 0 | `toolchain.log` |

The first translation logging wrapper used `/bin/sh` with unsupported
`set -o pipefail` and exited 2 before translation; it is retained in
`stage2-translation.log`. It was a reviewer wrapper error, and the successful
rerun above is the evidence used.

## Clean builds and generated-semantics execution

| Command | Exit | Log |
|---|---:|---|
| `kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled` | 0 | `stage3-kompile-semantic-llvm.log` |
| `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | 0 | `stage3-kompile-verification-haskell.log` |
| `krun solution.mpy --definition semantic-llvm-kompiled -cINPUT=.Vals` | 0 | `stage3-krun-empty.log` |
| `krun solution.mpy --definition semantic-llvm-kompiled -cINPUT='num(4,1) :: num(3,1) :: num(17,10) :: num(2,1) :: num(35,10) :: .Vals'` | 0 | `stage3-krun-prompt.log` |
| `krun solution.mpy --definition semantic-llvm-kompiled -cINPUT='num(4,1) :: num(37,10) :: num(33,10) :: num(3,1) :: num(27,10) :: num(23,10) :: num(2,1) :: num(17,10) :: num(13,10) :: num(1,1) :: num(7,10) :: num(0,1) :: .Vals'` | 0 | `stage3-krun-thresholds.log` |
| `krun solution.mpy --definition semantic-llvm-kompiled -cINPUT='num(4165829655317709,1125899906842624) :: .Vals'` | 0 | `stage3-krun-ieee-3.7-witness.log` |
| `python3 /audit-output/evidence/ieee_bridge_witness.py` | 0 | `stage3-ieee-bridge-python-success.log` |

The first Python witness script used an unintended chained comparison in its
assertion and exited 1 after printing the correct observations; that reviewer
script error is retained in `stage3-ieee-bridge-python.log`. The corrected
script and successful log above are authoritative.

## Isolated positive proofs

`run_positive_claims.sh` invoked the following command once for each label:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.<label>
```

Every run exited 0 and printed exactly one `#Top`.

| Label | Log |
|---|---|
| `empty-input` | `stage3-kprove-empty-input.log` |
| `all-single-grades` | `stage3-kprove-all-single-grades.log` |
| `loop-step-new-variable` | `stage3-kprove-loop-step-new-variable.log` |
| `loop-step-existing-variable` | `stage3-kprove-loop-step-existing-variable.log` |
| `loop-empty` | `stage3-kprove-loop-empty.log` |
| `prompt-example` | `stage3-kprove-prompt-example.log` |

## Pinning and sensitivity

| Command | Exit | Log |
|---|---:|---|
| `python3 /audit-output/evidence/program_term_compare.py` (two explicit `kast ... --module VERIFICATION --sort Module --output kore` commands are printed by the script) | 0 | `stage4-program-term-compare-success.log` |
| `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled` in `/tmp/audit-work/body-mutation` | 0 | `stage4-body-mutation-kompile.log` |
| `kprove spec.k --definition body-mutated-kompiled --spec-module SPEC --claims SPEC.all-single-grades` in `/tmp/audit-work/body-mutation` | 1, expected | `stage4-body-mutation-kprove.log` |

The first constructor comparison attempted to parse K's internal `.Exprs`
empty-list spelling as external MPy syntax and exited 1. It is retained in
`stage4-program-term-compare.log`; the successful rerun normalizes `.Exprs` to
the external empty spelling and obtains identical KORE hashes.

## Inventory and non-vacuity

| Command | Exit | Log |
|---|---:|---|
| `rg -n '^\s*(syntax|configuration|rule|claim)' semantic.k verification.k spec.k` plus rule/claim counts | 0 | `stage5-static-extraction.log` |
| `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run` | 0 | `stage6-vacuity-dry-run.log` |
| `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY` | 1, expected | `stage6-vacuity-kprove.log` |

The fresh mutation source is `spec-vacuity.k`. Its input `[4.0]` is
satisfiable, the definition/spec build succeeds, and the proof residual shows
the actual `A+` value failing to unify with the false `WRONG` result.
