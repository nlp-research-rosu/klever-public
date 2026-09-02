requires "verification.k"

module SPEC
  imports VERIFICATION

  claim
    <k> solutionProgram => .K </k>
    <arg> A </arg>
    <env> .Map </env>
    <result>
      noResult => Bool(isThreePrimeProductBelow100(A))
    </result>
    requires A <Int 100
endmodule
