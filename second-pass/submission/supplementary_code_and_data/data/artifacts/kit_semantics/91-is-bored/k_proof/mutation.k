requires "verification-base.k"

module MUTATION
  imports VERIFICATION-BASE

  // Material body mutation: the loop deliberately does nothing.
  syntax Stmts ::= "MUTATED-LOOP-BODY" [macro]
  rule MUTATED-LOOP-BODY => .Stmts
endmodule
