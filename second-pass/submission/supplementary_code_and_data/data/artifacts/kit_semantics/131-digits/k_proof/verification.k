requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports INT

  // Empty product is 1.  The entry claim multiplies this by oddDigitSeen,
  // which changes the all-even result to the contract's required 0.
  syntax Int ::= oddDigitsProduct(Int) [function, total]
  syntax Int ::= oddDigitSeen(Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  // Definitional summaries.  Their positive cases follow exactly one decimal
  // digit-removal step from MPY-INT's Python // and % rules.
  rule oddDigitsProduct(N) => 1
    requires N <=Int 0
  rule oddDigitsProduct(N)
    => pyMod(N, 10) *Int
       oddDigitsProduct((N -Int pyMod(N, 10)) /Int 10)
    requires N >Int 0
     andBool pyMod(N, 2) ==Int 1
  rule oddDigitsProduct(N)
    => oddDigitsProduct((N -Int pyMod(N, 10)) /Int 10)
    requires N >Int 0
     andBool pyMod(N, 2) ==Int 0

  rule oddDigitSeen(N) => 0
    requires N <=Int 0
  rule oddDigitSeen(N) => 1
    requires N >Int 0
     andBool pyMod(N, 2) ==Int 1
  rule oddDigitSeen(N)
    => oddDigitSeen((N -Int pyMod(N, 10)) /Int 10)
    requires N >Int 0
     andBool pyMod(N, 2) ==Int 0

  // Derived integer identities used only to normalize the inductive
  // post-state after the circularity has executed the remaining loop.
  rule 1 *Int X => X [simplification]
  rule X *Int 1 => X [simplification]
  rule X +Int 1 -Int X => 1 [simplification]
  rule (X *Int Y) *Int Z => X *Int (Y *Int Z) [simplification]
endmodule
