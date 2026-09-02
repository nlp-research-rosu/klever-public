requires "verification.k"

module SPEC-ENTRY-3
  imports VERIFICATION

  claim <k> solutionProgram ~> invoke("two two one zero two")
         => VStr("zero one two two two") </k>
endmodule
