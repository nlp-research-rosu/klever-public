requires "/tmp/audit-work/28-concatenate/reference-semantics/semantics.k"

module AUDIT-BRIDGE-BASELINE
  imports MPY

  syntax Bool ::= auditIsStringValue(Val) [function, total]
  rule auditIsStringValue(str(_:IntSeq)) => true
  rule auditIsStringValue(_:Val) => false [owise]

  syntax IntSeq ::= auditStringCodes(Val) [function]
  rule auditStringCodes(str(S:IntSeq)) => S
endmodule
