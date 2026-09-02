requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-BASE-SYNTAX
  imports MPY

  syntax Bool ::= auditIsStringVal(Val) [function, total]
  syntax IntSeq ::= auditStringCodes(Val)
    [function, total, symbol(auditStringCodes), no-evaluators]
endmodule

module AUDIT-BRIDGE-BASE
  imports AUDIT-BRIDGE-BASE-SYNTAX
  imports MPY

  rule auditIsStringVal(str(_:IntSeq)) => true
  rule auditIsStringVal(_:Val) => false [owise]
  rule auditStringCodes(str(CODES:IntSeq)) => CODES [simplification]
endmodule
