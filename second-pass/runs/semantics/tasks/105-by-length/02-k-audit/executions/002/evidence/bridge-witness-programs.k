requires "reference-semantics/semantics.k"

module LOOP-WITNESS-PROGRAMS
  imports MPY

  // The first bridge's exact loop body, followed by an observable read of
  // the loop target. For Python input [2], fixed execution returns 2.
  syntax Stmts ::= "filterLoopWitnessBody" [function, total]
  rule filterLoopWitnessBody
    => Assign(Name("values"), ListExpr(.Exprs))
       Assign(Name("value"), Int(99))
       For(
         Name("value"),
         Name("arr"),
         If(
           BoolOp(
             "and",
             Compare(Name("value"), CmpOp(">=", Int(1))),
             Compare(Name("value"), CmpOp("<=", Int(9)))),
           Expr(
             Call(
               Attribute(Name("values"), "append"),
               Name("value"))),
           .Stmts))
       Return(Name("value"))

  syntax Val ::= "filterLoopWitnessClosure" [function, total]
  rule filterLoopWitnessClosure
    => closureVal("arr", filterLoopWitnessBody, 0)

  // The second bridge's exact loop body, again followed by an observable
  // read of the loop target. For Python input [2], fixed execution returns 2.
  syntax Stmts ::= "mapLoopWitnessBody" [function, total]
  rule mapLoopWitnessBody
    => Assign(
         Name("names"),
         ListExpr(
           Str("One"), Str("Two"), Str("Three"), Str("Four"),
           Str("Five"), Str("Six"), Str("Seven"), Str("Eight"),
           Str("Nine")))
       Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("value"), Int(99))
       For(
         Name("value"),
         Name("arr"),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Subscript(
               Name("names"),
               BinOp("-", Name("value"), Int(1))))))
       Return(Name("value"))

  syntax Val ::= "mapLoopWitnessClosure" [function, total]
  rule mapLoopWitnessClosure
    => closureVal("arr", mapLoopWitnessBody, 0)
endmodule
