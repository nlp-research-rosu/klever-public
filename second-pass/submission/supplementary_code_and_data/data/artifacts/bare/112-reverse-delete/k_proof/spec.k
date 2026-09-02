requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal functional-correctness theorem: S and C are arbitrary K
  // strings.  expectedResult is the natural-language contract encoded in
  // verification.k.
  claim <k>
          execute(solutionPgm, S:String, C:String)
          => returned(expectedResult(S, C))
        </k>

  // The three examples in the prompt are also independent proof claims.
  claim <k>
          execute(solutionPgm, "abcde", "ae")
          => returned(tupleVal(strVal("bcd"), boolVal(false)))
        </k>

  claim <k>
          execute(solutionPgm, "abcdef", "b")
          => returned(tupleVal(strVal("acdef"), boolVal(false)))
        </k>

  claim <k>
          execute(solutionPgm, "abcdedcba", "ab")
          => returned(tupleVal(strVal("cdedc"), boolVal(true)))
        </k>
endmodule
