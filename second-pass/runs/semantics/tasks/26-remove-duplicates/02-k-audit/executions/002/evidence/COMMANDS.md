# Evidence command ledger

All paths are container paths. `script -q -e -c ... LOG` wrapped the commands
that have typescript logs; the exit statuses below are the wrapped command
statuses recorded in each log footer.

| CWD | Command | Exit | Evidence |
|---|---|---:|---|
| `/audit-output` | `python3 evidence/stage1_integrity.py` | 0 | `stage1_integrity.log` |
| `/tmp/audit-work/candidate-scratch` | `python3 /tmp/audit-work/trusted/py2mpy.py solution.py > solution.regenerated.mpy; cmp -s solution.regenerated.mpy solution.mpy; sha256sum solution.py solution.mpy solution.regenerated.mpy` | 0 | `translator_regeneration.log` |
| `/audit-output` | `python3 evidence/differential_test.py` | 0 | `differential_test.log` |
| `/tmp/audit-work/candidate-scratch` | `kompile --version; kprove --version; krun --version` | 0 | `tool_versions.log` |
| `/tmp/audit-work/candidate-scratch` | `python3 /tmp/audit-work/trusted/py2mpy.py /audit-output/evidence/k_concrete_tests.py > audit-concrete-tests.mpy; kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled; krun audit-concrete-tests.mpy --definition audit-runtime-kompiled --output pretty` | 0 | `concrete_rebuild_and_run.log` |
| `/tmp/audit-work/candidate-scratch` | `kompile verification.k --backend haskell --main-module REMOVE-DUPLICATES-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 | `proof_rebuild.log` |
| `/tmp/audit-work/candidate-scratch` | `kprove spec.k --definition audit-verification-kompiled --spec-module REMOVE-DUPLICATES-SPEC --claims REMOVE-DUPLICATES-SPEC.loop-invariant --output pretty` | 0, `#Top` | `prove_loop_invariant.log` |
| `/tmp/audit-work/candidate-scratch` | `kprove spec.k --definition audit-verification-kompiled --spec-module REMOVE-DUPLICATES-SPEC --trusted REMOVE-DUPLICATES-SPEC.loop-invariant --output pretty` | 0, `#Top` | `prove_all_entries.log` |
| `/tmp/audit-work/candidate-scratch` | `kprove spec.k --definition audit-verification-kompiled --spec-module REMOVE-DUPLICATES-SPEC --claims REMOVE-DUPLICATES-SPEC.entry-empty --trusted REMOVE-DUPLICATES-SPEC.loop-invariant --output pretty` | 0, `#Top` | `prove_entry_empty.log` |
| `/audit-output` | `python3 evidence/program_pinning.py` | 0 | `program_pinning.log` |
| `/audit-output` | `python3 evidence/claim_witnesses.py` | 0 | `claim_witnesses.log` |
| `/audit-output` | `python3 evidence/build_rule_inventory.py > evidence/rule_inventory.tsv` | 0 | `rule_inventory_build.log` |
| `/tmp/audit-work/body-mutation` | `kompile verification.k --backend haskell --main-module REMOVE-DUPLICATES-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled` | 0 | `body_mutation_build.log` |
| `/tmp/audit-work/body-mutation` | `kprove spec.k --definition body-mutated-kompiled --spec-module REMOVE-DUPLICATES-SPEC --claims REMOVE-DUPLICATES-SPEC.loop-invariant --output pretty` | 1, expected stuck claim | `body_mutation_proof.log` |
| `/tmp/audit-work/candidate-scratch` | `kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module REMOVE-DUPLICATES-SPEC-VACUITY --claims REMOVE-DUPLICATES-SPEC-VACUITY.entry-empty --dry-run --output pretty` | 0 | `vacuity_mutation_build.log` |
| `/tmp/audit-work/candidate-scratch` | `kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module REMOVE-DUPLICATES-SPEC-VACUITY --claims REMOVE-DUPLICATES-SPEC-VACUITY.entry-empty --output pretty` | 1, expected stuck claim | `vacuity_mutation_proof.log` |

One diagnostic command selected only `entry-keep` while also naming the
invariant as trusted. It was interrupted after approximately 300 seconds
(status 130) because claim selection excluded the lemma from the selected set.
It is not a target-proof command; details are in
`prove_entry_keep_attempt.md`. The candidate's actual two-phase workflow is
the two successful `kprove` commands above.
