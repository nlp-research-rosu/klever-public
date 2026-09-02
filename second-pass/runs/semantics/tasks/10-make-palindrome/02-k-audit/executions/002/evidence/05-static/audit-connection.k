requires "reference-semantics/semantics.k"

module AUDIT-CONNECTION
  imports MPY

  // Independent copy of the candidate's mathematically standard prefix
  // definition. No candidate operational bridge is imported.
  syntax IntSeq ::= auditPrefixIS(IntSeq, Int) [function]
  rule auditPrefixIS(_:IntSeq, N:Int) => .IntSeq requires N <=Int 0
  rule auditPrefixIS(iCons(C:Int, R:IntSeq), N:Int)
    => iCons(C, auditPrefixIS(R, N -Int 1))
    requires N >Int 0

endmodule
