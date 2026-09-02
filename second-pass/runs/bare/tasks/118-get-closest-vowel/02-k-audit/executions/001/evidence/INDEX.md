# Audit evidence index

All commands were executed against source-only copies under
`/tmp/audit-work`. Each `.log` begins with its working directory and
shell-escaped command and ends with `EXIT_STATUS`.

- `00-tool-versions.log`: Python, K, and Java versions.
- `01-*`: mount/type/hash integrity and bounded summaries of untrusted
  generation metadata, text log signals, and JSONL trace.
- `02-translate.log`, `02-mpy-byte-identity.log`,
  `02-program-pinning.log`: trusted translation and exact embedded-program
  identity.
- `differential_test.py`, `02-differential-inputs.json`,
  `02-differential.log`: 23,766-input bounded differential with zero
  mismatches.
- `long_input_boundary.py`, `02-long-input-boundary.log`: expected nonzero
  audit probe exposing three `RecursionError` divergences.
- `03-kompile-*.log`: fresh LLVM and Haskell builds.
- `k_semantics_differential.py`, `03-k-semantics-inputs.json`,
  `03-k-semantics-differential.log`: 22 concrete K/Python comparisons.
- `k_long_boundary.py`, `03-k-long-boundary.log`: expected nonzero audit probe
  showing K/Python divergence at 1000 characters.
- `03-kprove-all.log`: original aggregate positive proof, `#Top`, exit 0.
- `03-spec-labeled.k`, `03-kprove-labeled-all-serial.log`, and
  `03-kprove-case-*-serial.log`: unchanged labeled aggregate and serial
  claim-target diagnostics, all `#Top`/exit 0. Non-`serial` logs preserve a
  discarded over-parallelized/OOM diagnostic attempt.
- `claim_witnesses.py`, `04-claim-witnesses.log`: satisfying ground state for
  every claim shape and both-Python comparisons.
- `05-rule-inventory.log`: mechanical declaration/rule/claim inventory.
- `05-body-mutation-*`: reviewer body-sensitivity mutation, trusted
  translation/pinning/build, Python result, false K result, and unchanged
  `#Top`.
- `06-spec-vacuity.k`, `06-vacuity-dry-run.log`,
  `06-vacuity-kprove.log`: fresh false postcondition; successful dry build and
  expected stuck proof failure.
- `run_with_status.sh`: common exact-command/status logger.
