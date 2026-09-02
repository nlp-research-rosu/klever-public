requires "verification.k"

module SPEC-ENTRY-2
  imports VERIFICATION

  claim <k> solutionProgram ~> invoke("three one five")
         => VStr("one three five") </k>
endmodule
