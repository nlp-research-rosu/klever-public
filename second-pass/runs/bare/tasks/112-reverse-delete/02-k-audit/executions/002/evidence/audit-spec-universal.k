requires "verification.k"

module AUDIT-SPEC-UNIVERSAL
  imports VERIFICATION

  claim <k>
          execute(solutionPgm, S:String, C:String)
          => returned(expectedResult(S, C))
        </k>
endmodule
