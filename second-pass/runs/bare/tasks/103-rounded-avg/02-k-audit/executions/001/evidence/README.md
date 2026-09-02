# Audit evidence index

All candidate execution used the source-only scratch copy at
`/tmp/audit-work/103-rounded-avg/candidate-src`. Candidate-provided compiled
definitions were not used.

## Reviewer-authored scripts and analyses

- `stage1_inventory.sh` — mount, file type, hash, provenance, and toolchain scan.
- `trace_summary.py` — bounded extraction of readable claims and commands from
  the untrusted generation trace and `codex-output.log`.
- `differential_test.py` — trusted-canonical versus generated-Python
  differential test; its exact inputs are in `differential-inputs.json`.
- `concrete_semantics_compare.py` — fresh `krun` versus both Python
  implementations, including binary64 precision and overflow witnesses.
- `stage3_rebuild_and_prove.sh` — fresh LLVM/Haskell builds and eleven
  independently selected positive claims.
- `claim_witnesses.py` — realizable states for every candidate claim and the
  universal integral-case counterexample.
- `rule-inventory.md` — exhaustive local syntax/function/rule inventory and
  rule-by-rule judgment.

## Main command logs

- `logs/01-stage1-inventory.log`
- `logs/02-untrusted-trace-summary.log`
- `logs/03-translation-and-differential.log`
- `logs/04-build-concrete-llvm.log`
- `logs/05-build-proof-haskell.log`
- `logs/06-concrete-semantics-compare.log`
- `logs/07-proof-*.log` (one for each of eleven positive claims)
- `logs/08-proof-all-claims.log`
- `logs/09-program-pinning.log`
- `logs/10-claim-witnesses.log`
- `logs/11-vacuity-dry-run.log`
- `logs/12-vacuity-expected-failure.log`
- `logs/13-static-declaration-scan.log`

The `03a`, `06a`, `09a`, and `12a` logs preserve reviewer harness mistakes
described in `REVIEW.md`; they are not candidate-failure evidence. The `06b`
log preserves the successful result parser run before the overflow case was
added.

## Preserved generated artifacts

- `artifacts/roundedAvgProgram-rhs.kterm` and
  `artifacts/roundedAvgProgram-rhs-surface.kterm`
- `artifacts/submitted-solution.kore` and
  `artifacts/roundedAvgProgram-rhs.kore`
- `artifacts/spec-vacuity-audit.k`
