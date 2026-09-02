requires "verification.k"

module SPEC-STRING-BOUNDARY
  imports VERIFICATION

  claim
    <py>
      <k>
        solutionProgram ~> invokeString("5  apples and 6 oranges", 19)
        => VInt(8)
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>
endmodule
