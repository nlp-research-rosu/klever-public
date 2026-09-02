requires "/tmp/audit-work/28-concatenate/bridge-baseline.k"

module AUDIT-BRIDGE-CONNECTION-SPEC
  imports AUDIT-BRIDGE-BASELINE

  // This definition does not import the candidate's generalized applyBin rule.
  // It asks fixed supplied semantics to establish the same result on the
  // complete guard used by that candidate rule.
  claim [bridge-free-string-addition]:
    <k>
      applyBin("+", str(A:IntSeq), V:Val)
      =>
      str(seqConcat(A, auditStringCodes(V)))
    </k>
    requires auditIsStringValue(V)
endmodule
