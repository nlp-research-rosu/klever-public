requires "reference-semantics/semantics.k"

module BRIDGE-FREE
  imports MPY

  syntax WordSeq ::= ".WordSeq"
                   | wCons(IntSeq, WordSeq)
  syntax ValSeq ::= wordsVals(WordSeq)
  syntax IntSeq ::= sentenceCodes(WordSeq)
endmodule
