requires "verification.k"

module XOR-SPEC-FALSE-RESULT-MUTATION
  imports XOR-VERIFICATION

  // False at the satisfying witness N=0, M=0: execution returns empty,
  // whereas this postcondition demands a leading one bit.
  claim
    <k> exec(solutionBody,
             env(str(segment(N, S1)), str(segment(M, S2))),
             solutionBody)
      => returned(str(cons(true, xorText(N, M, S1, S2)))) ... </k>
    <args> _ARGS </args>
    requires N >=Int 0 andBool M >=Int 0
endmodule
