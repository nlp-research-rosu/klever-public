requires "verification.k"

module XOR-SPEC-AUDIT
  imports XOR-VERIFICATION

  claim [audit-recursive]:
    <k> exec(solutionBody,
             env(str(segment(N, S1)), str(segment(M, S2))),
             solutionBody)
      => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> _ARGS </args>
    requires N >=Int 0 andBool M >=Int 0

  claim [audit-entry]:
    <k> solutionProgram => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> Args(str(segment(N, S1)), str(segment(M, S2))) </args>
    requires N >=Int 0 andBool M >=Int 0
endmodule
