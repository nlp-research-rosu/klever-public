# Why the counter loop proof stalled — it was the SUMMARY, not `<lstack>`

This folder is a self-contained probe. Every claim below is in a `.k` file here; the table is
reproduced by `kompile`-ing [`verif.k`](verif.k) once and running `kprove` on each `spec-*.k`.

```sh
cd verification/humaneval/reference/notes/lstack-probe
kompile verif.k --backend haskell --main-module VERIF --syntax-module VERIF --output-definition verif-kompiled
# then, capped (see memory cap-kprove-memory):
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 600 kprove spec-A-counter-nontotal.k --definition verif-kompiled --spec-module ACLAIM --depth 2000
```

## The question

Earlier I claimed: a `for i in range(N)` loop over a symbolic `N` *jams* kprove when the
next iteration is fetched from a side cell (`<lstack>`), and "fixed" it by moving the loop-back
into the `<k>` cell (the WASM method). That reasoning was **wrong**. RV's python-semantics uses
`<lstack>` and it works, so "the side cell jams on counters" can't be the real story. This probe
finds the real one.

## The setup — two loops, identical machinery, one difference

[`verif.k`](verif.k) defines two loops that share **byte-identical** loop control — the same
`<lstack>`, the same `#iterEnd` (fetch the next iteration from the side cell), the same
`#loopDone`. The only difference is the advance:

- `cLoop(I, N)` — a **counter** (`I -> I+1` until `I >= N`): *arithmetic* recursion.
- `sLoop(S)` — a **cons-list**: *structural* recursion (the tail `R` is smaller than `iCons(X,R)`).

Each iteration adds the current element to `<acc>`. So both compute a sum; we prove
`<acc>` ends at the right total.

It also defines four summaries so each spec varies exactly one thing:

| summary | recursion | `[total]`? | form |
| --- | --- | --- | --- |
| `sumTo(I,N)` | counter (arg **increases** `I+1`) | **no** (K can't accept it) | additive |
| `seqSum(S)` | list (arg **shrinks** `R`) | **yes** | additive |
| `seqSumNT(S)` | list — *same rules as `seqSum`* | **no** (just not marked total) | additive |
| `sumToAcc(I,N,ACC)` | counter | no | **threaded** (accumulator passed in) |

## The experiments (this IS the table, and where it comes from)

Each row is one `spec-*.k` file; "result" is `kprove ... | grep -c '^#Top'`.

| # | file | loop | summary | result |
| --- | --- | --- | --- | --- |
| A′ | [`spec-Aprime-seq-total.k`](spec-Aprime-seq-total.k) | seq | `seqSum` (total), additive | **#Top** |
| A | [`spec-A-counter-nontotal.k`](spec-A-counter-nontotal.k) | counter | `sumTo` (non-total), additive | **FAIL** |
| control | [`spec-control-seq-nontotal.k`](spec-control-seq-nontotal.k) | **seq** | `seqSumNT` (**non-total**), additive | **FAIL** |
| threaded | [`spec-counter-threaded.k`](spec-counter-threaded.k) | counter | `sumToAcc` (non-total), **threaded** | **#Top** |
| closed | [`spec-counter-closedform.k`](spec-counter-closedform.k) | counter | `(N(N-1)-I(I-1))/2`, pure arithmetic | **#Top** |

Read the rows:

- **A′ vs A** is the original mystery: seq proves, counter fails. Looks like "counter bad."
- **control** is the kill shot: take the *sequence* loop — the one that worked — and make its
  summary non-total (identical rules, drop `[total]`). It now **FAILS too**. So it was never
  counter-vs-seq, and never the `<lstack>`. The variable is the summary's `[total]`-ness.
- **threaded** and **closed** fix the *counter* without touching the loop or the summary's
  totality — by removing the need for the one thing that breaks (next section).

A (and the control) fail on exactly this — see [`A-failure.out`](A-failure.out):

```
#Not (  A +Int I +Int sumTo(I+1, N)   #Equals   A +Int ( I +Int sumTo(I+1, N) )  )
```

That is `(A+I)+Y == A+(I+Y)` with `Y = sumTo(I+1,N)`. **Pure associativity of `+`.** kprove
could not discharge it. The whole puzzle is: why can't it prove `(A+I)+Y == A+(I+Y)`?

## What Z3 is, and why associativity needs it

**Z3 is an SMT solver.** SMT = "Satisfiability Modulo Theories." Think of it as an automated
theorem prover for *decidable math*: you hand it a logical formula over integers, booleans,
arrays, etc., and it answers **satisfiable** (there's an assignment making it true) or
**unsatisfiable** (no assignment — i.e. the negation is a theorem). It is the engine kprove
calls whenever a proof step needs *arithmetic/logic reasoning* rather than rewriting.

Two things Z3 knows that matter here:

1. **Theory of linear integer arithmetic.** Z3 has `+`, `-`, `*`, `<`, `<=`, `/` (floor) for
   integers built in, with all their laws — commutativity, **associativity**, distributivity,
   etc. Ask it "is `(a+b)+c == a+(b+c)` for all integers?" and it says yes instantly. This is
   why the **closed-form** row passes: `A + (N(N-1)-I(I-1))/2` is *all* integer arithmetic, so
   Z3 verifies the whole Gauss identity (including the floor `/2`) by itself.

2. **Uninterpreted functions (UF).** If a formula mentions a function `f` that Z3 doesn't have a
   theory for, Z3 treats it as a **black box**: it knows nothing about `f` *except* one rule —
   **congruence**: equal inputs give equal outputs (`x == y  ⇒  f(x) == f(y)`). It assumes `f`
   returns *some* integer, but has no idea which. Crucially, even as a black box, `f(z)` is still
   a single integer value, so Z3 can reason about the arithmetic *around* it: it can prove
   `(a + b) + f(z) == a + (b + f(z))` by treating `f(z)` as an unknown-but-fixed integer `Y` and
   applying associativity. **This is exactly the step A needs.**

So if Z3 gets the goal with `sumTo(I+1,N)` abstracted as an unknown integer `Y`, it closes A by
associativity — same as it closes A′. The failure means **kprove never handed that goal to Z3
in that form.**

## Why a non-total function never reaches Z3 (the real mechanism)

To call Z3, kprove must first **translate** the K proof goal into an SMT formula. Integers,
`+Int`, `<Int` map straight onto Z3's integer theory. A function application like `sumTo(I+1,N)`
has to become *something* in SMT — and the only sound option is to abstract it as an
**uninterpreted** value (the `Y` above). But abstracting `f(x)` as a plain integer value is only
sound if `f(x)` *is* a value — i.e. `f` is **defined** at `x`.

- A **`[total]`** function is defined for every input, by declaration. So `seqSum(R)` is
  guaranteed to be some integer; kprove can hand Z3 "`Y := seqSum(R)`, an unknown integer," and
  Z3 finishes A′ by associativity.
- A plain **`[function]`** may be **partial** — undefined on some inputs (it would be `#Bottom`,
  K's "no value"). kprove cannot soundly tell Z3 "`sumTo(I+1,N)` is some integer," because for
  all the translator knows it might be undefined. So the term containing `sumTo(...)` is **not
  SMT-translatable**, kprove **does not send the equality to Z3 at all**, and falls back to a
  **purely syntactic** check: is `A +Int I +Int sumTo(...)` the *same syntax tree* as
  `A +Int (I +Int sumTo(...))`? It is not — one is `(A+I)+Y`, the other `A+(I+Y)` — so it
  reports the implication unproven. (`+Int` is a *hooked function*, not an associative-commutative
  *constructor*, so kprove doesn't structurally normalize it either; without Z3 there's nothing
  to bridge the parentheses.)

The `rule #Ceil(sumTo(...)) => #Top` I tried earlier asserts "`sumTo` is defined here," which
removes a *different* obstacle (the `#Ceil` definedness side-goal), but it does **not** make the
symbol SMT-translatable — kprove still won't abstract a partial symbol into Z3. That's why the
`#Ceil` lemmas were whack-a-mole: they never addressed the actual reason.

### Why `sumTo` can't just be `[total]`

`[total]` is a claim K *checks*: a function is total if it provably terminates and covers all
inputs. `seqSum` recurses on `R`, which is **structurally smaller** each step — K accepts that as
terminating, so `[total]` holds. `sumTo(I,N)` recurses on `I+1`, an **increasing** argument — K's
termination check can't see why that stops, so it refuses `[total]`. That single fact is the
entire counter-vs-list asymmetry: *structural* recursion is total-able, *arithmetic* recursion is
not, and only a total (or pure-arithmetic) summand survives the SMT translation needed for the
additive associativity step.

## The three fixes (and why each works)

- **Closed form** (`closed` row): no function symbol at all — the summand is pure integer
  arithmetic, fully inside Z3's theory, so Z3 verifies the whole identity. Strongest result too
  (you get the actual formula, e.g. `N*(N-1)/2`).
- **`[total]` summary**: keep the recursive summary but make it total (possible when recursion is
  structural). Then it abstracts cleanly into Z3 and the associativity bridges. This is what the
  list demos already do with `seq(IntSeq)`.
- **Thread the accumulator** (`threaded` row): write `acc := sumToAcc(I, N, A)` instead of
  `acc := A + sumTo(I, N)`. Now each step's reached term *is* the summary's unfold —
  `sumToAcc(I+1, N, A+I)` on both sides — so the check is **syntactic equality, no associativity,
  no Z3 needed**. Works even for a non-total summary.

## Bottom line

The `<lstack>` side-cell resume model is fine for counters — proven here in every configuration.
My range-loop stall was a bug in that specific spec (an additive non-total summary), not a
property of counter loops or side cells. The reusable rule is about **summaries**, independent of
the loop control:

> A loop-invariant summary must be **closed-form**, **`[total]`**, or **threaded** — never an
> additive non-total recursive function — or the inductive associativity step can't reach Z3.
