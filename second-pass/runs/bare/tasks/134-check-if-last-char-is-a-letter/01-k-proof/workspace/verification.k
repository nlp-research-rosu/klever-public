requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A direct formalization of the English contract.  A final letter is not
  // part of a word exactly when it is the whole string, or when a space is
  // immediately before it.
  syntax Bool ::= standaloneLastLetter(String) [function]

  rule standaloneLastLetter(S)
    => (lengthString(S) ==Int 1 andBool isAlphaString(S))
       orBool
       (lengthString(S) >Int 1
        andBool isAlphaString(atString(S, 0 -Int 1))
        andBool atString(S, 0 -Int 2) ==String " ")
endmodule
