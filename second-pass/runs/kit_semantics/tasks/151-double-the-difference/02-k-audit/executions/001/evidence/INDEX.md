# Audit evidence index

All proof builds and runs used fresh definitions below
`/tmp/audit-work/candidate-src`; no candidate-provided kompiled directory was
used. K version was 7.1.293.

## Stage 1

- `python3 /audit-output/evidence/provenance_check.py`
  - Exit 0; `01-provenance.log`.
- `python3 /audit-output/evidence/trace_inventory.py`
  - Exit 0 after parsing all 540 JSONL records; `01-trace-inventory.log`.

## Stage 2

- `python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py >
  /tmp/audit-work/candidate-src/solution.regenerated.mpy`
- `cmp -s /tmp/audit-work/candidate-src/solution.regenerated.mpy
  /tmp/audit-work/candidate-src/solution.mpy`
  - Exit 0, byte identity; `02-regeneration.log`.
- `python3 /audit-output/evidence/differential_test.py`
  - Exit 0; 2,517 contract cases, zero candidate/contract mismatches;
    `02-differential.log`.

## Stage 3

- `kompile --backend llvm reference-semantics/semantics.k --main-module
  MPY-KRUN --syntax-module MPY-SYNTAX --output-definition
  audit-runtime-kompiled`
  - Exit 0; `03-kompile-llvm.log`.
- `kompile --backend haskell verification.k --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  audit-verification-kompiled`
  - Exit 0; `03-kompile-haskell.log`.
- `krun audit-concrete.mpy --definition audit-runtime-kompiled`
- `krun audit-model-bool.mpy --definition audit-runtime-kompiled`
  - Both exit 0 with `.K`, `NoExc`, and exit code 0;
    `03-concrete-execution.log`.
- `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
  --claims SPEC.loop-invariant`
  - Exit 0 and `#Top`; `03-kprove-loop-invariant.log`.
- `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC`
  - Exit 0 and `#Top`; `03-kprove-all.log`.
- Diagnostic only: selecting `SPEC.double-the-difference` alone removes its
  auxiliary circularity and was interrupted after about 30 seconds (exit 130);
  `03-kprove-target.log`. It is not the authored target proof unit; the
  all-claims command above proves the entry claim with its circularity.

## Stage 4

- Two `kast ... --expand-macros --output kore` commands, followed by `cmp -s`,
  mechanically compared the regenerated source module with a module using the
  proof macro.
  - Both KORE hashes were
    `fed72e387cf57cf206f9dad4c410f9293a71cccc89f0d4c1dd64ec6c7949593d`;
    `04-constructor-identity.log`.
- `kprove witness-values.k --definition audit-verification-kompiled
  --spec-module WITNESS-VALUES`
- `python3 /audit-output/evidence/witness_compare.py`
  - Exit 0 and `#Top`; `04-witnesses-config.log`.
- Fresh inline body sensitivity:
  - `kprove audit-body-mutation.k --definition audit-verification-kompiled
    --spec-module AUDIT-BODY-MUTATION --dry-run` exited 0.
  - The same command without `--dry-run` exited 1 with execution result 2
    versus required 1; the enclosing audit check exited 0;
    `04-body-sensitivity-inline.log`.
- Superseded diagnostics are retained:
  `04-witnesses.log` used unsupported pure functional claims, and
  `04-body-sensitivity.log` attempted forbidden proof-module syntax. Neither
  is cited as positive evidence.

## Stage 5

- `python3 /audit-output/evidence/rule_inventory.py >
  /audit-output/evidence/05-rule-inventory.tsv`
  - Exit 0; inventory totals are in `05-rule-inventory-summary.log`.
- `kompile --backend haskell fixed-only.k --main-module FIXED-ONLY
  --syntax-module MPY-SYNTAX --output-definition fixed-only-kompiled`
  - Exit 0; `05-fixed-connection-build.log`.
- `kprove fixed-connection-spec.k --definition fixed-only-kompiled
  --spec-module FIXED-CONNECTION-SPEC`
  - The original four static Int connection claims exited 0 with `#Top`;
    `05-fixed-connection-proof.log`.
  - A later stronger abstract-`Val` version exited 1 because the fixed backend
    did not derive the required sort case split; `05-fixed-connection-dynamic.log`.
    This is retained as an evidence gap, not a counterexample.
- `kprove projection-opposite.k --definition audit-verification-kompiled
  --spec-module PROJECTION-OPPOSITE --dry-run`
  - Exit 0.
- The same command without `--dry-run`
  - Exit 1 with stuck value 3 versus required 4; the enclosing audit check
    exited 0; `05-projection-opposite.log`.

## Stage 6

- `kprove audit-spec-vacuity.k --definition audit-verification-kompiled
  --spec-module AUDIT-SPEC-VACUITY --dry-run`
  - Exit 0.
- The same command without `--dry-run`
  - Exit 1 with `WarnStuckClaimState` and the unmet equality
    `dtd(VS) +Int 1 #Equals dtd(VS)`; the enclosing audit check exited 0;
    `06-fresh-vacuity.log`.
