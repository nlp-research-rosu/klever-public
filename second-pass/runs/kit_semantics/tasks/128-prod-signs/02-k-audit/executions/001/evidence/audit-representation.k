requires "summaries.k"

module AUDIT-REPRESENTATION
  imports PROD-SUMMARIES

  // Independent transparent model of the intended IntSeq-to-ValSeq map.  This
  // audit-only definition contains neither connection.k's contextual rules nor
  // verification-base.k's iterator bridge.
  syntax ValSeq ::= auditIntVals(IntSeq) [function, total]
  rule auditIntVals(.IntSeq) => .ValSeq
  rule auditIntVals(iCons(VALUE:Int, REST:IntSeq))
    => vCons(VALUE, auditIntVals(REST))
endmodule
