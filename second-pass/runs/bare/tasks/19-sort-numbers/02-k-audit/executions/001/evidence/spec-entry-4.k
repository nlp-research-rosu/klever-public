requires "verification.k"

module SPEC-ENTRY-4
  imports VERIFICATION

  claim <k> solutionProgram ~> invoke(
           "nine eight seven six five four three two one zero")
         => VStr(
           "zero one two three four five six seven eight nine") </k>
endmodule
