requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Contract-level reference result.  It is intentionally phrased directly
  // in terms of normalized characters, independently of AST evaluation.
  syntax Int ::= expectedDistinctCharacters(String) [function]
  rule expectedDistinctCharacters(S) => size(charsSet(lowerString(S)))
endmodule
