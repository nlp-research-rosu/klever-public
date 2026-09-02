requires "verification.k"

module SPEC
  imports VERIFICATION

  claim <k> runProgram(solutionProgram, S:String)
          => contractResult(S)
        </k>
endmodule
