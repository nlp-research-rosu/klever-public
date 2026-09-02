# Evidence notes

Authoritative audit evidence is in the logs and reviewer-authored artifacts in
this directory. Each normal command log begins with `COMMAND:` and ends with
`EXIT_STATUS:`.

The following early diagnostic logs are superseded and are not used:

- `campaign-and-trace-check.log`: `jq` was unavailable; the composite shell
  continued. `provenance-structural-check.log` is the corrected structural
  check and parses every JSON/JSONL record with Python's standard library.
- `constructor-pinning-check.log` and
  `constructor-pinning-check-corrected.log`: the first did not normalize the
  `.Stmts` syntax macro and the second removed a line containing closing
  parentheses. `constructor-pinning-check-final.log` is the fail-fast,
  successful constructor comparison.
- `kprove-dispatch-mutant.log`: a one-statement mutant simplified past the
  intended intermediate destination. `kprove-dispatch-mutant2.log` uses a
  structurally observable multi-statement wrong body and is the valid
  dispatch-shape limitation test.
- `kprove-body-sensitivity.log`: the first reviewer-authored mutation contained
  a parser typo. `kprove-body-sensitivity-corrected.log` is the corrected,
  meaningful body-sensitivity run.

The following supplemental experiments were intentionally interrupted or
otherwise non-diagnostic and are not
candidate failures:

- Isolated `loop-init-cons` was stopped with status 130 after it lost the
  mutually supporting loop circularities. The exact submitted five-claim
  group subsequently closed with `#Top`.
- `omitted-entry-nonempty` was stopped with status 130 after 120 seconds
  without output. It is a reviewer-authored theorem absent from the candidate;
  the unresolved experiment is not credited to or charged against the
  candidate.
- `spec-combined-entry.k` mechanically copies every original candidate claim
  into one module and adds only the omitted nonempty entry result. Its prover
  remained CPU-active without `#Top` or a residual for about seven minutes and
  was stopped with status 130. This unsubmitted obligation is likewise not a
  candidate timeout failure; it shows that the composition was not
  independently packaged as one quickly reconstructed prover run.
- `spec-prefix-connection.k` was a reviewer attempt to expose only the
  deterministic prefix before the loop. The backend continued through the
  reachable loop and correctly produced a terminal string instead of the
  deliberately intermediate target, so `kprove-prefix-connection.log` is not a
  candidate proof failure or a valid negative test.

The corrected bounded connection check is `spec-prefix-steps.k`. Its four
finite claims isolate parameter binding, both initial assignments, and
represented-list `For` lowering; `kprove-prefix-steps.log` records their
combined `#Top`.
