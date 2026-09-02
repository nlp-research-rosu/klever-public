# Proof — `continue` on the general semantics

A minimal proof that the **general (`src/`) semantics** executes and proves `continue` over the
reference's real heterogeneous `list(ValSeq)`. `solution.py`:

```python
def f(xs):
    total = 0
    for x in xs:
        if x < 0:
            continue       # skip negatives
        total += x
    return total
```

`kprove`: **`#Top`** (both claims), non-vacuous; `krun` smoke green.

## Build + run

```sh
D=verification/humaneval/reference/tests/verification/loop-continue
kompile "$D/verification.k" --backend haskell \
  --main-module LOOP-CONTINUE-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition "$D/verification-kompiled"
kprove "$D/spec.k" --definition "$D/verification-kompiled" --spec-module LOOP-CONTINUE-SPEC  # => #Top
```

## `continue` proves IN-CELL — no resume slot

The earlier version of this demo used a `<lstack>` **resume slot**, on the theory that `continue`
must resume the next iteration after `Continue ~> _` discards the body, and that an in-cell next
iteration would be discarded too. **The general semantics does not need it.** `continue` is in-cell,
exactly like `break`, and the difference is only *which rule fires at the `loopLbl`*:

```k
rule <k> Continue => #cont ... </k>
rule <k> #cont ~> (_:KItem => .K) ... </k>    [owise]   // drop the rest of THIS body, one item…
rule <k> #cont ~> loopLbl(NEXT:K) => NEXT ... </k>      // …until loopLbl, then run the NEXT iteration
```

Because the discard is **one item at a time (`[owise]`)** rather than `~> _`, it stops *at* the
loopLbl (which still holds `#loop(REST,…)` in the `<k>` cell) and jumps into it — `break` instead
drops the loopLbl and exits. Both proved; there is no `<lstack>`.

## The proof

Summary `posSum(S, B)` = `B` plus the sum of the **non-negative** elements of `S` (negatives skipped).
It is written with `projectIntTotal(V)` directly (hence `[total]`) so the store's `total` carries no
`#Ceil` obligation. The heterogeneous element is made SMT-decidable by the **`projectIntTotal` total
cast** (`src/lemmas.k`, MPY-LEMMAS); the claims carry `requires allInt(VS)` (the `List[int]`
guarantee). Background: `../../notes/val-cast-probe`.

Two `[all-path]` claims: (1) loop invariant `#loop(list(VS), x, body) => .K` leaving
`total = posSum(VS, B)`; (2) entry `result = f(list(VS)) == posSum(VS, 0)`.

## Reliability

- **Non-vacuous:** corrupting the entry postcondition to `posSum(VS,0) +Int 1` fails the implication
  (`#Top`=0, 0 parse errors).
- **Differential-tested summary:** `posSum` matches CPython `f` on 200k random inputs (0 mismatches).
- **Same machinery as `krun`:** `smoke.mpy` runs the identical general-semantics `continue` concretely
  (`f([1,-2,3]) == 4`, …); the proof drives it on a symbolic `list(VS)`.
