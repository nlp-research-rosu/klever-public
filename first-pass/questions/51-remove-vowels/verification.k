// verification.k — summary for the remove_vowels proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module REMOVE-VOWELS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // isVowel(C): the 10-way vowel membership (the program tests its De Morgan negation).
  syntax Bool ::= isVowel(Int) [function, total]
  rule isVowel(C:Int)
    => C ==Int 97 orBool C ==Int 101 orBool C ==Int 105 orBool C ==Int 111 orBool C ==Int 117
       orBool C ==Int 65 orBool C ==Int 69 orBool C ==Int 73 orBool C ==Int 79 orBool C ==Int 85
    [simplification]

  // filterSeq(CS) = keep the non-vowel codes (a string FILTER).
  syntax IntSeq ::= filterSeq(IntSeq) [function, total]
  rule filterSeq(.IntSeq) => .IntSeq [simplification]
  rule filterSeq(iCons(C:Int, S:IntSeq)) => iCons(C, filterSeq(S)) requires notBool isVowel(C) [simplification]
  rule filterSeq(iCons(C:Int, S:IntSeq)) =>          filterSeq(S)  requires isVowel(C)         [simplification]

  // Left-built accumulator lemmas.
endmodule
