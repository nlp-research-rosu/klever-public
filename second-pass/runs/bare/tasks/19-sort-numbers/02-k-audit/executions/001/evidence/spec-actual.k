requires "audit-verification.k"

module SPEC-ACTUAL
  imports AUDIT-VERIFICATION

  claim <k> auditActualSolutionProgram ~> invoke(S)
         => VStr(sortSpec(S)) </k>
endmodule
