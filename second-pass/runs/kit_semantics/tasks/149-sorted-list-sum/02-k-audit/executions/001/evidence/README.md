# Reviewer evidence index

All commands were run against reviewer-created sources and definitions under
`/tmp/audit-work/149-sorted-list-sum`. Candidate-provided compiled definitions
and caches were not copied or used. Each `stage*.log` contains the exact command,
bounded relevant output, and a recorded exit status unless noted below.

- Stage 1: `provenance_check.py`, `stage1-provenance.log`, and
  `stage1-tool-versions.log`.
- Stage 2: `differential_test.py`, `stage2-regeneration.log`, and
  `stage2-differential.log`.
- Stage 3: `reviewer_smoke.py`, translation/build/concrete-execution logs,
  `stage3-kprove-filter-loop.log`, and `stage3-kprove-all.log`.
- Stage 4: `ground_claim_witness.py`, constructor pinning, and the body mutation
  dry-run/proof logs.
- Stage 5: `k_rule_inventory.py` and its exhaustive statement inventory,
  `k_differential_test.py`, and the fixed-semantics definedness checks.
- Stage 6: `reviewer-false-spec.k` and its successful dry-run / expected failing
  proof logs.

`stage3-kprove-sorted-list-sum.log` is a diagnostic, not a required positive
target. It records an interactive attempt to select only the entry claim, which
also removes the separately labelled loop claim from the circularity set. The
backend continued actively unrolling until the reviewer interrupted it; the
interactive tool call reported exit 130, but the PTY transcript did not append
an exit marker. No conclusion relies on this run. The intended full invocation,
which supplies both claims, returned `#Top` and status 0 in
`stage3-kprove-all.log`; the helper claim also independently returned `#Top` and
status 0.

The first fixed-only definedness formulation in
`stage5-definedness-direct-backend-error.log` exited 113 during backend
verification, before executing a claim. The alternate existential formulation
in `stage5-definedness-trivial-formulation.log` was vacuous and is not used.
The final constructor-level fixed-semantics connection is the claim and result
recorded in `definedness-spec.k` and
`stage5-kprove-definedness-connection.log`.
