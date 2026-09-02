# Reviewer command index

All K commands ran in `/tmp/audit-work/fresh` against source copied from the
trusted mounts and candidate source files. No candidate-provided kompiled
directory was copied or referenced. Each linked `.log` is a `script(1)`
transcript whose header records the command and whose footer records
`COMMAND_EXIT_CODE`.

| Purpose | Exact command | Exit | Transcript |
|---|---|---:|---|
| Provenance and recursive integrity | `python3 /audit-output/evidence/provenance_check.py` | 0 | `provenance.log` |
| Tool versions | `kompile --version && kprove --version && krun --version` | 0 | `tool-versions.log` |
| Trusted regeneration | `python3 py2mpy.py solution.py \| cmp solution.mpy -` | 0 | `translator-identity-valid.log` |
| Independent differential | `PYTHONDONTWRITEBYTECODE=1 python3 /audit-output/evidence/differential.py` | 0 | `differential.log` |
| Concrete build | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | 0 | `build-runtime.log` |
| Concrete execution | `python3 py2mpy.py /audit-output/evidence/concrete_harness.py > reviewer-concrete.mpy && krun reviewer-concrete.mpy --definition runtime-kompiled` | 0 | `concrete-execution.log` |
| Harness body identity | `python3 /audit-output/evidence/check_harness_body.py` | 0 | `concrete-harness-body.log` |
| Bridge-free proof build | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | 0 | `build-verification.log` |
| Universal loop proof | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.loop` | 0, `#Top` | `prove-loop.log` |
| Bridge-enabled proof build | `kompile verification-with-loop.k --backend haskell --main-module VERIFICATION-WITH-LOOP --syntax-module MPY-SYNTAX --output-definition verification-with-loop-kompiled` | 0 | `build-verification-with-loop.log` |
| Whole-program proof | `kprove spec.k --definition verification-with-loop-kompiled --spec-module SPEC --claims SPEC.correct-bracketing` | 0, `#Top` | `prove-entry.log` |
| Parsed program-term identity | `python3 /audit-output/evidence/extract_claim_program.py \| sed "s/\\.Stmts//g" > claim-entry-program.mpy && kast solution.mpy --definition verification-kompiled --output kore --output-file solution.kore && kast claim-entry-program.mpy --definition verification-kompiled --output kore --output-file claim-entry.kore && cmp solution.kore claim-entry.kore && sha256sum solution.kore claim-entry.kore` | 0 | `program-term-pinning-valid.log` |
| Loop claim/bridge identity | `python3 /audit-output/evidence/compare_loop_bridge.py` | 0 | `loop-bridge-identity.log` |
| Continuation containment | `krun reviewer-context.mpy --definition runtime-kompiled --output pretty --color off > fixed-context.pretty && krun reviewer-context.mpy --definition verification-with-loop-kompiled --output pretty --color off > bridge-context.pretty && cmp fixed-context.pretty bridge-context.pretty && sha256sum fixed-context.pretty bridge-context.pretty && grep -F "\"context_result\" \|-> false" fixed-context.pretty` | 0 | `context-containment-valid2.log` |
| Exhaustive K inventory | `python3 /audit-output/evidence/inventory_k.py` | 0 | `k-rule-inventory.log` |
| Fresh false postcondition | `kprove audit-spec-vacuity.k --definition verification-with-loop-kompiled --spec-module AUDIT-SPEC-VACUITY` | 1, expected stuck `true` | `non-vacuity.log` |
| Body sensitivity | `kprove audit-body-sensitivity.k --definition verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY` | 1, expected stuck `false` | `body-sensitivity.log` |
| Fixed pair opposite | `kprove audit-spec-vacuity.k --definition verification-kompiled --spec-module AUDIT-SPEC-VACUITY` | 1, expected stuck `true` | `fixed-pair-opposite.log` |
| Bridge open opposite | `kprove audit-open-opposite.k --definition verification-with-loop-kompiled --spec-module AUDIT-OPEN-OPPOSITE` | 1, expected stuck `false` | `opposite-false-value.log` |
| Fixed open opposite | `kprove audit-open-opposite.k --definition verification-kompiled --spec-module AUDIT-OPEN-OPPOSITE` | 1, expected stuck `false` | `fixed-open-opposite.log` |

Three retained diagnostic transcripts are not audit failures:

- `translator-identity.log` used process substitution under `script(1)`'s
  `/bin/sh` and exited 2 before translation; the portable pipe command above
  replaced it.
- `program-term-pinning.log` tried to parse proof-only explicit `.Stmts` as
  surface program syntax and exited 113. Removing only those explicit empty-list
  spellings yielded identical parsed KORE hashes in the valid transcript.
- `context-containment.log` compared backend-specific raw KORE serialization;
  semantic terms agreed but formatting and map order differed. The valid
  pretty/sorted comparison above is byte-identical.
