# Probe B: heap-list builders (de-escape rework Tasks 4/5)

## Question

With lists as heap objects (`ref(H)` in scopes, `H |-> list(VS)` in `<heap>`,
every constructor allocating), do the three builder claim shapes prove —
including loops whose bodies ALLOCATE garbage every iteration?

## Result: ALL FOUR CLAIMS #Top

`probe.py` (CPython + krun green): `build_squares` (`.append` builder) and
`build_plus` (`out = out + [i]` builder). Claims: two loop invariants + two
entries. `kprove spec.k` closes the whole module in one run.

## The three validated shapes

1. **Append-loop invariant** (body never allocates): the accumulator ref is
   FIXED; the heap entry folds in place and the rest is LITERALLY unchanged:
   `<heap> (RN |-> list(ACC)) HREST => (RN |-> list(sqFold(I, N, ACC))) HREST`,
   scope binds `ref(RN)` on both sides. NO premises needed.
2. **Plus-builder invariant** (two allocations per iteration — the `[i]`
   literal and the `+` result; the accumulator ref MOVES): scope
   `ref(ON) => ref(?ON2)`, heap
   `(ON |-> list(ACC)) HREST => (?ON2 |-> list(plusFold(I, N, ACC))) ?_:Map`,
   `<heapLoc> HL => ?_`, premises
   `0 <=Int ON andBool ON <Int HL andBool keysBelow(HREST, HL)`. Garbage lands
   in the abstract rest; the freshness guard discharges via the keysBelow
   axioms (lemmas/heap.k).
3. **Entry with an existential result ref**: `<heap> .Map =>
   (?NO |-> list(fold)) ?_:Map`, `<heapLoc> 0 => ?_`, scope post
   `"res" <- ref(?NO)`. Unification finds the result entry even with garbage
   in the final heap.

## Two probed lessons (both cost a timeout each)

- **Carry `0 <=Int HL` (via `0 <=Int ON andBool ON <Int HL`)**: the
  keysBelow offset absorption matches `B +Int K`; whichever operand the
  normalizer puts second must be provably non-negative.
- **Monotonicity must not lower the bound eagerly.** The first formulation
  `keysBelow(M, B +Int K) => keysBelow(M, B)` fired on the WHOLE map before
  the concrete entries peeled — the entry keyed exactly `HL` then failed
  `HL <Int HL` and the circularity never re-applied (pure unrolling, timeout).
  Fix: `keysBelow(M, B +Int K) => true requires K >=Int 0 andBool
  keysBelow(M, B)` — the requires-recursion forces peel-first order. The
  depth-60 frontier dump showed the exact false obligation
  `keysBelow((HL |-> …) …, HL)`.

## Migration guidance (the 44 allocating spec files)

- Input lists (FuncDef param names) stay BARE `list(VS)` bindings — readers
  are untouched (verify.sh's symbolic folds confirmed compatible).
- Constructed accumulators (non-param names bound to `list(…)`) take shape 2
  (or shape 1 once P-tasks rewrite `x = x + [e]` to `.append`).
- Entry claims add the heap cells; list results take shape 3; scalar results
  just add `<heap> .Map => ?_:Map` + `<heapLoc> 0 => ?_:Int`.
