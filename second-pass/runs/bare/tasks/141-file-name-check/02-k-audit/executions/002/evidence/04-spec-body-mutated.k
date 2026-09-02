requires "verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports VERIFICATION-BODY-MUTATED

  claim <k> runProgram(solutionProgram, S:String)
          => contractResult(S)
        </k>
endmodule
