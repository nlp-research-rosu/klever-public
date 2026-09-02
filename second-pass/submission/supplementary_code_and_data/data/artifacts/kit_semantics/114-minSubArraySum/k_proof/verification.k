requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The formal input domain is exactly the finite ValSeq values whose elements
  // are Python integers.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, XS:ValSeq)) => isInt(V) andBool allInts(XS)

  rule applyBin("+", I:Int, V:Val) => I +Int {V}:>Int
    requires isInt(V)
    [simplification]

  rule applyBuiltin("min", V:Val, I:Int, .Vals)
    => minInt({V}:>Int, I)
    requires isInt(V)
    [simplification]

  // Exact Kadane-fold summaries for the unprocessed suffix.
  syntax Int ::= kadaneCurrent(ValSeq, Int) [function]
  rule kadaneCurrent(.ValSeq, C:Int) => C
  rule kadaneCurrent(vCons(V:Val, XS:ValSeq), C:Int)
    => kadaneCurrent(
         XS,
         minInt({V}:>Int, C +Int {V}:>Int))
    requires isInt(V)

  syntax Int ::= kadaneMinimum(ValSeq, Int, Int) [function]
  rule kadaneMinimum(.ValSeq, _C:Int, B:Int) => B
  rule kadaneMinimum(vCons(V:Val, XS:ValSeq), C:Int, B:Int)
    => kadaneMinimum(
         XS,
         minInt({V}:>Int, C +Int {V}:>Int),
         minInt(B, minInt({V}:>Int, C +Int {V}:>Int)))
    requires isInt(V)
endmodule
