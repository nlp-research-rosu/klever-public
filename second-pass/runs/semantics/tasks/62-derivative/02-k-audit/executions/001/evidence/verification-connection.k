requires "reference-semantics/semantics.k"

module VERIFICATION-CONNECTION
  imports MPY
  imports MAP-SYMBOLIC

  syntax IntVals ::= ".IntVals"
                   | ivCons(Int, IntVals)

  syntax ValSeq ::= connectionAsValSeq(IntVals) [function, total]
  rule connectionAsValSeq(.IntVals) => .ValSeq
  rule connectionAsValSeq(ivCons(I:Int, REST:IntVals))
    => vCons(I, connectionAsValSeq(REST))

  syntax ValSeq ::= connectionEnum(IntVals, Int) [function]
  rule connectionEnum(.IntVals, _:Int) => .ValSeq
  rule connectionEnum(ivCons(I:Int, REST:IntVals), N:Int)
    => vCons(
         tuple(vCons(N, vCons(I, .ValSeq))),
         connectionEnum(REST, N +Int 1)
       )
endmodule
