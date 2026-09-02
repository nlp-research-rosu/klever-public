requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports INT-SYNTAX

  syntax Int ::= zeroResidueCount(Int) [function, total]
               | chooseThree(Int)      [function, total]
               | expectedTriples(Int)  [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY
  imports INT

  // Among 1,...,N, these are the indices congruent to 2 modulo 3.
  rule zeroResidueCount(N)
    => ((N +Int 1) -Int pyMod(N +Int 1, 3)) /Int 3

  // This form deliberately mirrors the reference semantics for Python's //.
  rule chooseThree(X)
    => (X *Int (X -Int 1) *Int (X -Int 2)
        -Int pyMod(X *Int (X -Int 1) *Int (X -Int 2), 6)) /Int 6

  rule expectedTriples(N)
    => chooseThree(zeroResidueCount(N))
       +Int chooseThree(N -Int zeroResidueCount(N))
endmodule
