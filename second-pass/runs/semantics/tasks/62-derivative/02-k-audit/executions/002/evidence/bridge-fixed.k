requires "reference-semantics/semantics.k"

module BRIDGE-FIXED
  imports MPY

  syntax IntVals ::= ".IntVals"
                   | ivCons(Int, IntVals)
  syntax ValSeq ::= asValSeq(IntVals) [function, total]
  rule asValSeq(.IntVals) => .ValSeq
  rule asValSeq(ivCons(I:Int, REST:IntVals))
    => vCons(I, asValSeq(REST))
endmodule
