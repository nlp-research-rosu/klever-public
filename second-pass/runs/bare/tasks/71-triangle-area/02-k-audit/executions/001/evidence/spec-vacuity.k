requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the real/K result for (3,4,5) is 600 hundredths.
  // Requiring 601 changes the observable result obligation.
  claim [false-result-3-4-5]:
    <triangle>
      <k> launch(solutionProgram, Args(VInt(3), VInt(4), VInt(5))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(601) </result>
    </triangle>
endmodule
