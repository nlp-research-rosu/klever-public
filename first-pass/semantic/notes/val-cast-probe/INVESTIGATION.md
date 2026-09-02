# Iterating a symbolic heterogeneous `list(ValSeq)` in a proof — folds AND branches

The question: can `loop-break` / `loop-continue` drop their `seq(IntSeq)` cut and prove over the
reference's **real** heterogeneous list `list(ValSeq)` — i.e. a circularity over a symbolic,
unknown-length, all-int payload? **Yes, both folds and branches.** The one genuine dead-end is
burying the symbolic variable inside a function.

```sh
cd verification/humaneval/reference/notes/val-cast-probe
kompile verif.k         --backend haskell --main-module VERIF --syntax-module VERIF --output-definition verif-kompiled
kompile verif-partial.k --backend haskell --main-module VERIF --syntax-module VERIF --output-definition verif-partial-kompiled
# then, capped (see memory cap-kprove-memory):
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 300 kprove spec-branch.k --definition verif-kompiled --spec-module BRANCH-SPEC --depth 2000
```

## Setup

[`verif.k`](verif.k) is a minimal model of the real semantics: `Val` is a genuine union
(`Int | other | list(ValSeq) | seq(IntSeq)`); `applyBin`/`applyCmp` match **`Int` only** (a `Val`
head does not match); a `for`-loop with `if x < 0: break`. The bridge from a `Val` element to an
`Int` is the **RV `ceils.k` total-cast pattern** — `projectIntTotal` declared
`[function, total, symbol(projectIntTotal), no-evaluators]`, plus a `[symbolic(Arg0)]` rule that
turns the partial cast `{V}:>Int` into it.

[`verif-partial.k`](verif-partial.k) is identical **except** `projectIntTotal` is a bare
`[function]` (no `total`, no `no-evaluators`) — the contrast.

## The experiments

Each row is one `spec-*.k`; result is `kprove … | grep -c '^#Top'`, saved beside it as `*.out`.

| # | file | what it tests | definition | result |
| --- | --- | --- | --- | --- |
| buried | [`spec-buried.k`](spec-buried.k) | symbolic var **hidden in a function**: `floop(list(ints2vals(IS)))` | verif | **FAIL** ([out](buried.out)) |
| fold | [`spec-fold.k`](spec-fold.k) | a **fold** (sum-all) over `list(VS)`, var in the open | verif | **#Top** ([out](fold.out)) |
| branch | [`spec-branch.k`](spec-branch.k) | **loop-break** over `list(VS)` — the answer | verif | **#Top** ([out](branch.out)) |
| branch-partial | [`spec-branch-partial.k`](spec-branch-partial.k) | **same claim**, bare `[function]` cast | verif-partial | **FAIL** ([out](branch-partial.out)) |
| control | [`spec-control-seq.k`](spec-control-seq.k) | same loop-break over `seq(IntSeq)` — a **genuine Int** head | verif | **#Top** ([out](control-seq.out)) |

(`branch` is non-vacuous: corrupting its postcondition to `prefixSumAcc(VS,A) +Int 1` fails the
implication, 0 parse errors.)

## What the rows say

- **buried** is the only real wall. With the payload written `ints2vals(IS)`, the variable kprove
  must split (`IS`) is **inside a function call**, so kprove unifies the opaque term with the loop
  rules' constructors instead of splitting `IS` — the induction never starts. *Don't bury the
  symbolic variable.*

- **fold vs branch.** A fold only ever **carries** the projected value (`A +Int {V}:>Int`, matched
  syntactically — no decision), so it proves trivially. A branch must **decide** `x < 0` to pick an
  arm; that needs the value to be **SMT-representable**.

- **branch vs branch-partial** is the crux. Same claim, same machinery — the *only* difference is
  the cast's attributes. With `[total, no-evaluators]`, `projectIntTotal(V)` is an abstract integer
  Z3 can reason about, so `projectIntTotal(V) <Int 0` is decidable and the branch splits (**#Top**).
  With a bare `[function]`, the same comparison is left **`≠true ∧ ≠false`** — not SMT-representable,
  so the branch can't decide (**FAIL**).

- **control** confirms the discriminator is **totality, not "Val-ness"**: a genuine `Int` head (and
  equally any `[total]` term) branches with no cast at all.

## Why `projectIntTotal` is "total" — the `no-evaluators` trick

`{V}:>Int` (the `:>` downcast) is genuinely partial — `#Bottom` when `V` isn't an `Int`, so you
cannot declare *it* total. `projectIntTotal` is a **separate, fresh symbol**. `no-evaluators` means
*it has no rewrite rules to evaluate it* — so K's totality checker has nothing to verify against and
takes `[total]` as a **declaration** (a sound totalization: any partial function extends to a total
one; the proof only uses it under `allInt`, where it equals the real cast). This is the standard K
idiom for an abstract uninterpreted total function — KEVM declares `keccak`, `hash`, gas, and
map-`store` the exact same way (`[function, total, no-evaluators, smtlib(...)]`). Being `[total]` is
what makes the term reach Z3 (the flip side of [`../lstack-probe`](../lstack-probe/INVESTIGATION.md):
partial terms never reach Z3, total ones do). The two `[concrete]`/`[symbolic(Arg0)]` rules are both
`[simplification]` (kprove-only, never `krun`): the symbolic one turns `{V}:>Int` into the abstract
`projectIntTotal(V)` during a proof; the concrete one unwraps it back to compute once `V` is a
literal.

To watch `projectIntTotal(V)` enter the comparison and the branch split, step a proof with
`--depth N` (kprove prints the remaining configuration after N rewrites).

## Bottom line

A symbolic heterogeneous `list(ValSeq)` **is** iterable in a proof — folds via a threaded summary,
branches via the `projectIntTotal` total-cast — so `loop-break`/`loop-continue` need no `seq` cut.
`str(IntSeq)` / `rangeObj` stay the correct, simplest models where they apply (a string *is* code
points, a range *is* arithmetic); the total-cast is what handles a genuinely heterogeneous
`List[int]`. The only thing that doesn't work is hiding the symbolic variable inside a function.
