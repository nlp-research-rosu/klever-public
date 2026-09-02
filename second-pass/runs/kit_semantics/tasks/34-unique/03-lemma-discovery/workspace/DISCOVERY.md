# Trust-boundary discovery

The canonical inventory hash is
`36c8f6930fe11a0ef65a3e4475e90f089611977614efad399cb53f17c8cfdc3d`.
All 11 canonical rules are classified exactly once and remain in canonical
inventory order in `trust-boundary.json`.

## Classification summary

| Classification | Count | Canonical rules |
|---|---:|---|
| `DEFINITION` | 9 | The three `memberVS` equations, two `appendUnique` equations, two `dedupFromVS` equations, and two `lastFromVS` equations |
| `OPERATIONAL_RULE` | 0 | None |
| `PROVED_DERIVED_LEMMA` | 2 | The staged `#memberAcc` summary rule and exact source-loop summary rule |
| `DOMAIN_LEMMA` | 0 | None |

The two rules carrying `simplification` are the unequal-head and equal-head
equations of the total `memberVS` function. They are guarded defining cases,
not extra mathematical facts, so both are classified `DEFINITION`.

The remaining seven `VERIFICATION-BASE` rules are also equations or structural
recurrences:

- `memberVS(_, .ValSeq) => false` supplies the empty membership case.
- `appendUnique` names the complementary present/absent accumulator cases.
- `dedupFromVS` is the empty/cons recurrence for first-seen deduplication.
- `lastFromVS` is the empty/cons recurrence for the value retained in the
  source loop target.

No canonical rule is classified `OPERATIONAL_RULE`. Although the final two
rules rewrite operational configurations, the Stage 1 evidence satisfies the
stricter `PROVED_DERIVED_LEMMA` definition: each exact reusable rewrite is
proved first against a compiled module that omits that rule.

## Separately proved derived lemmas

### Membership summary

Canonical rule:
`rule-968e632bd6cc05aaec79ddccf4d7456c3677f8bed85ef5841369f17a2d47bea3`.

The rule rewrites:

```k
<k> #memberAcc(V, list(VS)) => memberVS(V, VS) ... </k>
```

Stage 1 establishes the same reachability statement in
`MEMBER-SPEC.member-summary` at `spec.k:8`. The ordering evidence is explicit
in `prove.sh`:

1. Lines 19–22 compile `verification.k` with main module
   `VERIFICATION-BASE`.
2. Lines 23–25 prove `MEMBER-SPEC` against
   `verification-base-kompiled`.
3. Only the later Stage 2 compilation selects `VERIFICATION-MEMBER`, the module
   containing the priority-40 rule.

`VERIFICATION-BASE` imports `MPY` and does not import
`VERIFICATION-MEMBER`, so the proof definition does not contain the rule being
established. The first staged `kprove` result is `#Top` in `prove.log`.

### Exact source-loop summary

Canonical rule:
`rule-e2565529bcc6542c53c8abedee1129bc7ea40552bde63262b79144f437ec36ac`.

The rule summarizes the exact generated loop body while preserving an
arbitrary continuation, updating only the local `x` binding through
`lastFromVS` and heap entry 1 through `dedupFromVS`.

Stage 1 establishes the identical configuration transition in
`LOOP-SPEC.unique-loop` at `spec.k:18`. The staged ordering in `prove.sh` is:

1. Lines 28–31 compile main module `VERIFICATION-MEMBER`.
2. Lines 32–34 prove `LOOP-SPEC` against
   `verification-member-kompiled`.
3. Lines 37–40 compile main module `VERIFICATION`, which is the first compiled
   closure containing the priority-40 loop rule.

`VERIFICATION-MEMBER` imports the previously justified membership bridge but
does not import `VERIFICATION`, so it does not contain the loop rule being
proved. The second staged `kprove` result is `#Top` in `prove.log`.

## Domain-lemma set

The domain-lemma set is empty. None of the 11 canonical rules introduces an
additional unproved mathematical fact: nine are defining equations and two are
reusable operational summaries backed by prior, rule-free Stage 1 reachability
proofs.
