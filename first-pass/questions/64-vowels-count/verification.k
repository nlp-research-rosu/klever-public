// verification.k — summary for the vowels_count proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module VOWELS-COUNT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // isVowel(C): a e i o u A E I O U (the 10-way membership the program computes).
  syntax Bool ::= isVowel(Int) [function, total]
  rule isVowel(C:Int)
    => C ==Int 97 orBool C ==Int 101 orBool C ==Int 105 orBool C ==Int 111 orBool C ==Int 117
       orBool C ==Int 65 orBool C ==Int 69 orBool C ==Int 73 orBool C ==Int 79 orBool C ==Int 85
    [simplification]

  // vowelCount(CS): number of vowel codes.
  syntax Int ::= vowelCount(IntSeq) [function, total]
  rule vowelCount(.IntSeq) => 0 [simplification]
  rule vowelCount(iCons(C:Int, S:IntSeq)) => 1 +Int vowelCount(S) requires isVowel(C)       [simplification]
  rule vowelCount(iCons(C:Int, S:IntSeq)) =>       vowelCount(S) requires notBool isVowel(C) [simplification]

  // lastOf(CS, Init): last code of CS, or Init if empty (the `last` accumulator).
  syntax Int ::= lastOf(IntSeq, Int) [function, total]
  rule lastOf(.IntSeq, I:Int)                => I            [simplification]
  rule lastOf(iCons(C:Int, S:IntSeq), _:Int) => lastOf(S, C) [simplification]
endmodule
