requires "audit-dynamic-connection.k"

module AUDIT-DYNAMIC-CONNECTION-SPEC
  imports AUDIT-DYNAMIC-CONNECTION

  claim [set-full-guard-domain]:
    <k>
      applyBuiltin("set", V:Val, .Vals)
      => setV(dedupCodes(auditCodesOf(auditProjectStr(V))))
    </k>
    requires auditDefinedStr(V)

  claim [lt-full-guard-domain]:
    <k>
      applyCmp("<", A:Val, B:Val)
      => strLt(
           auditCodesOf(auditProjectStr(A)),
           auditCodesOf(auditProjectStr(B)))
    </k>
    requires auditDefinedStr(A) andBool auditDefinedStr(B)
endmodule
