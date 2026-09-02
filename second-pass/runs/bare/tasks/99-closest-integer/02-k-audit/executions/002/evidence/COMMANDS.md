# Reviewer command index

Every command was run from the stated working directory. The corresponding
typescript log ends with `COMMAND_EXIT_CODE` from `script -e`.

| Stage | Working directory | Exact command inside `script -q -e -c` | Exit | Log |
|---|---|---|---:|---|
| Tools | `/audit-output` | `command -v kompile && kompile --version && command -v krun && krun --version && command -v kprove && kprove --version && python3 --version` | 0 | `00-tool-versions.log` |
| 1 | `/audit-output` | `python3 /audit-output/evidence/integrity_check.py` | 0 | `01-integrity.log` |
| 1 | `/audit-output` | `python3 /audit-output/evidence/trace_summary.py` | 0 | `01-trace-summary.log` |
| 2 | `/audit-output` | `python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/solution.regenerated.mpy && cmp -s /tmp/audit-work/candidate/solution.mpy /tmp/audit-work/candidate/solution.regenerated.mpy && sha256sum /tmp/audit-work/candidate/solution.mpy /tmp/audit-work/candidate/solution.regenerated.mpy` | 0 | `02-regeneration.log` |
| 2 | `/audit-output` | `python3 /audit-output/evidence/differential_test.py` | 0 | `02-differential.log` |
| 3 | `/tmp/audit-work/candidate` | `kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition semantic-audit-kompiled` | 0 | `03-kompile-semantic.log` |
| 3 | `/tmp/audit-work/candidate` | `kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition verification-audit-kompiled` | 0 | `03-kompile-verification.log` |
| 3 | `/tmp/audit-work/candidate` | `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | 0, `#Top` | `03-kprove-positive.log` |
| 3 | `/tmp/audit-work/candidate` | `python3 /audit-output/evidence/semantic_differential.py` | 1, two semantic mismatches | `03-semantic-differential.log` |
| 4 | `/tmp/audit-work/candidate` | `python3 /audit-output/evidence/program_term_compare.py` | 0, equal KASTs | `04-program-term-compare.log` |
| 4 | `/tmp/audit-work/candidate` | `python3 /audit-output/evidence/adequacy_witness.py` | 0 | `04-adequacy-witness.log` |
| 4 | `/tmp/audit-work/candidate` | `kompile body-mutant-verification.k --main-module BODY-MUTANT-VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition body-mutant-kompiled` | 0 | `04-body-mutant-build.log` |
| 4 | `/tmp/audit-work/candidate` | `kprove body-mutant-spec.k --definition body-mutant-kompiled --spec-module BODY-MUTANT-SPEC` | 1, expected stuck result | `04-body-mutant-proof.log` |
| 5 | `/tmp/audit-work/candidate` | `rg -n "^[[:space:]]*(syntax\|configuration\|rule\|claim)" semantic.k verification.k spec.k && printf "semantic_rules=" && rg -c "^[[:space:]]*rule " semantic.k && printf "verification_rules=" && rg -c "^[[:space:]]*rule " verification.k && printf "spec_claims=" && rg -c "^[[:space:]]*claim" spec.k && rg -n "\[(function\|total\|functional\|simplification\|simplify\|priority\|owise\|opaque\|macro)" semantic.k verification.k \|\| true` | 0 | `05-static-declaration-scan.log` |
| 6 | `/tmp/audit-work/candidate` | `kprove spec-vacuity-audit.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run` | 0 | `06-vacuity-build.log` |
| 6 | `/tmp/audit-work/candidate` | `kprove spec-vacuity-audit.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY-AUDIT` | 1, expected stuck result | `06-vacuity-proof.log` |

Diagnostic attempts retained for transparency:

- `04-program-identity-first-parser-context.log`: direct functional-term claim
  failed to parse the translator's empty-list shorthand.
- `04-program-identity.log`: after the equivalent `.Stmts` normalization, the
  installed Haskell backend rejected a functional claim as unsupported. This
  was replaced by the successful constructor KAST comparison.
- `04-program-term-compare-first-parser-context.log`: standalone program
  parsing rejects `.Stmts`; the successful comparison normalized the proof term
  back to the translator's empty-list spelling.
- `03-semantic-differential-first-parser-bug.log`: the first reviewer harness
  used an over-escaped result regex. The visible K results were correct except
  for the same whitespace and underscore cases; the corrected script and final
  log are authoritative.
