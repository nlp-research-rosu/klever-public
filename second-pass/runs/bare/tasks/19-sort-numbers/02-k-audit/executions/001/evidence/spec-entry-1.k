requires "verification.k"

module SPEC-ENTRY-1
  imports VERIFICATION

  claim <k> solutionProgram ~> invoke(S) => VStr(sortSpec(S)) </k>
endmodule
