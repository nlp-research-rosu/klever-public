# Reviewer evidence index

All commands were executed against source-only copies below
`/tmp/audit-work`. `run_logged.sh` records the working directory, shell-escaped
command, bounded output, and exit status in each numbered log.

- `01`: provenance, real-file checks, recorded file digests, campaign equality,
  and pipeline-native candidate/trace tree digests.
- `02`–`03`: trusted translation byte identity and independent Python
  differential testing.
- `04`–`08`: toolchain, fresh LLVM/Haskell builds, concrete generated-semantics
  comparisons, and the complete positive proof.
- `09`–`13`: isolated positive claims. The universal entry claim in `10` carries
  only its exact loop-invariant companion; `11` proves that invariant alone.
- `14`–`15`: constructor-level program pinning and a result-changing body
  mutation. `15` is an expected semantic failure.
- `16`: exhaustive source declaration/rule scan.
- `17`–`18`: false-postcondition parse/build success and expected semantic
  failure.
- `19`–`20`: opposite summary interpretation build success and expected proof
  rejection.

Expected nonzero statuses are `15`, `18`, and `20`; their logs contain
`WarnStuckClaimState` with the relevant false result. Every positive build,
execution, and proof log exits zero.
