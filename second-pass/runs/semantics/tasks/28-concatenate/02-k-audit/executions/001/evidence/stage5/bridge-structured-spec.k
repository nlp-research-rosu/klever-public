requires "/tmp/audit-work/28-concatenate/bridge-baseline.k"

module AUDIT-BRIDGE-STRUCTURED-SPEC
  imports AUDIT-BRIDGE-BASELINE

  // Structural instance of the fixed semantics rule. This is narrower than
  // the candidate rule's Boolean guard and therefore is supporting evidence,
  // not the required complete-guard connection theorem.
  claim [fixed-string-addition-instance]:
    <k>
      applyBin("+", str(A:IntSeq), str(B:IntSeq))
      =>
      str(seqConcat(A, auditStringCodes(str(B))))
    </k>
endmodule
