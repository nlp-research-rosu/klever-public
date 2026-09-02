requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfying prompt-example input: the real result ends in
  // "five", not "four".
  claim <k> solutionProgram ~> invoke("three one five")
         => VStr("one three four") </k>
endmodule
