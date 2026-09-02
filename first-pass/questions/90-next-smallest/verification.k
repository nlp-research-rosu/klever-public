// verification.k — next_smallest on the UNIFIED semantics. Two-pass over a symbolic List[int]:
// pass 1 finds min1 (min-scan, #35 maxFold dual); pass 2 finds the smallest element strictly
// greater than min1 (the 2nd-smallest DISTINCT), threading (found, m2). Elements are symbolic Vals
// under allInt, compared via projectIntTotal (the reference operator cast bridge). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module NEXT-SMALLEST-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL   // #if _ #then _ #else _ #fi in the entry postcondition

  syntax Expr ::= Val

  // ---- PASS 1: minFold(VS, M) = min of M and every element of VS (strict < keeps the earlier on
  // ties). The two recursive rules split on the body's `if x < min1` — they line up with the
  // program's If case-split. (The < dual of #35's maxFold.)
  syntax Val ::= minFold(ValSeq, Val) [function, total]
  rule minFold(.ValSeq, M:Val) => M [simplification]
  rule minFold(vCons(V:Val, S:ValSeq), M:Val) => minFold(S, V)
    requires projectIntTotal(V)  <Int projectIntTotal(M) [simplification]
  rule minFold(vCons(V:Val, S:ValSeq), M:Val) => minFold(S, M)
    requires projectIntTotal(V) >=Int projectIntTotal(M) [simplification]

  // ---- PASS 2 over VS, min1 = MIN1 (constant), a (found, m2) pair; body is
  //   if x > min1: if found: (if x < m2: m2 = x)   else: m2 = x; found = True
  // foundFold threads `found` (set True once any x > min1); m2Fold threads the running smallest
  // element that is > min1. Both branch-split on the SAME tests the body's nested Ifs make.
  syntax Bool ::= foundFold(ValSeq, Val, Bool) [function, total]
  rule foundFold(.ValSeq, _:Val, F:Bool) => F [simplification]
  rule foundFold(vCons(X:Val, S:ValSeq), MIN1:Val, _F:Bool) => foundFold(S, MIN1, true)
    requires projectIntTotal(X)  >Int projectIntTotal(MIN1) [simplification]
  rule foundFold(vCons(X:Val, S:ValSeq), MIN1:Val, F:Bool) => foundFold(S, MIN1, F)
    requires projectIntTotal(X) <=Int projectIntTotal(MIN1) [simplification]

  syntax Val ::= m2Fold(ValSeq, Val, Bool, Val) [function, total]
  rule m2Fold(.ValSeq, _:Val, _:Bool, M2:Val) => M2 [simplification]
  // x > min1, not yet found  -> seed m2 := x, found := True
  rule m2Fold(vCons(X:Val, S:ValSeq), MIN1:Val, false, _M2:Val) => m2Fold(S, MIN1, true, X)
    requires projectIntTotal(X)  >Int projectIntTotal(MIN1) [simplification]
  // x > min1, already found, x < m2  -> m2 := x
  rule m2Fold(vCons(X:Val, S:ValSeq), MIN1:Val, true, M2:Val) => m2Fold(S, MIN1, true, X)
    requires projectIntTotal(X)  >Int projectIntTotal(MIN1) andBool projectIntTotal(X)  <Int projectIntTotal(M2) [simplification]
  // x > min1, already found, x >= m2 -> keep m2
  rule m2Fold(vCons(X:Val, S:ValSeq), MIN1:Val, true, M2:Val) => m2Fold(S, MIN1, true, M2)
    requires projectIntTotal(X)  >Int projectIntTotal(MIN1) andBool projectIntTotal(X) >=Int projectIntTotal(M2) [simplification]
  // x <= min1 -> unchanged (found/m2 both threaded)
  rule m2Fold(vCons(X:Val, S:ValSeq), MIN1:Val, F:Bool, M2:Val) => m2Fold(S, MIN1, F, M2)
    requires projectIntTotal(X) <=Int projectIntTotal(MIN1) [simplification]

  // knownInt(V): a PROBLEM-LOCAL "V casts to an int" predicate. Unlike the shared definedProjectInt
  // (whose base rule `definedProjectInt(K) => isInt(K)` shadows any add-on and lands on the
  // undecidable isInt(minFold(..))), knownInt has NO base rule, so my minFold clause is the only
  // one — kore evaluates knownInt(minFold(T,H)) to true. This lets the entry discharge the pass-2
  // invariant's knownInt(min1) obligation (min1 = minFold(T,H), an opaque Val summary).
  syntax Bool ::= knownInt(Val) [function]
  rule knownInt(V:Val) => true requires isInt(V) [simplification]
  rule knownInt(minFold(VS:ValSeq, M:Val)) => true requires allInt(VS) andBool knownInt(M) [simplification]

  // junk-narrow falsity legs: the deref narrower SUBSTITUTES a claim variable
  // (min1 := ref(H)), so no {V #Equals ref(_)} equation survives for the
  // ML killers — the refutation must live in the predicate itself: the PC's
  // knownInt(ref(H)) atom evaluates false and bottoms the branch (okV pattern)
  rule knownInt(ref(_:Int))     => false [simplification]
  rule knownInt(cellRef(_:Int)) => false [simplification]

  // Cast-bridge variants keyed on knownInt: the shared bridge needs isInt(W), which kore can't
  // decide for minFold(T,H); knownInt(W) IS establishable, so echo the compare through it. Reduces
  // `x > minFold(T,H)` (entry head-unroll) AND `x > min1` / `x < m2` in the pass-2 invariant (which
  // carries knownInt(min1), knownInt(m2)) to the projected-int form foundFold/m2Fold expect.
  rule applyCmp(OP:String, V:Val, W:Val) => applyCmp(OP, projectIntTotal(V), projectIntTotal(W))
    requires isInt(V) andBool knownInt(W) [simplification]
  rule applyCmp(OP:String, V:Val, W:Val) => applyCmp(OP, projectIntTotal(V), projectIntTotal(W))
    requires knownInt(V) andBool isInt(W) [simplification]

  // The function's result: `m2 if found else None`, with min1 = minSeq = minFold(T, H) and the
  // pass-2 accumulators seeded (found=false, m2=0) and folded over the WHOLE list vCons(H, T).
  syntax Val ::= nextSmallest(Val, ValSeq) [function]
  rule nextSmallest(H:Val, T:ValSeq)
    => #if foundFold(vCons(H, T), minFold(T, H), false)
       #then m2Fold(vCons(H, T), minFold(T, H), false, 0)
       #else noneV #fi
    [simplification]
endmodule
