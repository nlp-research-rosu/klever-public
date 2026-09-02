requires "verification.k"

module SPEC-INDIVIDUAL
  imports VERIFICATION

  claim [main-symbolic]:
    <k> solutionProgram ~> invoke(S) => VStr(sortSpec(S)) </k>

  claim [example]:
    <k> solutionProgram ~> invoke("three one five")
       => VStr("one three five") </k>

  claim [duplicates]:
    <k> solutionProgram ~> invoke("two two one zero two")
       => VStr("zero one two two two") </k>

  claim [all-numerals]:
    <k> solutionProgram ~> invoke(
         "nine eight seven six five four three two one zero")
       => VStr(
         "zero one two three four five six seven eight nine") </k>

  claim [empty]:
    <k> solutionProgram ~> invoke("") => VStr("") </k>
endmodule
