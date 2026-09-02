# Independent Lean/Klean audit

Stage `06-lean-audit` starts a fresh auditor after deterministic Stage 4. It
never uses the generating session and never receives `runner-state/`.

Run one eligible audit with:

```bash
docker/klean-audit/run_task.sh <run-id> <problem>
```

The following inputs are mounted read-only:

- the frozen Stage 1 K workspace;
- the selected Stage 2 K audit;
- the protected Stage 3 lemma-classification manifest;
- the selected deterministic Stage 4 Klean generation and trust inventory;
- the completed Stage 5 Lean workspace, only when a proof exists; and
- trusted preflight tooling and its toolchain lock.

The launcher resolves two exact modes:

- classification-only: Stage 4 is `KLEAN_NO_OBLIGATIONS`, Stage 5 is absent,
  and the fresh auditor must independently confirm a genuinely empty domain
  set;
- classification-plus-proof: Stage 4 is `PASS`, Stage 5 is successful, and
  the auditor validates both the classification and exact Lean proof.

`KLEAN_NO_OBLIGATIONS` still proceeds to Stage 6; it is not complete before
this independent classification-only verdict. In both modes, the auditor
reconstructs the Stage 1 simplification-rule inventory, reclassifies every
entry, recomputes provenance hashes, and checks the Stage 4 generation.

In both modes, the no-network, no-auth mechanical container reruns deterministic Klean preflight
against the frozen Stage 1 input, protected Stage 3 manifest, and selected
Stage 4 generation.
Classification-only confirms the no-obligation generation and receives no
proof candidate.
Proof mode additionally runs `lake clean` and `lake build` on a fresh copy of
the candidate, type-checks `Proof.final` against the exact generated target,
rejects proof holes and new trust escapes, and records
`#print axioms Proof.final`.

In proof mode, the fresh model auditor separately checks each
`target.parameters` operational bridge against the frozen K rules and
semantics; a clean build alone is insufficient. The mechanical container
cannot write the audit directory while candidate code is being elaborated;
its JSON result is published by the host afterward.

Each numbered execution preserves `audit-input.json`, metrics, logs, structured
trace, raw `evidence/`, `REVIEW.md`, and `verdict.json`. `PASS` and
`CONCERNS` are `LEGIT`; `FAIL` is `NOT_LEGIT`. Only infrastructure/model
`AUDIT_ERROR` permits another numbered audit. A mechanical failure forces
`FAIL`/`NOT_LEGIT`; mechanical infrastructure failure forces `AUDIT_ERROR`.
A `FAIL` is terminal.

The Stage 6 execution tree is safe to archive with the run. Authentication,
ephemeral auditor state, and generating `runner-state/` must not be archived.
No live model call is part of automated verification.
