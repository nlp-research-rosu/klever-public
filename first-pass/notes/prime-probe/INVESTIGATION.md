# is_prime is provable — the symbolic-bound divisor scan closes

Jeff's categorization flags the **primality cluster** (`31 39 75 82 94 96 127 143 150`) as the one
bucket in "unbounded recursion" with a *plausible unlock*, riding the `range-loop` (Gauss) machinery.
This probe settles it: **the is_prime core proves.**

```sh
cd verification/humaneval/reference/notes/prime-probe
kompile verif.k --backend haskell --main-module PRIME --syntax-module PRIME --output-definition verif-kompiled
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 300 kprove spec.k --definition verif-kompiled --spec-module PRIME-SPEC --depth 3000
```

## What it tests

[`verif.k`](verif.k) is the is_prime core stripped to its essence — a **symbolic-bound divisor
scan** with early exit:

```
scan(I, N):  for i in [I, N):  if N % i == 0  ->  "div" (stop);  else i+1
```

with the boolean ∃-summary `hasDiv(I, N) = ∃ j in [I, N): N mod j == 0` (recurses on the
**increasing** counter `i`, so it can't be `[total]` — declared `[function]` + a full-coverage
`#Ceil(hasDiv(_,_)) => #Top`). [`spec.k`](spec.k) claims `scan(I, N)` ends with `<res> = div` iff
`hasDiv(I, N)`.

**Result: `#Top`, non-vacuous** ([out.txt](out.txt); flipping the postcondition fails, 0 parse
errors). So kprove handles all three things is_prime needs at once:

1. the **counter induction** over a symbolic bound `N` (the `range-loop` machinery),
2. the symbolic **`N %Int i ==Int 0` case-split** (3-way via the rule guards — modulo is hooked, so
   it's decidable), and
3. a **threaded boolean ∃-summary** (early-exit, so no associativity step — matches syntactically
   each iteration, the same shape that made `loop-break`/`val-cast` branches close).

## What it unlocks (HumanEval/31 is exactly this)

`is_prime(n)`: `if n < 2: return False; for k in range(2, n-1): if n % k == 0: return False; return True`
— the probe's scan with `N = n`, bound `n-1`. Modulo is already in the proven corpus (102, 103, 106).

Once `is_prime` is built over the per-problem semantics (range loop + early return + `applyBin("%")`),
the dependents follow with a thin wrapper:

- **direct** — `31 is_prime`; `150 x_or_y` (`x if is_prime(n) else y`); `82 prime_length`
  (`is_prime(len(s))`); `143 words_in_sentence` (keep words of prime length); `127 intersection`
  (prime intersection length → "YES"/"NO").
- **loop over is_prime** — `96 count_up_to` (the first primes).
- **harder, is_prime + more** — `94` (largest prime in a list + digit sum), `75` (product of exactly
  3 primes), `39` (prime Fibonacci).

So ~5-6 of jeff's 36 are reachable with this one unlock; the rest of his buckets (sort-correctness
×17, float-rounding ×4, factorization/root ×4, external ×2) stay genuinely walled.
