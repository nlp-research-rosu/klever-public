requires "verification-core.k"

module SPEC-CORE
  imports VERIFICATION-CORE

  claim <k> solutionProgram ~> invoke(S) => VStr(coreSortSpec(S)) </k>
endmodule
