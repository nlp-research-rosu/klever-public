# Auditor command index

All commands used candidate sources copied to
`/tmp/audit-work/76-is-simple-power`.  The `.log` transcripts contain relevant
stdout/stderr and a final `COMMAND_EXIT_CODE`.

| Purpose | Exact command | Exit | Transcript |
|---|---|---:|---|
| Mounted-input integrity | `python3 /audit-output/evidence/01_integrity.py` | 0 | `01_integrity.log` |
| Trusted translation identity | `python3 /reference/py2mpy.py /tmp/audit-work/76-is-simple-power/solution.py > /tmp/audit-work/76-is-simple-power/solution.regenerated.mpy; cmp -s /tmp/audit-work/76-is-simple-power/solution.regenerated.mpy /tmp/audit-work/76-is-simple-power/solution.mpy` | 0 | `02_translation_identity.log` |
| Python differential | `python3 /audit-output/evidence/02_differential.py` | 0 | `02_differential.log` |
| Fresh concrete build | `kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition fresh-semantic-kompiled` | 0 | `03_build_concrete.log` |
| Fresh proof build | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled` | 0 | `03_build_proof.log` |
| All claims, individually | `/audit-output/evidence/03_run_positive_claims.sh` | 0 | `03_positive_claims.log` |
| Fresh concrete comparison | `python3 /audit-output/evidence/03_concrete_compare.py` | 0 | `03_concrete_compare.log` |
| Pinning and claim witnesses | `python3 /audit-output/evidence/04_pinning_and_witnesses.py` | 0 | `04_pinning_and_witnesses.log` |
| Body-mutation build | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled` | 0 | `04_body_mutation_build.log` |
| Body-mutation proof | `kprove spec.k --definition body-mutated-kompiled --claims SPEC.returns-on-one` | 1, expected | `04_body_mutation_proof.log` |
| Source inventory | `rg -n "^[[:space:]]*(requires\|module\|imports\|syntax\|configuration\|rule\|claim\|endmodule)" semantic.k verification.k spec.k` | 0 | `05_source_inventory.log` |
| False-result parse/build | `kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --dry-run` | 0 | `06_mutation_dry_run.log` |
| False-result proof | `kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY` | 1, expected | `06_mutation_proof.log` |

`03_positive_claims.log` prints the exact six `kprove` commands and their
individual exits.  `03_concrete_compare.log` prints every exact `krun` command,
full final configuration, and exit.
