requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  syntax ValSeq ::= finishPile(ValSeq, Int, Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  rule finishPile(A:ValSeq, N:Int, I:Int) => A
    requires I >=Int N

  rule finishPile(A:ValSeq, N:Int, I:Int)
    => finishPile(
         valSeqConcat(A, vCons(N +Int (2 *Int I), .ValSeq)),
         N,
         I +Int 1)
    requires I <Int N
endmodule
