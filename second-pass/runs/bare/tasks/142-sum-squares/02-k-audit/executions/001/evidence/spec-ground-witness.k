requires "verification.k"

module MPY-SPEC-GROUND-WITNESS
  imports MPY-VERIFICATION

  claim [ground-call-empty]:
    <k> invoke1("sum_squares", ListVal(.Ints))
      => VInt(0) </k>
    <functions> solutionFunctions </functions>
    <env> .Map => .Map </env>

  claim [ground-program-example]:
    <k> solutionProgram ~> run(ListVal(1, 2, 3))
      => VInt(6) </k>
    <functions> .Map => solutionFunctions </functions>
    <env> .Map </env>
endmodule
