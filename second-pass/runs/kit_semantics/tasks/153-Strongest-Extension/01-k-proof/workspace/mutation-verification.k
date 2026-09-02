requires "verification.k"

module MUTATION-VERIFICATION
  imports TARGET-VERIFICATION

  syntax Stmts ::= "MUTATED-BODY" [macro]
  rule MUTATED-BODY
    => Return(Str("wrong")) .Stmts
endmodule
