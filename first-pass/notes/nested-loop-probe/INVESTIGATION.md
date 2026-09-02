# Nested-loop invariants work — inner loop in the `<k>` head + continuation

Question: can kprove close a **nested** loop invariant (an inner loop inside the outer loop's body)?
Needed for the index-based double loops in 20 (find_closest_elements) and 87 (get_row). This probe
confirms **yes**, and pins down the shape.

```sh
cd verification/humaneval/reference/notes/nested-loop-probe
kompile verif.k --backend haskell --main-module NEST --syntax-module NEST --output-definition verif-kompiled
kprove spec.k --definition verif-kompiled --spec-module NEST-SPEC --depth 5000   # #Top
```

## The result

`outer i in [0,N): inner j in [0,N): count += 1` proves `count` ends `C + N*N` — two claims
(`innerLoop => innerAcc`, `outerLoop => outerAcc`), both `#Top`.

## The two things that make it work

1. **Run the inner loop in the `<k>` HEAD, with a continuation — not buried as a function argument.**
   The natural-looking `outerLoop(...) => #runInner(I, HI, innerLoop(0, HI, C))` **fails**: the
   `innerLoop(...)` sits as an *argument*, so its circularity never fires (the same buried-term wall
   as opaque `sortI`/`split`) and the outer sticks. Instead:

   ```
   rule <k> outerLoop(I, HI, C) => innerLoop(0, HI, C) ~> #afterInner(I, HI) ... </k> requires I <Int HI
   rule <k> CV:Int ~> #afterInner(I, HI) => outerLoop(I +Int 1, HI, CV) ... </k>
   ```

   `innerLoop(0, HI, C)` is now the `<k>` head → it executes, its circularity resolves it to the
   count `CV`, then `#afterInner` continues the outer loop (exactly how a function call returns).

2. **`... </k>` cell-frame claims, not `~> REST`.** `<k> loop(...) => summary(...) ... </k>` lets the
   inner claim apply when the loop is followed by a continuation (`~> #afterInner`); the explicit
   `~> REST` form mismatched and looped. The inner claim is proved first and reused as a lemma when
   proving the outer (kprove composes the two circularities).

## Unlocks

**20 find_closest_elements** and **87 get_row** — index-based double loops over a symbolic list. Note
the body's `numbers[i]` is `atK(NUMS, i)`, an opaque `Int` for symbolic input, so the best-pair
comparisons are SMT-decidable symbolic-`Int` splits — tractable, though each problem still adds
Subscript / abs / tuple-output machinery on top of this nested skeleton.

## Follow-up (v3): opaque accumulator survives the boundary

`verif-opaque.k` / `spec-opaque.k` repeat the probe with the accumulator updated by an opaque
`stepI(A, J)` (`[function, total, no-evaluators]` — no rules on symbolic input), simulating 20's
min-tracking triple. Both claims still prove `#Top`: the opaque accumulator term flows through the
`CV:Int ~> #afterInner` inner->outer boundary capture unchanged. So a threaded opaque min/max
accumulator (not just a concrete `+1` count) closes through the nesting — **20 is buildable.**
