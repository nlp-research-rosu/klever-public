requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-FREE
  imports MPY

  syntax WordSeq ::= ".WordSeq" | wCons(IntSeq, WordSeq)
  syntax ValSeq ::= wordVals(WordSeq) [function, total]

  rule wordVals(.WordSeq) => .ValSeq
  rule wordVals(wCons(WORD:IntSeq, REST:WordSeq))
    => vCons(str(WORD), wordVals(REST))
endmodule
