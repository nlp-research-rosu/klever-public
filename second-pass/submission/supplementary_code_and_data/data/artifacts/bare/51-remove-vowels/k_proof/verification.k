requires "semantic.k"

module VERIFICATION
  imports MPY

  // This is the contract in executable mathematical form: delete every
  // occurrence of each of the ten one-character English vowel strings.
  syntax String ::= removeLowerVowels(String) [function, total]
                  | removeUpperVowels(String) [function, total]
                  | removeVowelsSpec(String)  [function, total]

  rule removeLowerVowels(S)
    => deleteAll(
         deleteAll(
           deleteAll(
             deleteAll(
               deleteAll(S, "a"),
             "e"),
           "i"),
         "o"),
       "u")

  rule removeUpperVowels(S)
    => deleteAll(
         deleteAll(
           deleteAll(
             deleteAll(
               deleteAll(S, "A"),
             "E"),
           "I"),
         "O"),
       "U")

  rule removeVowelsSpec(S) => removeUpperVowels(removeLowerVowels(S))
endmodule
