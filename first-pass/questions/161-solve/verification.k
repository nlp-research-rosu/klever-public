// verification.k — summary for the solve proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module SOLVE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // swapC / swapMap: swapcase each code (upper<->lower, else unchanged).
  syntax Int ::= sSwapC(Int) [function, total]
  rule sSwapC(C:Int) => C +Int 32 requires C >=Int 65 andBool C <=Int 90  [simplification]
  rule sSwapC(C:Int) => C -Int 32 requires C >=Int 97 andBool C <=Int 122 [simplification]
  rule sSwapC(C:Int) => C
    requires notBool (C >=Int 65 andBool C <=Int 90) andBool notBool (C >=Int 97 andBool C <=Int 122) [simplification]
  syntax IntSeq ::= sSwapMap(IntSeq) [function, total]
  rule sSwapMap(.IntSeq) => .IntSeq [simplification]
  rule sSwapMap(iCons(C:Int, S:IntSeq)) => iCons(sSwapC(C), sSwapMap(S)) [simplification]

  // revPrep(CS, R) = reverse(CS) prepended to R (the loop does rev = c + rev).
  syntax IntSeq ::= revPrep(IntSeq, IntSeq) [function, total]
  rule revPrep(.IntSeq, R:IntSeq) => R [simplification]
  rule revPrep(iCons(C:Int, S:IntSeq), R:IntSeq) => revPrep(S, iCons(C, R)) [simplification]

  // sHasAlpha(CS) = any char is a letter.
  syntax Bool ::= sIsLetter(Int) [function, total]
  rule sIsLetter(C:Int) => (C >=Int 65 andBool C <=Int 90) orBool (C >=Int 97 andBool C <=Int 122) [simplification]
  syntax Bool ::= sHasAlpha(IntSeq) [function, total]
  rule sHasAlpha(.IntSeq) => false [simplification]
  rule sHasAlpha(iCons(C:Int, S:IntSeq)) => sIsLetter(C) orBool sHasAlpha(S) [simplification]

endmodule
