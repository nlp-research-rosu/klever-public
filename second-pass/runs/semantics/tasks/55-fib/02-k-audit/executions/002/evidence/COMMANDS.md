# Audit command index

All K commands ran from `/tmp/audit-work/55-fib-audit`; no candidate
definition or cache was reused. The linked terminal transcripts record the
exact command, timestamps, bounded output, and `COMMAND_EXIT_CODE`.

| Purpose | Exact command | Exit | Evidence |
|---|---|---:|---|
| Provenance/integrity | `python3 /audit-output/evidence/stage1_integrity.py` | 0 | `stage1-integrity.log` |
| Trusted regeneration identity | `python3 ../trusted/py2mpy.py solution.py \| cmp - solution.mpy` | 0 | `stage2-translation.log` |
| Python differential | `python3 /audit-output/evidence/differential_fib.py` | 0 | `stage2-differential.log` |
| Fresh LLVM definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition fresh-runtime-kompiled` | 0 | `stage3-kompile-llvm.log` |
| Concrete audit program | `krun concrete-audit.mpy --definition fresh-runtime-kompiled` | 0 | `stage3-krun-concrete.log` |
| Actual solution module load | `krun solution.mpy --definition fresh-runtime-kompiled` | 0 | `stage3-krun-solution-module.log` |
| Fresh Haskell definition | `kompile verification.k --backend haskell --main-module FIB-VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled` | 0 | `stage3-kompile-haskell.log` |
| Original complete spec | `kprove spec.k --definition fresh-verification-kompiled --spec-module FIB-SPEC` | 0, `#Top` | `stage3-kprove-all.log` |
| Loop lemma alone | `kprove spec.k --definition fresh-verification-kompiled --spec-module FIB-SPEC --claims FIB-SPEC.fib-loop` | 0, `#Top` | `stage3-kprove-fib-loop.log` |
| Entry theorem composed with separately proved loop lemma | `kprove spec.k --definition fresh-verification-kompiled --spec-module FIB-SPEC --claims FIB-SPEC.fib-loop,FIB-SPEC.fib-all-natural --trusted FIB-SPEC.fib-loop` | 0, `#Top` | `stage3-kprove-fib-all-natural-with-proven-lemma.log` |
| Mechanical program pin | `python3 /audit-output/evidence/pinning_check.py` | 0 | `stage4-pinning.log` |
| Ground witnesses | `python3 /audit-output/evidence/ground_witnesses.py` | 0 | `stage4-ground-witnesses.log` |
| Body-mutation definition | `kompile verification.k --backend haskell --main-module FIB-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled` | 0 | `stage4-body-mutation-build.log` |
| Body-sensitivity proof | `kprove spec.k --definition body-mutated-kompiled --spec-module FIB-SPEC` | 1, expected stuck claim | `stage4-body-mutation-proof.log` |
| False-spec parse/build | `kprove spec-vacuity-audit.k --definition fresh-verification-kompiled --spec-module FIB-SPEC-VACUITY --dry-run` | 0 | `stage6-vacuity-dry-run.log` |
| False-spec proof | `kprove spec-vacuity-audit.k --definition fresh-verification-kompiled --spec-module FIB-SPEC-VACUITY` | 1, expected stuck claim | `stage6-vacuity-proof.log` |

One additional diagnostic selected only `fib-all-natural`, thereby filtering
out its declared `fib-loop` dependency. It was manually interrupted (exit 130)
after it began unbounded symbolic loop unrolling. It is preserved as
`stage3-kprove-fib-all-natural.log` but is not a target proof result. The
original unfiltered proof and the explicit separately-proved-lemma composition
both closed.
