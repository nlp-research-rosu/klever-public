requires "semantic.k"

module SPEC-VACUITY
  imports SEMANTIC

  // Fresh audit mutation: the real n == 2 branch returns 2, not 3.
  // The initial state is realizable and has no additional precondition.
  claim [fib4-base-2-false]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> 2 </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(3) </result>
    </fib4>
endmodule
