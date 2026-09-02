requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Independent mathematical characterization of the English contract.
  // Only a/e/i/o/u (in either case) are counted everywhere; y/Y contributes
  // one exactly when it is the sole remaining, hence final, character.
  syntax Int ::= "#vowels" "(" String ")" [function, total]

  rule #vowels("") => 0

  rule #vowels(S) =>
       1 +Int #vowels(substrString(S, 1, lengthString(S)))
    requires S =/=String ""
     andBool #isVowelChar(substrString(S, 0, 1))

  rule #vowels(S) => 1
    requires S =/=String ""
     andBool notBool #isVowelChar(substrString(S, 0, 1))
     andBool lengthString(S) ==Int 1
     andBool #isYChar(substrString(S, 0, 1))

  rule #vowels(S) =>
       #vowels(substrString(S, 1, lengthString(S)))
    requires S =/=String ""
     andBool notBool #isVowelChar(substrString(S, 0, 1))
     andBool (lengthString(S) =/=Int 1
              orBool notBool #isYChar(substrString(S, 0, 1)))
endmodule
