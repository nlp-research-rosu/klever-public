requires "verification.k"

module SPEC-ENTRY-5
  imports VERIFICATION

  claim <k> solutionProgram ~> invoke("") => VStr("") </k>
endmodule
