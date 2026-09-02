requires "/tmp/audit-work/130-tri/candidate/verification.k"

module AUDIT-SPEC-EVAL-CALL
  imports TRI-VERIFICATION
  claim <k> evalCall(solutionProgram, "tri", N)
          => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0
endmodule
