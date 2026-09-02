requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation. A = 30 satisfies the original A < 100 domain,
  // the real program returns true, and this result obligation requires false.
  claim
    <k> solutionProgram => .K </k>
    <arg> A </arg>
    <env> .Map </env>
    <result>
      noResult => Bool(false)
    </result>
    requires A ==Int 30
endmodule
