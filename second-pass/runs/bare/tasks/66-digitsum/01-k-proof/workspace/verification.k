module DIGIT-SUM-VERIFICATION
  imports INT
  imports BOOL
  imports STRING
  imports K-EQUAL

  // Independent mathematical contract: recursively sum exactly the code
  // points in the inclusive ASCII uppercase interval [65, 90].
  syntax Int ::= "upperAsciiSum" "(" String ")" [function]
               | "upperAsciiContribution" "(" String ")" [function]

  rule upperAsciiSum("") => 0 [simplification]
  rule upperAsciiSum(S)
    => upperAsciiContribution(substrString(S, 0, 1))
       +Int upperAsciiSum(substrString(S, 1, lengthString(S)))
    requires S =/=String "" [simplification]

  rule upperAsciiContribution(C)
    => #if ordChar(C) >=Int 65 andBool ordChar(C) <=Int 90
       #then ordChar(C)
       #else 0
       #fi [simplification]

  // Canonical right-associated form used by the loop invariant.
  rule (I +Int J) +Int K => I +Int (J +Int K) [simplification]
endmodule
