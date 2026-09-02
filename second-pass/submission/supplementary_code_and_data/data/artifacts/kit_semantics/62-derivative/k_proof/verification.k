requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The list accumulated by the source loop after processing the remaining
  // coefficients VS, starting at source index I.
  syntax ValSeq ::= derivAcc(ValSeq, ValSeq, Int) [function]
  rule derivAcc(ACC:ValSeq, .ValSeq, _I:Int) => ACC [simplification]
  rule derivAcc(ACC:ValSeq, vCons(_V:Val, REST:ValSeq), I:Int)
    => derivAcc(ACC, REST, I +Int 1)
    requires notBool (I >Int 0)
    [simplification]
  rule derivAcc(ACC:ValSeq, vCons(V:Val, REST:ValSeq), I:Int)
    => derivAcc(
         valSeqConcat(ACC, vCons(applyBin("*", I, V), .ValSeq)),
         REST,
         I +Int 1)
    requires I >Int 0
    [simplification]

  // Heap references are operational handles, not self-contained read-only
  // input values. This predicate admits every self-contained Val constructor.
  syntax Bool ::= noRefsVS(ValSeq) [function, total]
  rule noRefsVS(.ValSeq) => true
  rule noRefsVS(vCons(V:Val, REST:ValSeq))
    => notBool isRefV(V) andBool noRefsVS(REST)
endmodule
