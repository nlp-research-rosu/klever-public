requires "reference-semantics/semantics.k"

module INT-VAL-REP-NO-ITER-BRIDGE
  imports MPY

  syntax ValSeq ::= intValsNoIterBridge(IntSeq)

  rule intValsNoIterBridge(.IntSeq) => .ValSeq
  rule intValsNoIterBridge(iCons(I:Int, IS:IntSeq))
    => vCons(I, intValsNoIterBridge(IS))
endmodule
