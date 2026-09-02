---
name: k-proof-technique
description: 'Use when constructing a K reachability proof requires deriving a loop invariant, choosing a summary representation, laying out proof obligations, or abstracting an operation kprove cannot evaluate.'
---

## Scope & boundary

This skill is the **strategy** for a K reachability proof: how to derive a loop
invariant, why a summary must be solver-friendly, and what obligations the
proof has to discharge.

This skill does **not** run any tool. Machine-checking the proof — running `kprove`, reading a residual configuration, adding a `[simplification]` lemma, narrowing with `--depth N` — belongs to `proving-spec`.

This skill does **not** execute or document a proof run. It supplies the
reasoning scaffold that execution workflows consume.

---

## The scaffold

### Deriving the loop invariant

The loop invariant captures what is preserved at the loop head on every iteration. To derive it:

1. **Identify the postcondition.** For the entry claim it is the condition on the final state — e.g. `n == 0` and `s == sumTo(N0)`.

2. **Ask: what is true at the loop head that implies the postcondition when the loop exits?** The loop exits when the guard is false (`n == 0`). At that point the invariant must reduce to the postcondition.

3. **Parametrize by the mid-loop state.** Replace the initial values by symbolic variables `N` (remaining counter) and `S` (accumulated so far). The invariant is: "with `n |-> N` and `s |-> S` at the loop head, the loop ends with `n |-> 0` and `s |-> S + sumTo(N)`."

4. **Check the base case algebraically.** When `N == 0` the guard is false, the loop exits immediately, and the postcondition becomes `S == S + sumTo(0)`, i.e. `sumTo(0) == 0` — true by the definition of the summary function.

5. **Check the inductive case algebraically.** When `N > 0`, one iteration runs: `n` becomes `N - 1`, `s` becomes `S + N`. Applying the invariant to the new state gives `n |-> 0` and `s |-> (S + N) + sumTo(N - 1)`. The obligation is `(S + N) + sumTo(N - 1) == S + sumTo(N)`, which the chosen closed form reduces to solver-supported integer arithmetic in this example.

The invariant ties the running partial sum `S` and the remaining count `N` to the final postcondition through the summary function `sumTo`. The summary function belongs in `verification.k`, not in the spec module.

### Choose the summary representation

When an equivalent closed form exists in a theory the target solver can decide,
prefer it; for the sum example, `N*(N+1)/2` reduces the obligation to supported
integer arithmetic. If no faithful closed form exists, keep the recursive
definition—it may be the only exact specification of the result. Make its base
and step equations explicit, and use induction, folding, or summary lemmas so
the proof does not depend on unbounded evaluator unfolding. A recursive
equation can otherwise keep expanding while its symbolic guard remains
entailed; see
[symbolic-recursion debugging](../shared/kprove-debug-troubleshoot/symbolic-recursion.md).

### The three obligation shapes

Every loop-bearing K proof discharges three obligations:

1. **Base case** — the invariant holds when the loop guard is already false: the postcondition it claims must follow from doing nothing.
2. **Inductive case** — assuming the invariant at the loop head, one iteration of the loop body must re-establish it (or reach the postcondition, if the guard is now false).
3. **Whole-program discharge** — instantiating the loop-invariant claim at the point the entry claim first reaches the loop head must produce exactly the entry claim's postcondition.

A complete proof records how each obligation is discharged.

---

## Classify proof extensions before using them

Read the [proof-extension soundness contract](../shared/proof-extension-soundness.md)
before adding a proof-local function, equation, claim, or operational rewrite.
Classify it as a definitional summary, derived lemma, operational bridge, or
trusted primitive.

For each extension, complete the contract's **Proof-extension record**. In
particular, answer whether it replaces a term that fixed semantics would have
executed and enumerate the complete state footprint of that execution.

Program-defined code is not an external primitive. Either let fixed semantics
execute it or prove an auxiliary reachability claim connecting the exact body,
binding, arguments, environment, and state transition to the summary. A result
equation alone does not justify skipping lookup, control, or effects.

Before admitting any operational bridge, prove a bridge-free universal
connection theorem over its complete match domain. The theorem must not import
the proposed bridge; it must use fixed semantics and independently justified
theory to establish the exact binding, execution, value, control, and state
transition for every configuration the bridge accepts. Finite tests do not
satisfy this precondition.

Opacity is safe only when the proof is parametric in the primitive's value:
changing its interpretation must not establish a different source-level fact,
except through an explicit external contract. A fresh symbol that selects a
branch, result, or observable state is a result-bearing oracle, not a threaded
value. Reusing that symbol in both an operational bridge and postcondition is
circular unless a machine-checked theorem independently connects fixed
execution to its value.

Check every group of equations for guard coverage and overlap before using
`[total]` or `[simplification]`. Guards that overlap must produce equal results
on the overlap. Narrow false off-domain equations instead of relying on current
unreachability.

If Gate A rejects an extension, remove or disable it and inspect the
fixed-semantics residual in the same agent invocation. Prefer fixed-semantics
execution, then an exact auxiliary execution theorem, then a stronger invariant
or truthful definitional summary. Narrow the theorem honestly when that is the
sound result; terminal incomplete reporting is reserved for an evidenced hard
blocker, not for a proof strategy that is merely harder or slower. Repair that
requires redesign is not a hard blocker.

---

## Trusted-opaque primitives — isolating an external trust boundary

Use opacity only for a fixed operation intentionally outside the theorem and
outside the program-defined code being verified. Prove the surrounding structure
and state the value-level result conditionally on the primitive's contract.

One K-specific implementation uses a `[function, total]` wrapper with **no rule
that fires under `kprove`** plus a `[concrete]` rule that computes the real value
under `krun`:

```k
syntax Float ::= intFloatDiv(Int, Float) [function, total, no-evaluators]
rule intFloatDiv(I, F) => Int2Float(I, 53, 11) /Float F  [concrete]
```

- Under `kprove` the argument is symbolic, the `[concrete]` rule does not fire, and
  `intFloatDiv(I, F)` stays uninterpreted. The proof only *threads* that term — it never
  reasons about the float value — so what is verified is the surrounding shape (the map, the
  fold, the accumulator), position for position.
- Under `krun` the argument is ground, the `[concrete]` rule fires, and the smoke/differential
  test checks a real numeric answer (the LLVM backend has the float hooks).

**`[no-evaluators]` is metadata, not a switch.** It suppresses the LLVM "non-exhaustive match"
warning on an under-covered total function and documents intent; it disables nothing. Opacity
is an emergent property of the *rules*: no `kprove`-firing rule ⇒ opaque everywhere; a
`[simplification]` rule with a guard ⇒ unfolds only where the guard is entailed; a `[concrete]`
rule ⇒ krun computes it, kprove applies it only on ground arguments.

One consequence that bites:

- A `[concrete]` rule **still fires on ground arguments under `kprove`** and hits the missing
  hook — `subF(0.0, 1.0)` crashes just like `0.0 -Float 1.0`. Keep every argument symbolic and
  emit any needed constant as a **literal** (`-1.0`), never as a computed expression.

An opaque term may be threaded without proving its value. Differential testing
can support the primitive's concrete implementation, but it does not replace an
auxiliary theorem for program-defined code and does not establish a universal
value property.

---

## References

- [Proof-extension soundness contract](../shared/proof-extension-soundness.md) —
  classification, justification, and validation obligations for proof-local
  functions, equations, claims, and rewrites.
- [K functions, claims, and proof modules](../shared/k-claims.md) —
  `[function]`, `[simplification]`, and claim syntax.
- [Symbolic recursion](../shared/kprove-debug-troubleshoot/symbolic-recursion.md)
  — diagnosis when a helper keeps unfolding.
