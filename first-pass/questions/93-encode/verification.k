// verification.k — summary for the encode proof, on the UNIFIED semantics.
// Composes swapcase (27) + vowel membership (64): each char is case-flipped, then
// shifted +2 if the flipped code is a vowel.

requires "../../reference/src/lemmas.k"

module ENCODE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // swapc(C) = swapcase a code (upper +32, lower -32, else unchanged).
  syntax Int ::= swapc(Int) [function, total]
  rule swapc(C:Int) => C +Int 32 requires C >=Int 65 andBool C <=Int 90  [simplification]
  rule swapc(C:Int) => C -Int 32 requires C >=Int 97 andBool C <=Int 122 [simplification]
  rule swapc(C:Int) => C
    requires notBool (C >=Int 65 andBool C <=Int 90)
     andBool notBool (C >=Int 97 andBool C <=Int 122) [simplification]

  // isVowel(C) = the 10-way vowel membership.
  syntax Bool ::= isVowel(Int) [function, total]
  rule isVowel(C:Int)
    => C ==Int 97 orBool C ==Int 101 orBool C ==Int 105 orBool C ==Int 111 orBool C ==Int 117
       orBool C ==Int 65 orBool C ==Int 69 orBool C ==Int 73 orBool C ==Int 79 orBool C ==Int 85
    [simplification]

  // encChar(C) = swapcase, then +2 if the result is a vowel.
  syntax Int ::= encChar(Int) [function, total]
  rule encChar(C:Int) => swapc(C) +Int 2 requires isVowel(swapc(C))         [simplification]
  rule encChar(C:Int) => swapc(C)         requires notBool isVowel(swapc(C)) [simplification]

  syntax IntSeq ::= encMap(IntSeq) [function, total]
  rule encMap(.IntSeq) => .IntSeq [simplification]
  rule encMap(iCons(C:Int, S:IntSeq)) => iCons(encChar(C), encMap(S)) [simplification]

  // Left-built accumulator lemmas.
endmodule
