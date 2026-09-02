requires "verification.k"

module AUDIT-BODY-IDENTITY-VERIFICATION
  imports GET-ROW-VERIFICATION

  // Independently transcribed constructor term from the freshly regenerated
  // solution.mpy.
  syntax Stmts ::= "expectedGetRowBody" [function]
  rule expectedGetRowBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(
         TupleExpr(Name("row_index"), Name("row"), .Exprs),
         Call(Name("enumerate"), Name("lst"), .Exprs),
         For(
           Name("column_index"),
           Call(
             Name("range"),
             BinOp("-", Call(Name("len"), Name("row"), .Exprs), Int(1)),
             UnaryOp("-", Int(1)),
             UnaryOp("-", Int(1)),
             .Exprs),
           If(
             Compare(
               Subscript(Name("row"), Name("column_index")),
               CmpOp("==", Name("x"))),
             Expr(
               Call(
                 Attribute(Name("result"), "append"),
                 TupleExpr(Name("row_index"), Name("column_index"), .Exprs),
                 .Exprs)),
             .Stmts)
           .Stmts)
         .Stmts)
       Return(Name("result"))
       .Stmts

  syntax Val ::= "expectedGetRowClosure" [function]
  rule expectedGetRowClosure
    => closureVal(("lst", "x", .ParamNames), expectedGetRowBody, 0)
endmodule
