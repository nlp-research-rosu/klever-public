requires "/tmp/audit-work/reconstruct-001/reference-semantics/semantics.k"

module AUDIT-DYNAMIC-CONNECTION
  imports MPY

  syntax Bool ::= auditDefinedStr(Val) [function, total]
  rule auditDefinedStr(V:Val) => isStr(V)

  syntax Str ::= auditProjectStr(Val)
    [function, total, symbol(auditProjectStr), no-evaluators]

  rule #Ceil({@V:Val}:>Str)
    => ({ auditDefinedStr(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule auditProjectStr(V:Val) => {V}:>Str
    requires auditDefinedStr(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Str => auditProjectStr(V)
    requires auditDefinedStr(V)
    [symbolic(V), simplification, preserves-definedness]
  rule auditProjectStr(S:Str) => S [simplification]
  rule auditProjectStr(auditProjectStr(V)) => auditProjectStr(V)
    [simplification]

  syntax IntSeq ::= auditCodesOf(Str) [function, total]
  rule auditCodesOf(str(CS)) => CS
endmodule
