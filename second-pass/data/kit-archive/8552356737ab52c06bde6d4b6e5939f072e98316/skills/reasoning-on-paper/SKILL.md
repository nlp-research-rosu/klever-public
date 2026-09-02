---
name: reasoning-on-paper
description: 'Use when the user explicitly requests an on-paper K proof, or live K tooling cannot be made available and the user accepts an unchecked fallback.'
---

## Output contract

Produce exactly three artifacts:

| Artifact | Purpose |
|---|---|
| `spec.k` | Schematic reachability claims |
| `verification.k` | Summary functions and proof-specific lemmas |
| `REASONING.md` | Primary evidence: the natural-language symbolic trace |

Mark all three `UNCHECKED` and state that no K tool accepted them. Do not create
`semantics.k`. If an existing semantics is supplied, the drafts may target it;
otherwise record the assumed configuration and transition behavior in
`REASONING.md` instead of inventing a language definition.

Do not write `PROOF.md`, report `#Top`, or claim verification or validation.

## Derive the claims

Use `k-proof-technique` to derive the invariant, summary function, and
base/inductive/whole-program obligations.

Draft `spec.k` and `verification.k` as honestly as the available syntax permits:

- Begin each file with an `UNCHECKED` comment.
- Do not fabricate successful imports, tool output, or compilation status.
- If required syntax or cells are unknown, state the assumption in a comment
  and in `REASONING.md`.
- Keep the claims aligned with the source program and the user's stated intent.

## Write `REASONING.md`

Use this structure:

```markdown
# UNCHECKED on-paper reasoning

## Property
[Precondition, termination caveat, and postcondition in plain language.]

## Execution assumptions
[State representation and source-level transition assumptions. No semantics file was generated.]

## Invariant and summary
[Invariant, summary definition, domain, and why they imply the postcondition.]

## Symbolic trace
| Obligation | Starting state | Guard/rewrite steps | Claim or lemma applied | Residual condition | Status |
|---|---|---|---|---|---|
| Base | ... | ... | ... | ... | met / unmet / unknown |
| Inductive | ... | ... | ... | ... | met / unmet / unknown |
| Whole program | ... | ... | ... | ... | met / unmet / unknown |

## Undischarged obligations
[Every assumption, missing rule, solver-dependent fact, or unknown.]

## Conclusion
[What the trace supports, explicitly not machine verified.]
```

Trace like a prover:

1. Write the complete symbolic starting state for each obligation.
2. Split on the relevant guard or path condition.
3. Apply one source transition at a time and show substitutions explicitly.
4. State exactly where the invariant claim or lemma would apply.
5. Reduce the remaining condition algebraically.
6. Mark the obligation `met`, `unmet`, or `unknown`; never turn an assumption
   into a proved fact.

The natural-language trace is the main deliverable. The two K files record the
formal shape that a future live run should check.

## Reference

- [`k-proof-technique`](../k-proof-technique/SKILL.md) — invariant, summary, and
  obligation derivation
- [K functions and claims](../shared/k-claims.md) — syntax for the two K
  drafts
