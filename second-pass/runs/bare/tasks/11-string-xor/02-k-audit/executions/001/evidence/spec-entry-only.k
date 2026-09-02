requires "verification.k"

module XOR-SPEC-ENTRY-ONLY
  imports XOR-VERIFICATION

  claim
    <k> exec(solutionBody,
             env(str(segment(N, S1)), str(segment(M, S2))),
             solutionBody)
      => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> _ARGS </args>
    requires N >=Int 0 andBool M >=Int 0
endmodule
