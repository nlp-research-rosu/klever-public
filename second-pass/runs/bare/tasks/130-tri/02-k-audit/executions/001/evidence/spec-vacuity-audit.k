requires "/tmp/audit-work/130-tri/candidate/verification.k"

module AUDIT-SPEC-VACUITY
  imports TRI-VERIFICATION

  // Keep the successful interpreter lemma, but mutate the entry result to the
  // next prefix. At N = 0, execution returns [1] while this demands [1, 3].
  claim <k> evalCall(solutionProgram, "tri", N)
          => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0

  claim <k> run(solutionProgram, N)
          => returned(LVal(triPrefix(N +Int 1))) ... </k>
    requires N >=Int 0
endmodule
