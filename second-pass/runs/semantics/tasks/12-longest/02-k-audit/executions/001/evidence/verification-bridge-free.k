requires "../candidate-src/reference-semantics/semantics.k"

module VERIFICATION-BRIDGE-FREE
  imports MPY

  syntax StringSeq ::= ".StringSeq"
                     | sCons(IntSeq, StringSeq)

  syntax ValSeq ::= stringVals(StringSeq)
  rule stringVals(.StringSeq) => .ValSeq
  rule stringVals(sCons(CS:IntSeq, REST:StringSeq))
    => vCons(str(CS), stringVals(REST))
endmodule
