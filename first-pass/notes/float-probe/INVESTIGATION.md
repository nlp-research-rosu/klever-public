# Float map/fold problems (21/4) ARE provable — K `Float` + trusted opaque ops + accumulator threading

The `float-proving-limitation` note (K can't prove symbolic IEEE-754 arithmetic) does NOT block the
float **map/fold** problems (21 rescale_to_unit, 4 mean_absolute_deviation). Those don't need to
*reason about* float values — they build an output list whose elements are a trusted float op applied
per element. Model the op as opaque (`[function, total, no-evaluators]`) and the proof only threads
opaque `Float` terms; K's `Float` sort still lets `krun` compute real float results (a genuine krun
story, unlike 71's opaque-Val approach).

```sh
kprove spec.k     --definition verif-kompiled --spec-module FP-MAIN  # #Top  (accumulator-threading)
kprove spec-min.k --definition verif-kompiled --spec-module FP-MIN   # #Top  (K-Float itself is fine)
```

## The two findings

1. **K `Float` is fine in kprove.** A symbolic `Float` variable through one opaque op
   (`spec-min.k`) proves instantly. Float does not hang the prover.
2. **Thread the accumulator; don't concat-after.** The map fold's summary must take the output
   accumulator as an argument and thread it exactly as the loop does
   (`mapFA(R, LO, D, appF(ACC, rescale(X,LO,D)))`), matching the Int fold problems. The natural-looking
   `loop(FS,LO,D,ACC) => concatF(ACC, mapF(FS,LO,D))` gets **stuck on the base case**
   (`concatF(ACC, .FloatSeq)` doesn't reduce to `ACC` for symbolic `ACC` — right-identity isn't
   syntactic). Threading the accumulator sidesteps that (base case is `ACC => ACC`).

## Consequence

21/4 are buildable: model the input as a `Float` list, `min`/`max`/`/`/`abs` as trusted opaque float
primitives (concrete K-Float rules for krun), and verify the position-preserving map/fold with an
accumulator-threading summary. The float arithmetic is trusted (klean-bound); the map/fold structure
is verified.

## Follow-up: float WHILE-loop guards split — 32 find_zero is reachable (partial correctness)

`verif-while.k` / `spec-while.k`: a `while guard(B): B := step(B)` loop with an **opaque-float**
guard (`guard`, `step` both `[no-evaluators]`) proves partial correctness `#Top`. kprove
case-splits any `Bool` — `guard(B)` true (run body + recurse) vs false (exit) — regardless of whether
the float comparison is *decidable*. The coinductive `[all-path]` circularity discharges the
recursive case. So 32's bisection guard (`end - begin > 1e-10` on symbolic floats) does NOT block:
32 is provable as **partial correctness** (like the Collatz proofs) with trusted opaque poly/float
ops — "if the bracket + bisection loops halt, `result = begin`". The loop-threading structure is
verified; the float arithmetic and root property are trusted (klean).
