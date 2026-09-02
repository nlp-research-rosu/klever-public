---
name: writing-spec
description: 'Use when you have code and its K semantics and need to state what to prove in spec.k. Triggered by "write a spec for this program", "what should the preconditions be", "turn my postcondition into a K claim", or "draft spec.k".'
---

## Before writing: check `semantics.k`

`spec.k` imports and compiles against `semantics.k`. Confirm its status first:

| State | Action |
|---|---|
| `semantics.k` exists and compiles | Proceed with this skill |
| `semantics.k` exists but not yet smoke-tested | Proceed; note that spec errors may trace back to semantics bugs |
| `semantics.k` does not exist | Use `writing-semantics` first, then return here |

Also confirm that concrete program identifiers used by the claims parse as
identifiers rather than K rule variables. See
[K syntax and operational semantics](../shared/k-syntax.md#grammar).

---

## What a spec is

A K spec states **partial correctness**: *if* the program terminates and the precondition holds, then the postcondition holds at termination. It says nothing about whether the program terminates; that is a separate liveness question.

Keep three activities distinct (see `using-kit`): **Verification** closes
reachability claims under the supplied theory; **Soundness audit** checks proof
extensions; and **Validation** checks theorem scope and evidence against the
intended property.

---

## Record the validation scope

Before drafting claims, record four items that validating-proof will check:

| Item | Record |
|---|---|
| Program boundary | Exact entry computation and program-defined operations included in the theorem |
| Input domain | Types, guards, well-formedness conditions, and excluded inputs |
| Observable final state | Result and every state cell the intended property observes |
| Intended property | Plain-language result expected after termination |

The spec may frame cells that are intentionally irrelevant, but the scope record
must say why they are unobserved. Do not silently omit a cell whose change is
part of the intended behavior.

When the task requires the full source contract, the required entry claim or
claims must collectively cover that contract's input domain. Do not replace an
unbounded or symbolic domain with finitely many concrete sizes, examples, or
bounded unrollings. Such claims may be kept as diagnostic progress, but they are
not the required target theorem unless the source contract states the same
bound.

---

## Pre- and postconditions

Conditions are constraints on cell contents, written as `requires` and `ensures` clauses on a `claim`:

- **`requires`** — the precondition: a Boolean expression over the LHS cell values. The claim is only attempted when this holds.
- **`ensures`** — the postcondition: a Boolean expression over the RHS cell values. May introduce existential variables written `?X` (e.g. `ensures ?R ==Int sumTo(N0)`). Any RHS variable not bound on the LHS must use `?`; omitting it is a hard K error.

Preconditions and postconditions are constraints on the full K configuration (the `<k>` cell and every state cell) before and after the rewrite — not just function inputs/outputs in the ordinary sense.

**Programs that produce a return value** — use `ensures` to constrain it. Example shape for a claim where the computation leaves a result `?R` in `<k>`:

```k
claim [my-prog]:
      <k> myProgram(N0:Int) => ?R:Int </k>
      <state> S </state>
  requires N0 >=Int 0
  ensures  ?R ==Int sumTo(N0)
```

**Programs that terminate with a state** (no return value) — express the postcondition as the RHS of the state cells directly, without `ensures`:

```k
<state> .Map => n |-> 0 s |-> sumTo(N0) </state>
```

---

## The two claims in `spec.k`

A complete spec contains one **entry claim** for the whole program plus one **loop-invariant claim per loop**. The single-loop program used throughout this kit therefore has exactly two claims; a program with two loops needs three, and a nested loop needs its own invariant claim, which the outer loop's proof then uses to step over the inner loop.

### 1. Entry (whole-program) claim

States what the full program does from its initial configuration to termination.

```k
claim [sum-prog]:
      <k> n = N0:Int ; s = 0 ;
          while (n > 0) { s = s + n ; n = n - 1 ; } => .K ...</k>
      <state> .Map => n |-> 0 s |-> sumTo(N0) </state>
  requires N0 >=Int 0
```

- LHS: the full program text in `<k>`; initial state (`.Map` = empty).
- RHS: `.K` in `<k>` means all computation is done; the final state maps are the postcondition.
- `...` in `<k>` is a frame variable for the rest of the continuation.
- The state uses a closed map (no `...`) when exactly those keys must be present.

### 2. Loop-invariant (circularity) claim

States what the loop does at the loop head, given symbolic accumulator values. This is the coinductive hypothesis — kprove uses the claim to discharge the loop by applying it to itself.

```k
claim [loop-inv]:
      <k> while (n > 0) { s = s + n ; n = n - 1 ; } => .K ...</k>
      <state> n |-> (N:Int => 0)
              s |-> (S:Int => S +Int sumTo(N)) </state>
  requires N >=Int 0
```

- Starting at the loop head with `n |-> N` and `s |-> S` (both symbolic), `N >= 0`.
- The loop terminates with `n |-> 0` and `s |-> S + sumTo(N)`.
- The `=>` inside each cell maps old to new: `N:Int => 0` means `n` starts at `N` and ends at `0`.

Both claims live in a single spec module that only contains `claim`s (and optionally `[simplification]` rules). Plain `rule` statements in a spec module are a K compiler error.

```k
requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]: ...
  claim [sum-prog]: ...
endmodule
```

---

## The loop invariant

The loop invariant ties the running accumulator (`s`) and the remaining count (`n`) to the postcondition through a summary function (e.g. `sumTo`), parametrized by the mid-loop state so it covers every iteration, not just the initial call.

For the step-by-step derivation method and how to choose between a
solver-friendly closed form and a necessary recursive definition, see
[`k-proof-technique`](../k-proof-technique/SKILL.md).

---

## Adequacy hand-off

Once the spec is drafted, `proving-spec` owns verification, while
`validating-proof` owns the independent soundness audit and validation. Under
the shared
[proof-extension soundness contract](../shared/proof-extension-soundness.md),
`validating-proof` applies the Gate A/B/C audit. Do not duplicate those checks
here.

Machine-check the spec structure with a focused `kprove` attempt even before
the proof is expected to close. Early parser and module errors are cheaper to
fix before adding lemmas.

---

## References

- [K functions, claims, and proof modules](../shared/k-claims.md) — claim
  syntax, `requires`/`ensures`, labels, and proof-module restrictions.
- `proving-spec` — next step: add `verification.k` (summary function + kompiled definition) and make the claims pass `kprove`.
- `validating-proof` — independently audits proof-extension soundness and
  validates intent, trust, and evidence for a passing proof.
