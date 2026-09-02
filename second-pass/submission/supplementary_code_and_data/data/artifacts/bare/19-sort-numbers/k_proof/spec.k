requires "verification.k"

module SPEC
  imports VERIFICATION

  // Main theorem: for every String (and hence every input admitted by the
  // prompt), executing the translated implementation returns the canonical
  // ascending rendering with multiplicities preserved.
  claim <k> solutionProgram ~> invoke(S) => VStr(sortSpec(S)) </k>

  // Ground instances make the prompt example, multiplicities, all ten words,
  // and the empty boundary case independently visible in proof output.
  claim <k> solutionProgram ~> invoke("three one five")
         => VStr("one three five") </k>

  claim <k> solutionProgram ~> invoke("two two one zero two")
         => VStr("zero one two two two") </k>

  claim <k> solutionProgram ~> invoke(
           "nine eight seven six five four three two one zero")
         => VStr(
           "zero one two three four five six seven eight nine") </k>

  claim <k> solutionProgram ~> invoke("") => VStr("") </k>
endmodule
