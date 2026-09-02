requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: demand the logical complement of the real result.
  // Satisfying counterexample A=30: the program returns true, but this demands
  // false because isThreePrimeProductBelow100(30) is true.
  claim
    <k> solutionProgram => .K </k>
    <arg> A </arg>
    <env> .Map </env>
    <result>
      noResult => Bool(notBool isThreePrimeProductBelow100(A))
    </result>
    requires A <Int 100
endmodule
