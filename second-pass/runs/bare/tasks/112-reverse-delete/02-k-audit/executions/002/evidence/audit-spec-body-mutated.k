requires "verification-body-mutated.k"

module AUDIT-SPEC-BODY-MUTATED
  imports VERIFICATION-BODY-MUTATED

  claim <k>
          execute(mutatedSolutionPgm, S:String, C:String)
          => returned(expectedMutatedResult(S, C))
        </k>
endmodule
