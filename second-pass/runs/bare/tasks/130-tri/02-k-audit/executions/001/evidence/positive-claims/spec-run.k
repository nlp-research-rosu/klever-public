requires "/tmp/audit-work/130-tri/candidate/verification.k"

module AUDIT-SPEC-RUN
  imports TRI-VERIFICATION
  claim <k> evalCall(solutionProgram, "tri", N)
          => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0
  claim <k> run(solutionProgram, N)
          => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0
endmodule
