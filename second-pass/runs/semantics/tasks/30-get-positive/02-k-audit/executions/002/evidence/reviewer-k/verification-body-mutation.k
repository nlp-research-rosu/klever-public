requires "verification.k"

module VERIFICATION-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity mutation: change the real guard from x > 0 to x > 1.
  syntax Stmts ::= "mutatedGetPositiveBody" [macro]
  rule mutatedGetPositiveBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("x"), Name("l"), mutatedPositiveLoopBody)
       Return(Name("result"))

  syntax Stmts ::= "mutatedPositiveLoopBody" [macro]
  rule mutatedPositiveLoopBody
    => If(
         Compare(Name("x"), CmpOp(">", Int(1))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Name("x"))),
         .Stmts)
endmodule
