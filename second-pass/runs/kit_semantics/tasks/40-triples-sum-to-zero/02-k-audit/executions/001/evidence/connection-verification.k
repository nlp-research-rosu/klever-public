requires "reference-semantics/semantics.k"

module CONNECTION-VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // Auditor-local copies of the representation and indexing definitions.
  // The candidate's vsLen/valSeqAt simplification rules are intentionally absent.
  syntax ValSeq ::= auditIntVals(IntSeq) [function, total]
  rule auditIntVals(.IntSeq)                => .ValSeq
  rule auditIntVals(iCons(I:Int, R:IntSeq)) => vCons(I, auditIntVals(R))

  syntax Int ::= auditIntAt(IntSeq, Int) [function, total, no-evaluators]
  rule auditIntAt(.IntSeq, _:Int) => 0
  rule auditIntAt(iCons(I:Int, _:IntSeq), 0) => I
  rule auditIntAt(iCons(_:Int, R:IntSeq), N:Int) => auditIntAt(R, N -Int 1)
    requires N >Int 0
  rule auditIntAt(iCons(_:Int, _:IntSeq), N:Int) => 0
    requires N <Int 0
endmodule
