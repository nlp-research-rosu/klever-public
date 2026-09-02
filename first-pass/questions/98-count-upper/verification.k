// verification.k — summary for the count_upper proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module COUNT-UPPER-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // isUV(C): C is an uppercase vowel (A E I O U = 65 69 73 79 85).
  syntax Bool ::= isUV(Int) [function, total]
  rule isUV(C:Int) => C ==Int 65 orBool C ==Int 69 orBool C ==Int 73 orBool C ==Int 79 orBool C ==Int 85 [simplification]

  // countUE(CS, IDX) = count of uppercase vowels at even indices, folding from IDX.
  syntax Int ::= countUE(IntSeq, Int) [function, total]
  rule countUE(.IntSeq, _:Int) => 0 [simplification]
  rule countUE(iCons(C:Int, S:IntSeq), IDX:Int) => 1 +Int countUE(S, IDX +Int 1)
    requires pyMod(IDX, 2) ==Int 0 andBool isUV(C) [simplification]
  rule countUE(iCons(C:Int, S:IntSeq), IDX:Int) => countUE(S, IDX +Int 1)
    requires notBool (pyMod(IDX, 2) ==Int 0 andBool isUV(C)) [simplification]
endmodule
