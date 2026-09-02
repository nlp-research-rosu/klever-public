requires "audit-verification.k"

module SPEC-ALIAS-IDENTITY
  imports AUDIT-VERIFICATION

  claim <k> solutionProgram => auditActualSolutionProgram </k>
endmodule
