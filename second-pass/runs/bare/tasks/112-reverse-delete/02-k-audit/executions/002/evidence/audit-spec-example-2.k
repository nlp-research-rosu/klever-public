requires "verification.k"

module AUDIT-SPEC-EXAMPLE-2
  imports VERIFICATION

  claim <k>
          execute(solutionPgm, "abcdef", "b")
          => returned(tupleVal(strVal("acdef"), boolVal(false)))
        </k>
endmodule
