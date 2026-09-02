# Partial correctness unlocks the termination-dependent problems

Xiaohong's observation: for the "unbounded" problems we do **not** need *total* correctness (which
would require proving the loop halts — for Collatz that *is* the conjecture). **Partial correctness**
suffices: *if* the loop halts, the result is correct. This probe confirms kprove proves exactly that.

```sh
cd verification/humaneval/reference/notes/partial-correctness-probe
kompile verif4.k --backend haskell --main-module PARTIAL4 --syntax-module PARTIAL4 --output-definition verif4-kompiled
kprove spec4.k --definition verif4-kompiled --spec-module PARTIAL4-SPEC --depth 3000   # #Top
```

## The result

A **Collatz `3n+1` loop** — which is *not known to terminate* — proves
`loop(N, C) => cAcc(N, C)` (`[all-path]`, `#Top`). kprove's reachability circularity is
**coinductive**: it discharges the recursive case with the claim itself after ≥1 step, establishing
that *every terminating* execution reaches the target. It never requires a well-founded / decreasing
measure, so it does **not** prove halting. That is precisely partial correctness: **if it halts, the
result equals the summary.**

## Two things had to be right

1. **Threaded-accumulator summary, not additive.** `loop(N, C) => C +Int f(N)` **fails**: after one
   step the goal is `C+1+f(N/2) == C+(f(N/2)+1)` — trivially true, but kprove's implication check
   does not reassociate `+Int` past the opaque `f(...)`, and it sticks. Threading the accumulator
   *through* the summary — `loop(N, C) => cAcc(N, C)` with
   `cAcc(N,C) => cAcc(step(N), C+1)` — makes the summary unfold in **lockstep** with the loop, so
   both sides reduce to the identical term `cAcc(step(N), C+1)` (structural match, no arithmetic).
   This is the same threaded shape the working proofs already use (primeAcc, lastFold, cubeAcc).
2. **`cАcc` is `[function, total]` + `[simplification]`** (clears `#Ceil`, unfolds in the check).

## What this unlocks (as PARTIAL correctness)

| # | loop | why total was impossible / hard |
|---|---|---|
| **123** get_odd_collatz | Collatz orbit | halting = the Collatz conjecture |
| **39** prime_fib | scan Fibonacci for the n-th prime | halting = infinitude of Fibonacci primes (open) |
| **25** factorize | trial division `while n % d == 0` | terminates, but the trip count has no closed form (two-variable measure) — partial correctness sidesteps the measure entirely |
| **59** largest_prime_factor | same trial-division shape | same |

For all four, the honest theorem is **partial correctness**: the `while`-loop invariant is a threaded
`[function, total]` summary; `[all-path]` + circularity proves the result matches it *if the loop
exits*, with no termination obligation. (123 additionally ends in a `sorted(...)` — fine, the sort is
last: `result == sortI(collected)`.)

## Note on rigor

State the theorem honestly in each `PROOF.md`: **partial correctness** (`if the loop halts, …`), not
total. This is a standard, legitimate Hoare-logic result and the correct one here — total correctness
for 123/39 would be a proof of an open conjecture.
