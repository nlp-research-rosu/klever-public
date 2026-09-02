# Reviewer evidence index

All commands ran from `/audit-output` unless the entry names another working
directory. Logs were captured with `script -q -e -c 'COMMAND; ...' LOG`; the
commands below are the exact substantive commands inside that wrapper.

| Evidence | Exact substantive command | Result |
|---|---|---|
| `01-provenance.log` | `python3 /audit-output/evidence/check_provenance.py` | exit 0; required records, direct hashes, tree provenance, campaign lock, regular-file/symlink checks, and all 272 trace JSON records passed |
| `02-regeneration.log` | `python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy` then `cmp -s /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy` | both exit 0; identical SHA-256 `65fdcbb2...a49b1a8` |
| `03-differential.log` | `python3 /audit-output/evidence/differential_test.py` | exit 0; 2,205 generated nonempty cases and all nonempty fixed cases matched; empty boundary differed as recorded |
| `04-build-concrete.log` | `kompile --backend llvm semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-kompiled` | exit 0 with a non-exhaustive `[total] distinctCount` warning |
| `05-build-proof.log` | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION --output-definition proof-kompiled -I .` | exit 0 |
| `06-concrete-semantics.log` | `python3 /audit-output/evidence/concrete_semantics_test.py` against the first LLVM definition | script exit 1; pattern search was unavailable because the definition lacked `--enable-search` |
| `07-build-concrete-search.log` | `kompile --backend llvm semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --enable-search --output-definition concrete-search-kompiled` | exit 0 with the same non-exhaustive-total warning |
| `08-concrete-semantics-rerun.log` | `python3 /audit-output/evidence/concrete_semantics_test.py` against `concrete-search-kompiled` | script exit 1; empty input was `#Top`, every nonempty case was `#Bottom` under LLVM |
| `09-build-semantic-haskell.log` | `kompile --backend haskell semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition semantic-haskell-kompiled` | exit 0 |
| `10-concrete-semantics-haskell.log` | `python3 /audit-output/evidence/concrete_semantics_test.py` against `semantic-haskell-kompiled` | ASCII cases were `#Top`; two Unicode search-pattern checks printed `#Bottom`, so actual configurations were inspected next |
| `11-unicode-actual-results.log` | `krun solution.mpy --definition semantic-haskell-kompiled -cINPUT='cons("é", cons("é", nil))' --output pretty` and `krun solution.mpy --definition semantic-haskell-kompiled -cINPUT='cons("😀a", cons("東京", cons("λλ", nil)))' --output pretty` | both exit 0; actual final configurations recorded |
| `12-unicode-counterexample.log` | `python3 -c '... solution.find_max(["😀", "abc"]) ...'` and `krun solution.mpy --definition semantic-haskell-kompiled -cINPUT='cons("😀", cons("abc", nil))' --output pretty` | both exit 0; Python returned `"abc"`, K returned `"😀"` with count 4 |
| `13-kprove-program-initializes.log` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.program-initializes` | exit 0, `#Top` |
| `14-kprove-loop-correct.log` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.loop-correct` | exit 0, `#Top` |
| `15-kprove-find-max-correct.log` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.find-max-correct` | reviewer terminated the diagnostic after more than 90 seconds; filtering out the loop claim also removed the needed circularity |
| `16-kprove-find-max-with-proved-loop.log` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.find-max-correct --trusted SPEC.loop-correct` | reviewer terminated the nonproductive diagnostic after more than 120 seconds; no candidate verdict is inferred from it |
| `17-kprove-all-claims.log` | `kprove spec.k --definition proof-kompiled --spec-module SPEC` | exit 0, `#Top` |
| `18-kprove-end-with-loop-dependency.log` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.loop-correct,SPEC.find-max-correct` | exit 0, `#Top`; isolates the end theorem with its proved circularity |
| `19-program-pinning-depth0.log` | two `krun ... --depth 0` commands without `-cINPUT` | both exit 1 for the expected missing configuration variable; corrected next |
| `20-program-pinning-depth0-rerun.log` | `krun solution.mpy ... -cINPUT=nil --depth 0 --output kast` and the same for `solution-symbol.mpy` | both exit 0; parsed source term and symbolic alias recorded |
| `21-program-pinning-depth1.log` | `krun solution.mpy ... -cINPUT=nil --depth 1 --output pretty` and the same for `solution-symbol.mpy` | both exit 0 and reach the same constructor-level execution state |
| `22-program-pinning-mechanical-compare.log` | the same two depth-1 runs with `--output kore`, followed by `cmp -s /tmp/audit-work/source-depth1.kore /tmp/audit-work/symbol-depth1.kore` | both runs and comparison exit 0; both SHA-256 values are `9ded476e...ab8b072` |
| `23-body-mutation-build.log` | change `Call(Name("len"), Call(Name("set"), Name("word")))` to `Int(0)`, then `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION --output-definition body-mutated-kompiled -I .` | build exit 0; exact mutation preserved in `body-mutation-verification.k` |
| `24-body-mutation-expected-failure.log` | `kprove spec.k --definition body-mutated-kompiled --spec-module SPEC --claims SPEC.loop-correct` | underlying kprove exit 1 with `WarnStuckClaimState`; wrapper exits 0 because failure was expected |
| `25-false-mutation-dry-run.log` | `kprove spec-false-result.k --definition proof-kompiled --spec-module SPEC-VACUITY --dry-run` | exit 0; mutation parses and builds |
| `26-false-mutation-expected-failure.log` | `kprove spec-false-result.k --definition proof-kompiled --spec-module SPEC-VACUITY` | underlying kprove exit 1 with actual result `"a"` versus required `"wrong"`; wrapper exits 0 |
| `27-rule-inventory-extraction.log` | `rg -n '^\s*(syntax|configuration|rule|claim)' semantic.k verification.k spec.k` plus declaration counts | exit 0; 42 semantic rules, 9 verification equations, and 3 claims |
