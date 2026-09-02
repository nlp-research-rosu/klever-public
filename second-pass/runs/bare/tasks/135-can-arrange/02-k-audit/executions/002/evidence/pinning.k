requires "verification.k"

module PINNING
  imports VERIFICATION

  // Reviewer-only constructor wrapper: no evaluation and no task logic.
  syntax Pgm ::= "programOf" "(" Function ")" [macro]
  rule programOf(function(PS, BODY))
    => Module(FuncDef("can_arrange", PS, BODY))

endmodule
