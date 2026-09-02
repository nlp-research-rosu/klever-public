requires "verification.k"

module SPEC-AUDIT
  imports VERIFICATION

  claim [universal]:
        <k>
          execute(solutionPgm, S:String, C:String)
          => returned(expectedResult(S, C))
        </k>

  claim [example-1]:
        <k>
          execute(solutionPgm, "abcde", "ae")
          => returned(tupleVal(strVal("bcd"), boolVal(false)))
        </k>

  claim [example-2]:
        <k>
          execute(solutionPgm, "abcdef", "b")
          => returned(tupleVal(strVal("acdef"), boolVal(false)))
        </k>

  claim [example-3]:
        <k>
          execute(solutionPgm, "abcdedcba", "ab")
          => returned(tupleVal(strVal("cdedc"), boolVal(true)))
        </k>
endmodule
