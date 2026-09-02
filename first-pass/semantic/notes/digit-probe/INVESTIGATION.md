# Probe — the digits of a SYMBOLIC integer in a proof

Question: the deferred cluster (#68, #73, #74, #75, #76, #79, #80 — plus queued #86, #107,
#108, #113) is blocked because `str(N)` / `bin(N)` on a *symbolic* integer compiles to
`Int2String(N)`, which is stuck (kprove can't compute the digits of an unknown integer). How
far can we get modelling the digits directly?

```sh
cd verification/humaneval/reference/notes/digit-probe
kompile verif.k --backend haskell --main-module VERIF --syntax-module VERIF --output-definition verif-kompiled
# then capped (cap-kprove-memory):
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet timeout 200 \
  kprove spec-peel.k --definition verif-kompiled --spec-module PEEL-SPEC --depth 2000
```

## Experiments

| spec | claim | result |
| --- | --- | --- |
| `spec-peel` | `#peel(N,A) => evenOfInt(N,A)` — arithmetic `while n>0 { acc+=ev(n%10); n/=10 }` | **PASS `#Top`** |
| `spec-peel-nv` | same with RHS `+Int 1` (corruption) | **not `#Top`** (peel proof is non-vacuous) |
| `spec-seqfold` | `#iter(DS,A) => evenSeq(DS,A)` — fold over a symbolic digit sequence | **PASS `#Top`** |
| `spec-roundtrip` | `digitCodes(intOf(DS)) => DS`, `validDec(DS)` — the bridge | **STUCK** (not provable) |
| `spec-iter-int` | `#iter(digitCodes(N),0) => …` — iterate `str(N)` for symbolic `N` | **STUCK** |

## Findings

1. **Arithmetic digit-peel closes by induction on N.** `while n>0 { acc += f(n%10); n //= 10 }`
   reduces to its `/Int 10` recurrence summary and kprove discharges it to `#Top` (and the
   corruption fails, so it's meaningful). No new semantics, no trust — the reference already
   has `%`/`//`/`while`. This is the sound path.

2. **Iterating `str(N)` for symbolic `N` is a dead end.** `str(N) = digitCodes(N)` is a *frozen*
   term for symbolic `N` (the base case `N<10` is never concretely reached), so `#iterNext`
   can't peel its head — `spec-iter-int` is STUCK. Confirms you cannot keep `solution.py`'s
   `for i in str(n)` and merely add a `digitCodes` model; the loop won't unfold.

3. **The round-trip bridge, posed naively, does not START (NOT the same as "unprovable").**
   `digitCodes(intOf(DS)) = DS` as a bare equality over an *unconstrained* `DS` never rewrites:
   `intOfAcc(DS, 0)`'s rules match only `.IntSeq` / `iCons`, so nothing fires on an abstract
   variable; kprove falls straight to the terminal implication `DS = digitCodes(intOf(DS))` and
   can't discharge it (see `roundtrip.out` — "unifies … but the implication check … failed").
   This is a "didn't begin," because kprove is a *reachability* prover and won't spontaneously
   do structural induction on `DS`. Whether the round-trip is provable via a properly-structured
   inductive claim is **UNTESTED here** — do not read this row as "the theorem is false." (It is
   moot for the plan anyway: per the design decision, the `str(N)` ⇄ peel equivalence is *domain
   reasoning for Klean/Lean*, not a K obligation — K only needs the peel, which proves.)

4. **Folds over a symbolic digit sequence close** (`spec-seqfold`) — the "back half" is fine
   once you *have* a cons-structured sequence to fold.

5. **Totality is not the blocker** (tested — `verif2.k`, `roundtrip-total.out`). Declaring
   `intOf`/`intOfAcc`/`digitCodes` `[total]` drops the `#Ceil(...)` definedness obligations
   from the residual but leaves the core `#Not(DS #Equals digitCodes(intOf(DS)))` unchanged —
   still stuck. The blocker is that `DS` is buried inside `digitCodes(intOf(DS))` and never gets
   destructured, so kprove (a reachability prover) never case-splits `DS = .IntSeq / iCons`,
   which is what induction needs.

6. **Rewrite-form is the right tool — for the iteration, which is what we need.** The passing
   `#peel` (finding 1) *is* a `<k>`-cell rewrite that narrows `N` (`N>0`/`N<=0` split) and
   recurses — exactly the [[loop-dispatch-must-be-rewrite-rules]] pattern. So "a rewrite form,
   not a function form, solves it" holds for the digit *iteration*. `#peel` is the sound K
   artifact, and `str(N) ⇄ #peel` is the Klean domain lemma; we never need the round-trip.

7. **Rewrite-form applied to the round-trip itself (`verif3.k`): moves the frontier but doesn't
   finish.** Making `intOf`/`digitCodes` `<k>`-cell rewrites (`#intOf` destructures `DS`,
   `#digits` narrows `N`) — instead of frozen functions — lets kprove narrow on structure:
   - **fixed-length** `DS = [C, D]` with symbolic digit *values* → **`#Top`, non-vacuous**
     (`rt3-fixed2`): narrowing + SMT on the Horner arithmetic (`V/10=C-48`, `V%10=D-48`) closes it.
   - **unbounded** symbolic `DS` → still stuck (`rt3-unbounded`), now because `#intOf` collapses
     `DS` to a *monolithic integer* at the hand-off, leaving no cons-structure for an automatic
     circularity. Unbounded would need an **explicit inductive lemma** (strengthened
     Horner-inverse) — the rewrite form lets induction start but not close for free.

   Net: function→rewrite moved the round-trip from *totally stuck* to *bounded-proves,
   unbounded-needs-explicit-induction*. Still moot for the plan (`#peel` is the sound path).

## The deep reason (why the rewrite is the natural form, not a workaround)

A symbolic integer's digits are only reachable **least-significant-first**: `N % 10` is a
concrete symbolic term, `N // 10` is the strictly-smaller remainder — a clean decreasing
measure kprove inducts on. `str(N)` presents the digits **most-significant-first**, and the
leading digit depends on `⌊log₁₀ N⌋`, which is *not* reachable for symbolic `N`. So the
`%10`//`10` rewrite isn't a convenience — it's the only direction in which a symbolic integer's
digits are accessible to the prover.

## Conclusion

Model nothing new. **Rewrite each solution's `str(n)`/`bin(n)` digit processing to arithmetic
peel** (`%10`//`10`, or `%2`//`2` for binary; Horner `v=v*10+(c-48)` for the `str→int`
direction in #79). This is a behavior-preserving rewrite (a documented Canonical gap, like the
other 45) and it *proves*, with no reference change and no trusted bridge. The output-string
cases (#75/#80 build a binary string, #76 a decimal join) build the string by prepending each
peeled digit — the same `rev = c + rev` accumulator pattern already used by #7/#47/#52.
