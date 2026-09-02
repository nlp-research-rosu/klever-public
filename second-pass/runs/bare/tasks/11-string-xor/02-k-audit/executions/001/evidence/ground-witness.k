requires "verification.k"

module XOR-GROUND-WITNESS
  imports XOR-VERIFICATION

  // N=3, M=3, S1=seed(2) encode "010", and S2=seed(3) encodes "110".
  // This is a satisfiable instance of both submitted preconditions.
  claim
    <k> returned(str(xorText(3, 3, seed(2), seed(3))))
      => returned(str(cons(true, cons(false, cons(false, empty))))) ... </k>
    <args> Args(str(segment(3, seed(2))),
                str(segment(3, seed(3)))) </args>
endmodule
