requires "semantic-bridge-free.k"

module CONNECTION-VERIFICATION
  imports MPY

  // Proof-side exposure of the two exhaustive, disjoint equations already
  // defining evenPart in the generated semantics.
  rule evenPart(I) => I
    requires I %Int 2 ==Int 0
    [simplification]
  rule evenPart(I) => 0
    requires I %Int 2 =/=Int 0
    [simplification]
endmodule
