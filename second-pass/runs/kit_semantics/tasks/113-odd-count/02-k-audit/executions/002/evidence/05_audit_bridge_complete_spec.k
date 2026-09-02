requires "audit-bridge-base.k"

module AUDIT-BRIDGE-COMPLETE-SPEC
  imports AUDIT-BRIDGE-BASE

  claim [complete-match-domain]:
    <k>
      applyMethod(V:Val, "count", str(PATTERN:IntSeq), .Vals)
      =>
      cntSub(auditStringCodes(V), PATTERN)
    </k>
    requires auditIsStringVal(V)
endmodule
