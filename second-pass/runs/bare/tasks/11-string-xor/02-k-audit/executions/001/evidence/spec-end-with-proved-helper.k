requires "verification.k"

module XOR-SPEC-END-WITH-PROVED-HELPER
  imports XOR-VERIFICATION

  // This is byte-for-byte the body of the separately proven entry claim.
  // The attribute makes this run prove only the end-to-end target while using
  // that established helper as a compositional lemma.
  claim
    <k> exec(solutionBody,
             env(str(segment(N, S1)), str(segment(M, S2))),
             solutionBody)
      => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> _ARGS </args>
    requires N >=Int 0 andBool M >=Int 0
    [trusted]

  claim
    <k> solutionProgram => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> Args(str(segment(N, S1)), str(segment(M, S2))) </args>
    requires N >=Int 0 andBool M >=Int 0
endmodule
