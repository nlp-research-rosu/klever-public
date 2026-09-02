requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Independent statement of the prompt's result, expressed with the string
  // primitives defined by the semantics.
  syntax PString ::= "expected" "(" PString ")" [function, total]
  rule expected(S) => ifPString(hasAlpha(S), swapCase(S), reverse(S))
endmodule
