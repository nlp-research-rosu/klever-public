requires "verification.k"

module AUDIT-RUN-ENTRY
  imports TRI-VERIFICATION
  // Required circularity used by the outer entry claim, copied exactly from
  // the submitted spec.
  claim [eval-call-helper]:
    <k> evalCall(solutionProgram, "tri", N)
        => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0

  claim [run-entry]:
    <k> run(solutionProgram, N)
        => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0
endmodule
