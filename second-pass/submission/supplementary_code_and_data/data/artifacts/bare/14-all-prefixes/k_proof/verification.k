requires "semantic.k"
requires "solution-program.k"

module VERIFICATION
  imports MPY
  imports SOLUTION-PROGRAM

  // pacc(S,N) is the abstract list of the first N nonempty prefixes of S.
  // These two equations establish its base case and its induction step.
  syntax Values ::= pacc(String, Int)
  rule pacc(_, 0) => vnil
  rule snoc(pacc(S, N), strVal(substrString(S, 0, I)))
    => pacc(S, N +Int 1)
    requires I ==Int N +Int 1
    [simplification]

  syntax Values ::= allPrefixes(String) [function]
  rule allPrefixes(S) => pacc(S, lengthString(S))
endmodule
