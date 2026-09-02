requires "verification.k"

module PRECISION-WITNESS-SPEC
  imports VERIFICATION

  claim [precision-loss-valid]:
    <triangle>
      <k>
        launch(
          solutionProgram,
          Args(VInt(10000000000000000), VInt(10000000000000000), VInt(1))
        ) => .K
      </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(500000000000000000) </result>
    </triangle>
endmodule
