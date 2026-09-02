# Proof — `break` on the general semantics

A minimal proof that the **general (`src/`) semantics** executes and proves `break` over the
reference's real heterogeneous `list(ValSeq)`. `solution.py`:

```python
def f(xs):
    total = 0
    for x in xs:
        if x < 0:
            break          # stop at the first negative
        total += x
    return total
```

`kprove`: **`#Top`** (both claims), non-vacuous; `krun` smoke green.

## Build + run

```sh
D=verification/humaneval/reference/tests/verification/loop-break
kompile "$D/verification.k" --backend haskell \
  --main-module LOOP-BREAK-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition "$D/verification-kompiled"
kprove "$D/spec.k" --definition "$D/verification-kompiled" --spec-module LOOP-BREAK-SPEC   # => #Top
# krun uses the general semantics (kompile src/semantics.k --backend llvm --main-module MPY …).
```

## What this exercises

- **The general semantics, unmodified.** `verification.k` does `imports MPY-LEMMAS` (which
  `imports MPY`) — no standalone re-implementation, no `seq(IntSeq)` cut. `break` is the general
  **in-cell** control: `Break => #brk`, which drops the rest of the body one item at a time
  (`#brk ~> (_ => .K) [owise]`) until the in-cell `loopLbl`, then `#brk ~> loopLbl(_) => .K` exits
  the loop. No `<lstack>`.
- **A symbolic heterogeneous `list(ValSeq)`.** The loop iterates a `List[int]` whose elements are
  `Val`s. To *decide* `x < 0`, the element is cast to Int with the **`projectIntTotal` total cast**
  (`src/lemmas.k`, MPY-LEMMAS): declared `[total]`, so Z3 treats it as an unknown integer and the
  branch splits. The claims carry `requires allInt(VS)` (the `List[int]` type guarantee), which
  splits with the list and discharges the per-element cast. (Background:
  `../../notes/val-cast-probe`.)

## The proof

Summary `prefixSum(S, B)` = `B` plus the sum of the non-negative **prefix** of `S`, stopping at the
first element `< 0` — exactly what `break` computes. It is written with `projectIntTotal(V)` directly
(hence `[total]`), so the store's `total` carries **no `#Ceil` obligation** — a partial summary
leaves `\not(\ceil(_))` in a stuck state, which crashes the haskell backend.

Two `[all-path]` claims: (1) loop invariant `#loop(list(VS), x, body) => .K` leaving
`total = prefixSum(VS, B)`; (2) entry `result = f(list(VS)) == prefixSum(VS, 0)`.

## Reliability

- **Non-vacuous:** corrupting the entry postcondition to `prefixSum(VS,0) +Int 1` fails the
  implication (`#Top`=0, 0 parse errors).
- **Same machinery as `krun`:** `smoke.mpy` runs the identical general-semantics loop concretely
  (`f([1,-2,3]) == 1`, …); the proof drives it on a symbolic `list(VS)`.
