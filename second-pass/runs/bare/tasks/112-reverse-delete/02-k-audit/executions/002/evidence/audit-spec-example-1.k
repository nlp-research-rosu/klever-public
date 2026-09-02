requires "verification.k"

module AUDIT-SPEC-EXAMPLE-1
  imports VERIFICATION

  claim <k>
          execute(solutionPgm, "abcde", "ae")
          => returned(tupleVal(strVal("bcd"), boolVal(false)))
        </k>
endmodule
