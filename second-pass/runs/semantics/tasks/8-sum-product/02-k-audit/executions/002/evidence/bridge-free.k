requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-FREE
  imports MPY

  syntax ValSeq ::= intVals(IntSeq)
endmodule

module AUDIT-BRIDGE-FREE-PROBE
  imports AUDIT-BRIDGE-FREE

  claim [int-vals-one-step]:
    <k>
      #iterNext(list(intVals(iCons(2, .IntSeq))))
      => #iterYield(2, list(intVals(.IntSeq)))
    </k>
endmodule
