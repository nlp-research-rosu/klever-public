requires "verification-base.k"

module STAGE5-BODY-MUTATION
  imports VERIFICATION-BASE

  syntax Stmts ::= "AUDIT-MUTATED-LOOP-BODY" [macro]
  rule AUDIT-MUTATED-LOOP-BODY => .Stmts

  syntax Stmts ::= "AUDIT-MUTATED-FUNCTION-BODY" [macro]
  rule AUDIT-MUTATED-FUNCTION-BODY
    => Assign(Name("count"), Int(0))
       Assign(Name("at_start"), Bool(true))
       Assign(Name("pending_i"), Bool(false))
       Assign(Name("c"), Str(""))
       For(Name("c"), Name("S"), AUDIT-MUTATED-LOOP-BODY)
       If(
         Name("pending_i"),
         AugAssign(Name("count"), "+", Int(1)) .Stmts,
         .Stmts)
       Return(Name("count"))
       .Stmts
endmodule
