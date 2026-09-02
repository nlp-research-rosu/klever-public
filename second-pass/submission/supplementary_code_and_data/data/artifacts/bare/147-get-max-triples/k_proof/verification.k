requires "semantic.k"

// Mathematical contract used to verify get_max_triples.
module VERIFICATION
  imports MPY

  // Number of unordered ways to choose three indices from a class of size X.
  syntax Int ::= choose3(Int) [function, total]
  rule choose3(X) => (X *Int (X -Int 1) *Int (X -Int 2)) divInt 6

  // For i >= 1, i*i-i+1 is 0 modulo 3 precisely when i is 2 modulo 3;
  // otherwise it is 1 modulo 3.  Hence a divisible sum contains either three
  // zero-residue entries or three one-residue entries.  Among 1..N the class
  // sizes are (N+1)//3 and N-(N+1)//3, respectively.
  syntax Int ::= validTripleCount(Int) [function, total]
  rule validTripleCount(N) =>
    choose3((N +Int 1) divInt 3)
    +Int choose3(N -Int ((N +Int 1) divInt 3))
endmodule
