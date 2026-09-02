# Proving a sort correct — the sortedness kernel DOES prove (execution-driven, not buried)

The question (yuqing): can we *prove* (not trust) that a simple sort yields a sorted output? The
cleanest kernel is insertion sort's `insert` preserving sortedness:
`isSorted(insert(X, L)) == true` given `isSorted(L)`, by induction on `L`.

An earlier version of this probe concluded "won't induct as a function claim — needs a framework."
**That was the wrong formulation, not a real wall.** Driven correctly, the kernel proves.

```sh
cd verification/humaneval/reference/notes/sort-probe
kompile verif.k --backend haskell --main-module SORT --syntax-module SORT --output-definition verif-kompiled
# WIN  — execution-driven bounded circularity:
kprove spec.k        --definition verif-kompiled --spec-module SORT-SPEC        --depth 3000   # #Top
# FAIL — the bare buried-function lemma (the contrast):
kprove spec-buried.k --definition verif-kompiled --spec-module SORT-BURIED-SPEC --depth 3000   # stuck
```

## The mistake: a buried function term ([`spec-buried.k`](spec-buried.k), FAILS)

`claim run(isSorted(insert(X, L))) => true requires isSorted(L)`. Stuck state:
`isSorted(insert(X, L))` **unreduced** — for a symbolic `L`, `insert(X, L)` never fires because `L`
sits as a **function argument** inside `isSorted(insert(X, L))`, not a position the *execution* rules
match, so kprove never case-splits it. Same wall as `val-cast` / `intlist`: a symbolic variable
splits only where rewrite rules match its constructors **in the `<k>` cell**.

## The fix: drive `insert` through the `<k>` open as a bounded circularity ([`spec.k`](spec.k), `#Top`)

This is exactly how K's own `insertion-sort-spec.k` does it
(`references/k-repos/kframework/java-semantics/src/verification/`): a loop/recursion invariant that
**`requires sorted(prefix)` and `ensures sorted(result)`**, carrying the head bound. Mirrored here in
the minimal cons-list setting:

```k
claim <k> ind(B, X, L) => .K </k>
  requires isSorted(L) andBool B <=Int X andBool lbHead(B, L)
  ensures  isSorted(insert(X, L)) andBool B <=Int ihead(insert(X, L))
```

`ind(B, X, L)` case-splits `L` via its `<k>` rules (`.IntSeq` / `iCons(Y,R)`) and **recurses on the
tail `R` with the new bound `Y`** — a self-circularity, the same shape as `spec-control-seq`'s
`iloop`. Three pieces make the inductive step close:

1. **The lower bound `B`** threaded through the recursion. The `X > Y` case yields
   `iCons(Y, insert(X, R))`; its sortedness needs `Y <= head(insert(X, R))`. The strengthened
   `ensures ... B <= ihead(insert(X, L))` hands exactly that fact back from the recursive call —
   without it the obligation is unprovable (this is what sank the function-lemma form).
2. **`ihead(insert(...))` is non-inductive** — `head(insert(X, L))` depends only on `X` vs `L`'s
   first element (`= minInt(X, head L)`), so two finite simplification rules discharge it.
3. **A bridge** `isSorted(iCons(B, insert(X, R))) => B <= ihead(insert(X,R)) andBool isSorted(insert(X,R))`
   lets `isSorted` see past the still-opaque recursive `insert(X, R)` term (it is always nonempty).

**Result: `#Top`, non-vacuous.** Flipping `ensures isSorted(...)` to `notBool isSorted(...)` fails
(`#Top=0`), and — the sharper check — **dropping the `isSorted(L)` precondition also fails**, so the
proof genuinely uses it (insert into an unsorted list is not sorted). 0 parse errors both times.

## The full framework — insertion sort is proven a SORTED PERMUTATION

All three levels now close in kprove (each `#Top`, non-vacuous):

| level | file | claim |
|---|---|---|
| **ordering kernel** | [`spec.k`](spec.k) | `isSorted(L) ⇒ isSorted(insert(X, L))` (bound-carrying circularity) |
| **permutation kernel** | [`spec-perm.k`](spec-perm.k) | `count(Y, insert(X, L)) == count(Y, X::L)` for a symbolic witness `Y` |
| **full sort** | [`spec-sort.k`](spec-sort.k) | `isSorted(sortL(L)) ∧ count(Y, sortL(L)) == count(Y, L)` — sortL is a **sorted permutation** |

```sh
kompile verif.k      --backend haskell --main-module SORT      --syntax-module SORT --output-definition verif-kompiled
kompile verif-full.k --backend haskell --main-module SORT-FULL --syntax-module SORT --output-definition verif-full-kompiled
kprove spec.k        --definition verif-kompiled      --spec-module SORT-SPEC        # ordering    #Top
kprove spec-perm.k   --definition verif-kompiled      --spec-module SORT-PERM-SPEC   # permutation #Top
kprove spec-sort.k   --definition verif-full-kompiled --spec-module SORT-FULL-SPEC   # full sort   #Top
```

### The permutation half (the piece that was "remaining")

Multiset equality via an **occurrence count** `count(Y, L)` for a symbolic witness `Y` (proving it for
an arbitrary `Y` = proving multiset equality). The key: `count` peels the cons **unconditionally**
with `#if Z==Y #then 1 #else 0 #fi` (never deciding `Y`), so it **reduces past the opaque recursive
`insert(X,R)`** — the outer cons is always visible. No bound needed (unlike the ordering half): a
clean structural induction on `L`, self-circularity on the tail. Guarded `count` rules (like the
per-problem summaries) get stuck here because the witness's equality is a free symbolic, undecided.

### The full lift (`verif-full.k`)

`sortL(L) = fold insert` over `L`. Structural induction on `L`, using the two kernels as
`[simplification]` lemmas (sound — each is proven separately against module `SORT`, which
`verif-full.k` does not touch). The step: `sortL(X::R) = insert(X, sortL(R))`; ordering follows from
`isSorted(insert(X,·))⇐isSorted(·)` + IH `isSorted(sortL(R))`; permutation from
`count(Y,insert(X,·))=count(Y,X::·)` + IH `count(Y,sortL(R))=count(Y,R)`.

## Bottom line

**A sort is now proven fully correct in K — trusting it is no longer necessary.** The trusted-sort
proofs (88, 34, 58, 149, 120, 47) rest on exactly the two facts now discharged here
(`isSorted(sortI(L))`, `isPerm(sortI(L), L)`), so their trust boundary is **backed by proof**, not
assumption. Applying the framework to problems that *iterate* the sorted output (33/37/105) is the
next step: introduce the sorted result as a symbolic variable carrying `isSorted` + `count`-equality,
then reason about the scatter/interleave over it.
