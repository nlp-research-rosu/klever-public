requires "semantic.k"

module SPEC-VACUITY
  imports SEMANTIC

  // Fresh audit mutation: fib4(7) is 14, so requiring 15 is meaningful,
  // reachable, result-constraining, and false.
  claim [false-fib4-seven]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> 7 </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(15) </result>
    </fib4>
endmodule
