requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-CORE

  // Proof-side representation of a Python list containing only integers.
  syntax ValSeq ::= intVals(IntSeq) [function, total]
  syntax Bool ::= nonNegative(IntSeq) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  rule intVals(.IntSeq) => .ValSeq
  rule intVals(iCons(I:Int, IS:IntSeq)) => vCons(I, intVals(IS))

  rule nonNegative(.IntSeq) => true
  rule nonNegative(iCons(I:Int, IS:IntSeq))
    => I >=Int 0 andBool nonNegative(IS)

endmodule
