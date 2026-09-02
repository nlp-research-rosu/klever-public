requires "program.k"

module VERIFICATION
  imports MPY-SYNTAX
  imports SOLUTION-PROGRAM
  imports BOOL

  // A direct mathematical reading of the contract.  Looking from the right,
  // a word shorter than three characters has no eligible position.  Otherwise
  // inspect its last three characters: return the middle one exactly when it
  // is a vowel bracketed by consonants, or continue with the final character
  // removed.  This definition is independent of the evaluator below.
  syntax Val ::= closestSpec(Chars)                           [function]
  rule closestSpec(.Chars) => pyStr(.Chars)
  rule closestSpec(snoc(.Chars, A)) => pyStr(.Chars)
  rule closestSpec(snoc(snoc(.Chars, A), B)) => pyStr(.Chars)
  rule closestSpec(snoc(snoc(snoc(P, con(A)), vow(V:Vowel)), con(C)))
    => pyStr(snoc(.Chars, vow(V)))
  rule closestSpec(snoc(snoc(snoc(P, A), con(B)), C))
    => closestSpec(snoc(snoc(P, A), con(B)))
  rule closestSpec(snoc(snoc(snoc(P, vow(V1:Vowel)), vow(V2:Vowel)), C))
    => closestSpec(snoc(snoc(P, vow(V1)), vow(V2)))
  rule closestSpec(snoc(snoc(snoc(P, con(A)), vow(V:Vowel)), vow(V2:Vowel)))
    => closestSpec(snoc(snoc(P, con(A)), vow(V)))

endmodule
