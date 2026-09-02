requires "reference-semantics/semantics.k"

module VERIFICATION-NO-ITER-BRIDGE
  imports MPY

  syntax StringSeq ::= ".StringSeq"
                     | sCons(IntSeq, StringSeq)

  syntax ValSeq ::= stringVals(StringSeq)
  rule stringVals(.StringSeq) => .ValSeq
  rule stringVals(sCons(CS:IntSeq, REST:StringSeq))
    => vCons(str(CS), stringVals(REST))
endmodule
