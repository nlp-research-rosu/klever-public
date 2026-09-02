requires "verification.k"

module XOR-SPEC-END-TO-END-ONLY
  imports XOR-VERIFICATION

  claim
    <k> solutionProgram => returned(str(xorText(N, M, S1, S2))) ... </k>
    <args> Args(str(segment(N, S1)), str(segment(M, S2))) </args>
    requires N >=Int 0 andBool M >=Int 0
endmodule
