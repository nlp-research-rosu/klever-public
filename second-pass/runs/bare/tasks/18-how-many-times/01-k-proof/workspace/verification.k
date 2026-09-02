requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Independent mathematical recurrence for overlapping occurrences.
  syntax Int ::= overlapCount(String, String) [function]

  rule overlapCount(S, T) => lengthString(S) +Int 1
    requires T ==String ""

  rule overlapCount(S, T) => 0
    requires notBool (T ==String "")
     andBool lengthString(S) <Int lengthString(T)

  rule overlapCount(S, T)
    => 1 +Int overlapCount(
         substrString(S, 1, lengthString(S)), T)
    requires notBool (T ==String "")
     andBool notBool (lengthString(S) <Int lengthString(T))
     andBool substrString(S, 0, lengthString(T)) ==String T

  rule overlapCount(S, T)
    => overlapCount(substrString(S, 1, lengthString(S)), T)
    requires notBool (T ==String "")
     andBool notBool (lengthString(S) <Int lengthString(T))
     andBool notBool (substrString(S, 0, lengthString(T)) ==String T)
endmodule
