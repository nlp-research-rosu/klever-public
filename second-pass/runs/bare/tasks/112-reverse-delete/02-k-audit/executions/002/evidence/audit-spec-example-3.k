requires "verification.k"

module AUDIT-SPEC-EXAMPLE-3
  imports VERIFICATION

  claim <k>
          execute(solutionPgm, "abcdedcba", "ab")
          => returned(tupleVal(strVal("cdedc"), boolVal(true)))
        </k>
endmodule
