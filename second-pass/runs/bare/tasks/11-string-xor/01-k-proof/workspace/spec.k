requires "verification.k"

module XOR-SPEC
  imports XOR-VERIFICATION

  // Induction lemma at function entry.  The K-sequence ellipsis preserves
  // the caller continuation, so recursive calls can reuse this claim.
  claim
    <k> exec(solutionBody,
             env(str(segment(N, S1)), str(segment(M, S2))),
             solutionBody)
      => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> _ARGS </args>
    requires N >=Int 0 andBool M >=Int 0

  // End-to-end theorem from the translated module's initial configuration.
  claim
    <k> solutionProgram => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> Args(str(segment(N, S1)), str(segment(M, S2))) </args>
    requires N >=Int 0 andBool M >=Int 0
endmodule
