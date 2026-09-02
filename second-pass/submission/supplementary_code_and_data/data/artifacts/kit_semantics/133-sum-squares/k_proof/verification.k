requires "reference-semantics/semantics.k"
requires "program.k"

module VERIFICATION
  imports MPY
  imports SOLUTION-PROGRAM
  imports INT

  // Mathematical fold used only in postconditions.  It does not rewrite any
  // program computation; the Python loop continues to execute under MPY.
  syntax Int ::= sumCeilSquares(ValSeq) [function, total]
  rule sumCeilSquares(.ValSeq) => 0
  rule sumCeilSquares(vCons(V:Val, VS:ValSeq))
    => (ceilF(V) *Int ceilF(V)) +Int sumCeilSquares(VS)
endmodule
