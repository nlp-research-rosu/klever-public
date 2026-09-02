// verification.k — even_odd_palindrome on the UNIFIED semantics, TRAP-FREE
// (P107). solution.py is canonical (nested is_palindrome with the REAL
// str(n) == str(n)[::-1] body). All bridges are SHARED lemmas: str(symbolic
// int) -> digitCodes (lemmas/str-int-decimal.k) and the whole-reverse slice
// buildIS -> revIS (lemmas/subscript.k). The palindrome ATOM the execution
// produces is digitCodes(I) ==K revIS(digitCodes(I)); both counter folds
// case-split on it.

requires "../../reference/src/lemmas.k"

module EVEN-ODD-PALINDROME-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- the two counter folds over i in [I, HI); guards over the EXACT atoms
  syntax Int ::= evenPal(Int, Int, Int) [function, total]
  rule evenPal(I:Int, HI:Int, C:Int) => C requires I >=Int HI [simplification]
  rule evenPal(I:Int, HI:Int, C:Int) => evenPal(I +Int 1, HI, C +Int 1)
    requires I <Int HI andBool pyMod(I, 2) ==Int 0
     andBool digitCodes(I) ==K revIS(digitCodes(I))
    [simplification]
  rule evenPal(I:Int, HI:Int, C:Int) => evenPal(I +Int 1, HI, C)
    requires I <Int HI
     andBool notBool (pyMod(I, 2) ==Int 0 andBool digitCodes(I) ==K revIS(digitCodes(I)))
    [simplification]

  syntax Int ::= oddPal(Int, Int, Int) [function, total]
  rule oddPal(I:Int, HI:Int, C:Int) => C requires I >=Int HI [simplification]
  rule oddPal(I:Int, HI:Int, C:Int) => oddPal(I +Int 1, HI, C +Int 1)
    requires I <Int HI andBool pyMod(I, 2) ==Int 1
     andBool digitCodes(I) ==K revIS(digitCodes(I))
    [simplification]
  rule oddPal(I:Int, HI:Int, C:Int) => oddPal(I +Int 1, HI, C)
    requires I <Int HI
     andBool notBool (pyMod(I, 2) ==Int 1 andBool digitCodes(I) ==K revIS(digitCodes(I)))
    [simplification]
endmodule
