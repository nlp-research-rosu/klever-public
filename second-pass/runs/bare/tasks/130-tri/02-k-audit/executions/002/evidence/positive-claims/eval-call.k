requires "verification.k"

module AUDIT-EVAL-CALL
  imports TRI-VERIFICATION
  claim [eval-call]:
    <k> evalCall(solutionProgram, "tri", N)
        => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0
endmodule
