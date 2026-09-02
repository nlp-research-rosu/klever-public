// verification.k — has_close_elements on the UNIFIED semantics. Any two elements closer than a
// threshold? The Q43 pairs_sum_to_zero NESTED-LOOP existential (found accumulator over i<j) with the
// FLOAT proximity test instead of the int sum. solution.py rewrites the early `return True` as a
// sticky `found` and the inner loop as `range(idx+1, n)` (symmetric compare, so i<j suffices) — the
// Q43 shape exactly (diff-tested 0 mismatches). The per-pair test `abs(a-b) < t` is a SINGLE opaque
// float Bool per branch (subF/absF/floatLt, no-evaluators — no nonlinear cascade), so the existential
// STRUCTURE is verified and the float arithmetic is trusted (real in krun). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module HAS-CLOSE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // isFloat-bridge echo: numbers[i] - numbers[j] on symbolic float elements -> opaque subF.
  rule applyBin("-", valSeqAt(VS:ValSeq, I:Int), valSeqAt(VS:ValSeq, J:Int))
    => subF(projectFloatTotal(valSeqAt(VS, I)), projectFloatTotal(valSeqAt(VS, J)))
    requires allFloat(VS) [simplification]

  // the deref narrower junk-branches numbers[i] into a {valSeqAt(VS,I) #Equals ref(_)} case; the
  // shared killers (lemmas/subscript.k) only carry the allInt guard, so under allFloat the ref
  // branch survives and the subF bridge can't fire -> grind. The allFloat twins refute it (a float
  // element is never a ref), same declare-then-guard idiom as the allInt originals.
  rule { ref(_:Int) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom
    requires allFloat(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals ref(_:Int) } => #Bottom
    requires allFloat(VS) [simplification]

  // the per-pair proximity test abs(numbers[i]-numbers[j]) < t (composed opaque float Bool).
  syntax Bool ::= closePair(ValSeq, Int, Int, Float) [function, total]
  rule closePair(VS:ValSeq, I:Int, J:Int, T:Float)
    => floatLt(absF(subF(projectFloatTotal(valSeqAt(VS, I)), projectFloatTotal(valSeqAt(VS, J)))), T) [simplification]

  // inner fold over j in [J, N): found becomes true if any pair (i, j) is close (i fixed). Guarded
  // case-split (Q43 primeAcc pattern) on closePair.
  syntax Bool ::= innerFold(Int, Int, Int, ValSeq, Float, Bool) [function, total]
  rule innerFold(J:Int, N:Int, _I:Int, _VS:ValSeq, _T:Float, F:Bool) => F requires J >=Int N [simplification]
  rule innerFold(J:Int, N:Int, I:Int, VS:ValSeq, T:Float, _F:Bool) => innerFold(J +Int 1, N, I, VS, T, true)
    requires J <Int N andBool closePair(VS, I, J, T) [simplification]
  rule innerFold(J:Int, N:Int, I:Int, VS:ValSeq, T:Float, F:Bool) => innerFold(J +Int 1, N, I, VS, T, F)
    requires J <Int N andBool notBool closePair(VS, I, J, T) [simplification]

  // outer fold over i in [I, N): each runs the inner fold over (i+1, N).
  syntax Bool ::= outerFold(Int, Int, ValSeq, Float, Bool) [function, total]
  rule outerFold(I:Int, N:Int, _VS:ValSeq, _T:Float, F:Bool) => F requires I >=Int N [simplification]
  rule outerFold(I:Int, N:Int, VS:ValSeq, T:Float, F:Bool)
    => outerFold(I +Int 1, N, VS, T, innerFold(I +Int 1, N, I, VS, T, F)) requires I <Int N [simplification]

  syntax Bool ::= hceRes(ValSeq, Float) [function]
  rule hceRes(VS:ValSeq, T:Float) => outerFold(0, vsLen(VS), VS, T, false) [simplification]
endmodule
