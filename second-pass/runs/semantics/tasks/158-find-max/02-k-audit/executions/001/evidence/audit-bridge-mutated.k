requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-MUTATED
  imports MPY

  syntax AuditMutWordSeq ::= ".AuditMutWordSeq"
                            | amwCons(IntSeq, AuditMutWordSeq)
  syntax ValSeq ::= auditMutWordVals(AuditMutWordSeq) [function, total]

  rule auditMutWordVals(.AuditMutWordSeq) => .ValSeq
  // Deliberate sensitivity mutation: replace every yielded word by "".
  rule auditMutWordVals(
         amwCons(_:IntSeq, REST:AuditMutWordSeq))
    => vCons(str(.IntSeq), auditMutWordVals(REST))
endmodule
