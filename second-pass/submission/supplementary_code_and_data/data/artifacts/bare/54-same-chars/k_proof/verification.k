requires "semantic.k"
requires "solution-program.k"

module VERIFICATION
  imports SOLUTION

  // The contract: the two strings induce the same mathematical set of
  // one-code-point strings.  Set equality deliberately ignores order and
  // duplicate occurrences.
  syntax Bool ::= "sameCharsSpec" "(" String "," String ")" [function, total]
  rule sameCharsSpec(S0, S1) => charSet(S0) ==K charSet(S1)
endmodule
