requires "bridge-free.k"

module XOR-BRIDGE-FREE-SPEC
  imports XOR-BRIDGE-FREE

  claim [core-recursive]:
    <k> exec(solutionBodyCore,
             env(str(segment(N, S1)), str(segment(M, S2))),
             solutionBodyCore)
      => returned(str(xorTextCore(N, M, S1, S2))) ... </k>
    <args> _ARGS </args>
    requires N >=Int 0 andBool M >=Int 0

  claim [core-entry]:
    <k> solutionProgramCore
      => returned(str(xorTextCore(N, M, S1, S2))) ... </k>
    <args> Args(str(segment(N, S1)), str(segment(M, S2))) </args>
    requires N >=Int 0 andBool M >=Int 0
endmodule
