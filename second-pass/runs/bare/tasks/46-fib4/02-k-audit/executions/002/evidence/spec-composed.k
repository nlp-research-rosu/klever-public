requires "spec.k"

module SPEC-COMPOSED
  imports SPEC

  // Reviewer-derived composition of the candidate's separately proved
  // initialization and loop reachability claims.
  claim [fib4-ge4-composed]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> N </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(fib4Spec(N)) </result>
    </fib4>
    requires N >=Int 4
endmodule
