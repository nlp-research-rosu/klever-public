// verification.k — summary for the get_closest_vowel proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module GET-CLOSEST-VOWEL-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // isv(C): C is a vowel code (a e i o u, either case).
  syntax Bool ::= isv(Int) [function, total]
  rule isv(C:Int) => C ==Int 97 orBool C ==Int 101 orBool C ==Int 105 orBool C ==Int 111 orBool C ==Int 117 orBool C ==Int 65 orBool C ==Int 69 orBool C ==Int 73 orBool C ==Int 79 orBool C ==Int 85 [simplification]

  // closeVowel(CS, IDX, P1, P2, RES): the result string after folding CS from index IDX
  // with previous codes P1 (i-1), P2 (i-2) and current result RES. From IDX>=2, a vowel
  // P1 flanked by consonants (P2, current C) sets RES := chr(P1) = str(iCons(P1,.IntSeq)).
  syntax Str ::= closeVowel(IntSeq, Int, Int, Int, Str) [function, total]
  rule closeVowel(.IntSeq, _:Int, _:Int, _:Int, RES:Str) => RES [simplification]
  rule closeVowel(iCons(C:Int, S:IntSeq), IDX:Int, P1:Int, P2:Int, _RES:Str)
    => closeVowel(S, IDX +Int 1, C, P1, str(iCons(P1, .IntSeq)))
    requires IDX >=Int 2 andBool isv(P1) andBool notBool isv(P2) andBool notBool isv(C) [simplification]
  rule closeVowel(iCons(C:Int, S:IntSeq), IDX:Int, P1:Int, P2:Int, RES:Str)
    => closeVowel(S, IDX +Int 1, C, P1, RES)
    requires notBool (IDX >=Int 2 andBool isv(P1) andBool notBool isv(P2) andBool notBool isv(C)) [simplification]

endmodule
