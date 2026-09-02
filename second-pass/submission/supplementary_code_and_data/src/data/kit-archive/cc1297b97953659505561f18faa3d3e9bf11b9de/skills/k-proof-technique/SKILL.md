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

## Dynamic-to-static sort refinement — guarded total projections

Symptom: iteration or dispatch over a heterogeneous dynamic supersort yields a
symbolic `V:Super`, while the semantics' operation rules pattern-match on a
static subsort (`op(X:S, …)`). A Boolean path condition `isS(V)` does **not**
refine `V` to sort `S` in the Haskell backend: the fixed rule stays stuck on
`V:Super`, so fixed-size claims close (every element becomes concrete) while
the unbounded claim unrolls or accumulates unsolved existential witnesses.
Neither escape is acceptable: a bounded-size theorem is a material domain
restriction (`PARTIAL`, not success), and an operational rule that force-casts
or intercepts the program manufactures `#Top` and fails the soundness gates.

The sound repair is the guarded total-projection idiom (the upstream K
`ceils.k` family). Introduce a total twin of the partial subsort cast and keep
every use guarded:

```k
syntax Bool ::= definedProjectS(Super) [function, total]
rule definedProjectS(V:Super) => isS(V)

syntax S ::= projectSTotal(Super)
  [function, total, symbol(projectSTotal), no-evaluators]

// #Ceil characterization of the built-in partial cast
rule #Ceil({@V:Super}:>S)
  => ({ definedProjectS(@V) #Equals true } #And #Ceil(@V))
  [simplification]

// orientation pair at the cast boundary
rule projectSTotal(V:Super) => {V}:>S
  requires definedProjectS(V)
  [concrete, simplification(10), preserves-definedness]
rule {V:Super}:>S => projectSTotal(V)
  requires definedProjectS(V)
  [symbolic(V), simplification, preserves-definedness]

// sort-based collapse and idempotence
rule projectSTotal(X:S) => X [simplification]
rule projectSTotal(projectSTotal(V)) => projectSTotal(V) [simplification]
```

When the backend has no hooks for the target sort at all (structure-only
reasoning), the collapse rule alone is enough: `projectSTotal(X:S) => X`
plus `[no-evaluators]` keeps the symbol uninterpreted everywhere else.

Then give the stuck operations **guarded dispatch twins**: simplification
rules over supersort variables that restate the semantics' own equation with
the projection applied under the exact guard.

```k
rule op(V:Super, W:Super) => opS(projectSTotal(V), projectSTotal(W))
  requires isS(V) andBool isS(W) [simplification]
```

For sequence domains, pair this with a recursive total domain predicate
(`allS(.Seq) => true`, `allS(cons(V, R)) => isS(V) andBool allS(R)`) as the
claim's precondition, so the guard on each unrolled head is entailed.

Soundness obligations — classify each piece under the shared
proof-extension contract before use:

- Every dispatch twin must be **the same equation** as an existing rule of
  the frozen semantics, restated over the supersort; its guard must cover
  exactly the original static match domain (match-domain containment and
  value fidelity — a twin that widens, narrows, or redirects the operation
  is an unsound bridge).
- The projection has **no evaluators and no `kprove`-firing rule** beyond
  collapse/orientation; it can never produce a value out of nothing (an
  unconstrained result symbol is the oracle bug).
- Orientation rules carry `preserves-definedness` and fire only where the
  definedness predicate is entailed.
- These extensions are derived lemmas or definitional summaries over the
  frozen semantics — not new trusted primitives — so validate them with the
  usual mutation and vacuity probes.

---

## Nested sequence domains — no custom wrapper sorts

Symptom: the input is a nested container — a sequence of heap references to
inner sequences — and the unbounded claim must range over every well-typed
inner sequence. The tempting representation is a custom embedding wrapper
(`xsSeq(IS)` injecting a homogeneous static sequence into the semantics'
dynamic sequence sort). This fails structurally: the semantics' iteration
rules match the dynamic sort's raw constructors (nil/cons), and the backend
will not narrow a custom wrapper application to those alternatives at the
loop head. Fixed-size instances close while the symbolic claim stalls on
unresolved constructor alternatives or diverges during the case split.

Sound approach, in order:

1. Represent symbolic inputs with the semantics' **own constructors** plus
   recursive domain predicates as claim preconditions (`allXs(S)` for
   element typing, length/shape predicates for structure). A custom wrapper
   sort is never the input representation; if one is convenient as a
   *summary codomain*, keep it out of every operational position.
2. Expose exactly **one constructor layer per circularity**. Give each loop
   its own claim whose initial term already has the iterated sequence in
   nil/cons form; the empty and cons instances are then separate proof
   obligations, and the backend never has to invent the split itself.
3. Summarize each inner loop as a **total, structurally recursive function
   over the raw constructors**, proved against that loop's circularity, so
   the outer induction carries only the summary value — never the inner
   sequence's structure.
4. Keep unexposed inner sequences **abstract**: one symbolic variable per
   heap entry in the outer claim, with only the currently iterated inner
   sequence unfolded by its own circularity.
5. Nested symbolic induction is memory-intensive on the Haskell backend.
   If a claim still diverges after the restructuring above, record each
   attempt with its resident-memory evidence and report the limitation
   honestly. Do not add iterator accelerator or interception rules to force
   progress — those manufacture `#Top` and fail the soundness gates.

---

## References

- [Proof-extension soundness contract](../shared/proof-extension-soundness.md) —
  classification, justification, and validation obligations for proof-local
  functions, equations, claims, and rewrites.
- [K functions, claims, and proof modules](../shared/k-claims.md) —
  `[function]`, `[simplification]`, and claim syntax.
- [Symbolic recursion](../shared/kprove-debug-troubleshoot/symbolic-recursion.md)
  — diagnosis when a helper keeps unfolding.
