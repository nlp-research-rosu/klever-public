requires "reference-semantics/semantics.k"

module MEDIAN-VERIFICATION
  imports MPY

  rule vsLen(sortVS(VS:ValSeq)) => vsLen(VS) [simplification]

  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(_:Int, VS:ValSeq)) => allInts(VS)
  rule allInts(vCons(_:Val, _:ValSeq)) => false [owise]

  syntax Int ::= sortedIntAt(ValSeq, Int)
    [function, total, symbol(sortedIntAt), no-evaluators]
endmodule
