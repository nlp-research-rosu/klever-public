# How bad is TRUE reference semantics for lists (heap-backed) on the proof side?

Question (user, 2026-07-11): Python lists are references (int/str/tuple are value-like); our
semantics models lists as values, which is why `.append` is a canonical gap. If lists lived in
a heap behind `lref(Loc)`, mutation would be faithful — what does that cost in kprove?
**Verdict: FULLY PROVABLE — all three legs #Top after adopting the update-vs-cons discipline
below. The loop invariant over a heap-resident accumulator proves, including with a second live
ref and a symbolic heap frame; entries prove from BOTH a concrete initial heap and a fully
symbolic one.** The cost is bookkeeping (one exposed binding per live list, one distinctness
premise per pair) plus one hard-won discipline: keep the symbolic heap in CONS-form everywhere —
an update-form `H[N <- _]` never re-normalizes symbolically, even with freshness in the path
condition (stdlib rule 418 fires neither inside recorded equations nor on goal conditions).

```sh
cd verification/humaneval/reference/notes/heap-list-probe
kompile verif-heap.k --backend haskell --main-module VERIF-HEAP --syntax-module VERIF-HEAP --output-definition verif-heap-kompiled
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 500 kprove spec-<leg>.k --definition verif-heap-kompiled --spec-module SPEC-<LEG>-SPEC --depth 2000
```

The model: `<heap> Loc |-> ValSeq </heap>` + `<nextref>` allocator; `Val ::= Int | lref(Int)`;
append = in-place heap update `P |-> (L => vSnoc(L, V))`; summary `appAll(A, VS)`.

| leg | claim shape | result |
| --- | --- | --- |
| [tworef](spec-tworef.k) | loop invariant, TWO live refs + symbolic frame, `requires P =/=Int Q` | **#Top** |
| [entry-empty](spec-entry-empty.k) | invariant + entry from CONCRETE `.Map` heap (production shape) | **#Top** |
| [oneref](spec-oneref.k) | same invariant + entry from a SYMBOLIC heap `H` with fresh `N` | **#Top** after the fixes below (originally FAIL) |

## The update-vs-cons wall, and the three-step fix (probed one failure at a time)

1. Original FAIL: the allocation rule produced `H[N <- .ValSeq]` (update-FORM). The invariant's
   cons-form pattern `P |-> L HR` can't unify with it; the prover records
   `{H[N <- .ValSeq] #Equals HR N |-> L}` as an unsolved constraint and the entry never closes.
   Stdlib's `M[K <- V] => K |-> V M requires notBool K in_keys(M)` (domains.md:418) fires
   NEITHER inside that equation NOR on goal conditions, despite the freshness premise being in
   the path condition.
2. Fix 1 — an ML-level DECOMPOSITION lemma (same layer as the casts round-trip):
   `{M[K <- V] #Equals (K |-> W REST)} => {V #Equals W} #And {M #Equals REST}` under freshness
   of K for both rests (+ mirrored orientation). This discharges update-vs-cons equations in
   RECORDED constraints — the non-empty branch then closes — but not in GOAL conditions
   (the `#Not(...)` obligation of the final implication is out of the simplifier's reach).
3. Fix 2 — state the claim's postcondition heap in CONS-form (`N |-> appAll(...) H`, not
   `H[N <- appAll(...)]`). Kills the goal-side equation for the branch that ran the loop; the
   EMPTY-input branch still fails (its heap never left update-form).
4. Fix 3 — the allocation RULE emits cons-form directly:
   `<heap> H => (N |-> .ValSeq) H </heap> requires notBool N in_keys(H)`. No update-form ever
   exists; all three legs #Top. (With this, fix 1's lemma may be redundant — kept as belt and
   suspenders for equations that form via other routes.)

DISCIPLINE for a future heap semantics: allocation and write rules emit cons-form; claims state
heaps in cons-form; never rely on `M[K <- V]` normalizing under a symbolic M.

## Reading

- The invariant machinery is ALREADY ours: the heap cell + exposed binding + symbolic frame is
  exactly the shape of our existing `<store> ... L |-> scope(...) ... </store>` claims — the
  store IS a heap (nextLoc allocator, framing, pinning). Adding `lref` extends the architecture,
  it does not invent one.
- Costs that scale with the corpus:
  1. every list-touching claim gains the heap binding for each LIVE list (one extra exposed
     `P |-> …` per list, like scopes today);
  2. one `P =/=Int Q` distinctness premise per PAIR of live lists in an invariant (tworef shows
     the prover is happy once told);
  3. allocation must stay at CONCRETE refs in entry claims (it already does — nextLoc pinning;
     the oneref failure is exactly what havocking the allocator costs, consistent with the
     minimal-cells probe finding).
- What it buys: faithful `.append`/`.sort()`/item-assignment (25/6/5 problems currently gapped),
  aliasing handled CORRECTLY instead of excluded by rewrite — the function-trap-adjacent
  rewrites (`result = result + [e]`) disappear from solution.py.
- What it costs beyond the probe: a full-corpus migration — every list argument becomes a ref,
  entry claims allocate the input lists, all 164 proofs' claims change shape. The probe says
  none of it is prover-blocked; it is volume, not risk.
