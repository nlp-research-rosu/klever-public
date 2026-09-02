// verification.k — sum_squares on the UNIFIED semantics. Sum of ceil(i)**2 over a list of numbers
// (int or float). The sum is an EXACT INT (no compensated-sum issue). math.ceil is trusted:
// ceilF(V) is opaque for a symbolic element (kprove — structural) and concrete for krun (int
// identity / Float2Int(ceilFloat) — matches Python incl. negatives). See ./PROOF.md, mpy-float.k.

requires "../../reference/src/lemmas.k"

module SUM-SQUARES-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // squared = ACC + sum over the list of ceil(element)^2.
  syntax Int ::= sqFold(ValSeq, Int) [function, total]
  rule sqFold(.ValSeq, ACC:Int) => ACC [simplification]
  rule sqFold(vCons(V:Val, R:ValSeq), ACC:Int) => sqFold(R, ACC +Int ipow(ceilF(V), 2)) [simplification]

  syntax Val ::= sqRes(ValSeq) [function]
  rule sqRes(VS:ValSeq) => sqFold(VS, 0) [simplification]
endmodule
