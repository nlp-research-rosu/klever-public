# Applying the sort framework to 33/37/105 — blocked by the opaque-output iteration wall

The full sort-correctness framework (`../sort-probe`) proves the sort is a sorted permutation. The
next hope was to use it to close the problems that **iterate the sorted output** (33 sort_third,
37 sort_even, 105 by_length). This probe shows that the framework is **necessary but not
sufficient**: those problems hit a *separate* wall the framework does not touch.

```sh
cd verification/humaneval/reference/notes/sort-apply-probe
kompile verif.k --backend haskell --main-module APPLY --syntax-module APPLY --output-definition verif-kompiled
kprove spec2.k    --definition verif-kompiled --spec-module APPLY-SPEC2    --depth 2000   # opaque   -> stuck
kprove spec-var.k --definition verif-kompiled --spec-module APPLY-VAR-SPEC --depth 2000   # variable -> #Top
```

## The experiment — "sort a list, then loop over it"

`sumLoop` consumes a list in the `<k>` cell (a stand-in for any loop over the sorted output). Two
claims, **identical loop shape**, differ only in what they loop over:

| loops over | claim | result |
|---|---|---|
| **opaque** `sortI(L)` (the trusted/proven sort output) | [`spec2.k`](spec2.k) | **stuck**, `#Top=0` |
| **symbolic variable** `S` | [`spec-var.k`](spec-var.k) | **`#Top`** |

`sortI(L)` is `[no-evaluators]`, so on a symbolic `L` it is an **opaque term** — neither `.IntSeq`
nor `iCons(...)`. The loop rules match those two constructors, so the loop **cannot consume it**: no
split, no progress, stuck. A symbolic *variable* `S` splits into `.IntSeq | iCons(H, T)` and iterates
normally (the standard fold circularity). The correctness framework changes nothing here — it proves
*facts about* `sortI(L)` (`isSorted`, `count`), but a program that **executes a loop over** the term
still stalls.

## Why the framework can't bridge it (in a single-claim proof)

To iterate the sorted output, it must be a **symbolic variable carrying `isSorted` + `count`
constraints**. Introducing such a variable *mid-execution* (where `sorted()` is called) needs an
`ensures`-style constraint attached to a fresh `?S` — but **only claims have `ensures`/existentials;
rewrite rules do not**. So `sorted(l)` can only rewrite to the opaque `sortI(L)` (unconstrained
`?S` would be an unsound "sort returns anything"), and the downstream loop stalls. The program's own
execution gets stuck, independent of the postcondition.

## Consequence

- **33 / 37 / 105 stay blocked for a single-claim full-function proof.** They iterate the sorted
  output; the execution stalls on the opaque term.
- The **framework's real payoff stands**: the sort is proven correct, which retroactively backs the
  six trusted-sort proofs (88, 34, 58, 149, 120, 47) — their `isSorted(sortI(L))` / `isPerm` trust
  is now proof-backed rather than assumed.
- A **decomposition** is possible but weaker than our per-problem bar: prove the sort via the
  framework, and *separately* prove the post-sort logic as a claim over a **symbolic sorted-variable
  input** (`spec-var.k` shows such folds close). The end-to-end `result == spec` then follows
  logically but is not a single `#Top`, so it does not meet the "one entry claim per problem"
  standard the corpus uses.

**Bottom line:** the framework closes *sort correctness* and upgrades the trust boundary of six
existing proofs; it does not, by itself, unlock the iterate-the-sorted-output problems — those need
a mid-execution "havoc + assume sorted permutation" step that kprove's rule layer cannot express.

---

## UPDATE — the wall is crackable: a universal loop-invariant lemma discharges the opaque loop

The "bottom line" above is **too pessimistic**. It tested the opaque loop as a *single* claim
(`spec2.k`, stuck) and a variable loop as a *separate* claim (`spec-var.k`, `#Top`) — but never put
them in **one module** and let the variable claim act as a **lemma/circularity** for the opaque one.
It can, and this is exactly how every loop-invariant proof (20, 87, 96) discharges its loop.

```sh
kprove spec-both.k       --definition verif-kompiled --spec-module APPLY-BOTH       # #Top (both)
kprove spec-entry-only.k --definition verif-kompiled --spec-module APPLY-ENTRY-ONLY # #Top=0 (stuck)
```

| module | claims | result |
|---|---|---|
| `spec-entry-only.k` | entry `sumLoop(sortI(L),0) => sumOf(sortI(L))` alone | **stuck** (`#Top=0`) |
| `spec-both.k` | entry **+** invariant `sumLoop(S,A) => A +Int sumOf(S)` (cell-framed `...`) | **`#Top`** |

The invariant is over a **fresh universally-quantified variable** `S`; kprove proves it by the
standard fold circularity (splitting `S` into `.IntSeq | iCons`). The entry's `sumLoop(sortI(L),0)`
is then discharged as the **instance `S := sortI(L)`** — no execution over the opaque term, no
unrolling, no stall.

### Why this is sound (the old worry does not apply)

The earlier section feared "introducing an unconstrained `?S` mid-execution = *sort returns
anything* = unsound." That is **not** what happens. We do **not** havoc `sortI(L)` into an
unconstrained variable. We apply a lemma that is **true for every `S`** to the **specific** term
`sortI(L)`. `∀S. sumLoop(S,A) = A + sumOf(S)` is proved outright; its instance at `S = sortI(L)` is a
logical consequence. The result `sumOf(sortI(L))` still names the actual sorted list — no information
is lost or fabricated. Soundness is identical to any loop-invariant application.

### Consequence — the opaque-sort cluster is REACHABLE

33 / 37 / 105 / 19 / 86 (and 70) that **iterate** the sorted output are provable with a **two-claim**
spec: (1) the post-sort loop invariant over a **variable sorted list** `S` (does the real
reconstruction/aggregation work), (2) the entry that calls `sorted()` and reaches the loop, closed by
(1) at `S := sortI(...)`. `sortI` itself is trusted-and-proven (`../sort-probe`), so the whole chain
is proof-backed. Each still needs its own reconstruction invariant, but the wall itself is gone.
