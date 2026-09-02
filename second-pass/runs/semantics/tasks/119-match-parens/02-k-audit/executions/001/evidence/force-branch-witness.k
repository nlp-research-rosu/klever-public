requires "verification.k"

module FORCE-BRANCH-WITNESS
  imports MATCH-PARENS-VERIFICATION

  syntax Stmt ::= "ThenMark" | "ElseMark"
  syntax Val ::= "thenReached" | "elseReached"

  rule <k> ThenMark ~> _ => thenReached </k>
  rule <k> ElseMark ~> _ => elseReached </k>
endmodule
