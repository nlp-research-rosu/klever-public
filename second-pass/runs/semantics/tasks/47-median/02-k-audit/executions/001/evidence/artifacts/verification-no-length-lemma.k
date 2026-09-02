requires "reference-semantics/semantics.k"

module MEDIAN-VERIFICATION
  imports MPY

  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(_:Int, VS:ValSeq)) => allInts(VS)
  rule allInts(vCons(_:Val, _:ValSeq)) => false [owise]

  syntax Int ::= sortedIntAt(ValSeq, Int)
    [function, total, symbol(sortedIntAt), no-evaluators]
  rule valSeqAt(sortVS(VS:ValSeq), I:Int) => sortedIntAt(VS, I)
    requires allInts(VS)
     andBool I >=Int 0
     andBool I <Int vsLen(VS)
    [simplification]
endmodule
