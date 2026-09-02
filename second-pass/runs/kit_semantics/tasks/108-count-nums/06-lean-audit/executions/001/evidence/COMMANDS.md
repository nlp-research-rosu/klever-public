# Audit command index

All mounted inputs were treated as read-only evidence. Audit-authored scripts,
copies, and auxiliary Lean files were written only below `/audit-output` or
`/tmp/audit-work`.

## Integrity and Stage 3

`01-integrity-command.log` records:

```sh
AUDIT_MODE="$AUDIT_MODE" PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_integrity.py
```

This hashes the two producer files, authenticates their source manifest and
image binding, checks the Stage 1 per-file/tree hashes, invokes the trusted
rule-inventory implementation, and performs the ordered bijection comparison.

`11-classification-obligation-command.log` records:

```sh
python3 \
  /audit-output/evidence/independent_classification_and_obligations.py
```

The complete 29-row independent classification and five-row mathematical
obligation assessment are in
`classification-and-obligation-judgment.json`.

## Stage 4 preflight

The first command exposed the audit image's incomplete Lean launcher:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_preflight.py
```

Its failure is preserved in `02-preflight-command.log` and
`preflight-initial-failed-lake-clean.log`. The exact locked Lean 4.22
`Lean.Shell` frontend was then invoked from the mounted `libleanshared`;
the launcher source, hashes, and version evidence are in
`lean_shell_wrapper.c` and `14-toolchain-recovery.log`.

The successful required rerun was:

```sh
PATH=/tmp/audit-work/lake-home/.lake/build/bin:$PATH \
LEAN_FIXED_PREFIX=/tmp/audit-work/lean-fixed-root \
LEAN_SYSROOT=/tmp/audit-work/lean-fixed-root \
LAKE_OVERRIDE_LEAN=true \
LAKE_HOME=/tmp/audit-work/lake-home \
ELAN= \
PYTHONPATH=/reference \
python3 /audit-output/evidence/run_preflight.py
```

Complete output is in `02b-preflight-command.log`,
`preflight-01-lake-clean.log`, and `preflight-02-lake-build.log`; the exact
returned object is `preflight-returned-evidence.json`.

## Fresh Stage 5 project

The project path is recorded in `fresh-proof-workspace.txt`. It was populated
with:

```sh
cp -a /candidate/. /tmp/audit-work/stage5-audit.bWjLhR/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/stage5-audit.bWjLhR/Base/
```

The same recovered-toolchain environment shown above was used for:

```sh
(cd /tmp/audit-work/stage5-audit.bWjLhR/Base && lake clean)
(cd /tmp/audit-work/stage5-audit.bWjLhR && lake clean)
(cd /tmp/audit-work/stage5-audit.bWjLhR && lake build)
(cd /tmp/audit-work/stage5-audit.bWjLhR &&
  lake env lean Axioms.lean)
(cd /tmp/audit-work/stage5-audit.bWjLhR &&
  lake env lean OperationalAudit.lean)
```

The full results are `04-base-lake-clean.log`,
`05-proof-lake-clean.log`, `06-proof-lake-build.log`,
`07-print-axioms-Proof.final.log`, and
`09-operational-adversarial-tests.log`.

The trusted mechanical final gate was also rerun:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_final_gate.py
```

Its three complete command logs are named `final-gate-*.log` and its returned
object is `final-gate-returned-evidence.json`.

`10-proof-integrity-command.log` and `proof-integrity.json` record the
candidate/generation tree hashes, exact target extraction, candidate token
scan, per-parameter declaration counts, and exact `Proof.final` statement
comparison.

`12-operational-bridge-command.log`,
`operational-bridge-judgment.json`, and `OperationalAudit.lean` record the
13 per-binding operational comparisons, adversarial inputs, and convenient
counterfactual definitions.

`13-source-excerpts.log` contains line-numbered frozen `verification.k`,
`solution.py`, relevant supplied operational semantics, `prove.sh`, and the
candidate `Proof.lean`.
