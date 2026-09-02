# Reviewer command ledger

Unless stated otherwise, the working directory was `/tmp/audit-work`. The
corresponding `.log` files contain bounded stdout/stderr and a `script` footer
with `COMMAND_EXIT_CODE`. Compound negative probes also print the inner
`kprove`/`cmp` status explicitly.

| Evidence | Exact command | Status |
|---|---|---:|
| `tool_versions.log` | `kompile --version && kprove --version && python3 --version` | 0; K 7.1.293, Python 3.10.12 |
| `stage1_integrity.log` | `python3 /audit-output/evidence/stage1_integrity.py` (working directory `/audit-output`) | 0 |
| `translation_identity.log` | `python3 py2mpy.py solution.py > regenerated-solution.mpy && cmp -s regenerated-solution.mpy solution.mpy && sha256sum regenerated-solution.mpy solution.mpy && echo BYTE_IDENTITY_OK` | 0 |
| `differential_test.log` | `python3 /audit-output/evidence/differential_test.py` | 0 |
| `kompile_llvm.log` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 |
| `krun_concrete.log` | `python3 py2mpy.py concrete_tests.py > audit-concrete-tests.mpy && cmp -s audit-concrete-tests.mpy concrete_tests.mpy && krun audit-concrete-tests.mpy --definition audit-runtime-kompiled` | 0 |
| `kompile_haskell.log` | `kompile verification.k --backend haskell --main-module PILE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 |
| `kprove_prefix.log` | `kprove spec.k --definition audit-verification-kompiled --spec-module PILE-PREFIX-SPEC` | 0, `#Top` |
| `kprove_loop.log` | `kprove spec.k --definition audit-verification-kompiled --spec-module PILE-LOOP-SPEC` | 0, `#Top` |
| `constructor_identity.log` | `kast solution.mpy --definition audit-verification-kompiled --module PILE-VERIFICATION --sort Module --expand-macros --output json --output-file audit-solution-expanded.json && kast --expression pileModule --definition audit-verification-kompiled --module PILE-VERIFICATION --sort Module --expand-macros --output json --output-file audit-claim-program-expanded.json && cmp -s audit-solution-expanded.json audit-claim-program-expanded.json && sha256sum audit-solution-expanded.json audit-claim-program-expanded.json && echo CONSTRUCTOR_IDENTITY_OK` | 0 |
| `claim_witness.log` | `python3 /audit-output/evidence/claim_witness.py` | 0 |
| `body_mutation_kompile.log` | `kompile verification-body-mutation.k --backend haskell --main-module PILE-VERIFICATION-BODY-MUTATION --syntax-module MPY-SYNTAX --output-definition audit-body-mutation-kompiled` | 0 |
| `body_mutation_constructor.log` | `kast solution.mpy --definition audit-body-mutation-kompiled --module PILE-VERIFICATION-BODY-MUTATION --sort Module --expand-macros --output json --output-file audit-original-under-mutated-definition.json; kast --expression pileModuleMut --definition audit-body-mutation-kompiled --module PILE-VERIFICATION-BODY-MUTATION --sort Module --expand-macros --output json --output-file audit-mutated-claim-program.json; cmp -s audit-original-under-mutated-definition.json audit-mutated-claim-program.json; rc=$?; echo MUTATED_CONSTRUCTOR_CMP_EXIT=$rc; test $rc -eq 1` | wrapper 0; `cmp` 1 as expected |
| `body_mutation_kprove.log` | `kprove spec-body-mutation.k --definition audit-body-mutation-kompiled --spec-module PILE-BODY-MUTATION-SPEC; rc=$?; echo BODY_MUTATION_KPROVE_EXIT=$rc; test $rc -ne 0` | wrapper 0; `kprove` 1 as expected |
| `rule_inventory.log` | `python3 /audit-output/evidence/rule_inventory.py` | 0 |
| `vacuity_witness.log` | `python3 /audit-output/evidence/vacuity_witness.py` | 0 |
| `vacuity_kprove.log` | `kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module PILE-AUDIT-VACUITY-SPEC; rc=$?; echo VACUITY_MUTATION_KPROVE_EXIT=$rc; test $rc -ne 0` | wrapper 0; `kprove` 1 as expected |

Each logging wrapper was:

```bash
script -q -e -c '<exact command above>' /audit-output/evidence/<log>
```
