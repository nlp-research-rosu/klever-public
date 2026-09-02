module VERIFICATION
  imports MPY-SEMANTICS

  // Independent contract model.  It is the structural characterization of
  // the shortest palindrome beginning with S: a palindrome needs no suffix;
  // otherwise its first character must also be its final character, reducing
  // the problem to the tail.  Length decreases in the recursive branch.
  syntax String ::= "#reference" "(" String ")" [function, total]
                  | "#referenceChoice" "(" String "," Bool ")" [function, total]
  rule #reference(S)
    => #referenceChoice(S, S ==String #reverse(S))
  rule #referenceChoice(S, B) => S
    requires B
  rule #referenceChoice(S, B)
    => substrString(S, 0, 1)
       +String #reference(substrString(S, 1, lengthString(S)))
       +String substrString(S, 0, 1)
    requires notBool B andBool lengthString(S) >Int 0

  // Proof-only predicates are kept in this layer.  The executable semantics
  // does not depend on them.
  syntax Bool ::= "#isPalindrome" "(" String ")" [function]
  rule #isPalindrome(S) => S ==String #reverse(S)
endmodule
