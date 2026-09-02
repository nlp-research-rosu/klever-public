requires "reference-semantics/semantics.k"

module CONCATENATE-NO-BRIDGE
  imports MPY

  syntax Bool ::= isStringValueNB(Val) [function, total]
  rule isStringValueNB(str(_:IntSeq)) => true
  rule isStringValueNB(_:Val) => false [owise]

  syntax IntSeq ::= stringCodesNB(Val) [function, total]
  rule stringCodesNB(str(S:IntSeq)) => S
endmodule
