requires "reference-semantics/semantics.k"

module GET-ROW-VERIFICATION
  imports MPY

  // This is the body emitted in solution.mpy, factored into a macro so that
  // the claims can install the function in the module scope without first
  // executing unrelated module-loading steps.
  syntax Stmts ::= "getRowBody" [function]
  rule getRowBody
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

  syntax Val ::= "getRowClosure" [function]
  rule getRowClosure
    => closureVal(("lst", "x", .ParamNames), getRowBody, 0)

  // Prepend (ROW, COLUMN) exactly when VALUE equals the requested integer.
  // Nesting addMatch from the last visited coordinate to the first gives the
  // mathematical result sequence for a fixed ragged shape.
  syntax ValSeq ::= addMatch(Int, Int, Int, Int, ValSeq) [function, total]
  rule addMatch(V:Int, X:Int, R:Int, C:Int, REST:ValSeq)
    => vCons(tuple(vCons(R, vCons(C, .ValSeq))), REST)
    requires V ==Int X
  rule addMatch(V:Int, X:Int, _R:Int, _C:Int, REST:ValSeq)
    => REST
    requires V =/=Int X
endmodule
