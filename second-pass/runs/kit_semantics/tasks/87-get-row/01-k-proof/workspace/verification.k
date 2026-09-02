requires "row-model.k"

module VERIFICATION-SYNTAX
  imports ROW-MODEL-SYNTAX

  syntax ValSeq ::= scanAppend(ValSeq, ValSeq, Int, Int, Int) [function, total]
                  | rowsAppend(ValSeq, ValSeq, Int, Int) [function]
  syntax Int ::= advanceIndex(Int, ValSeq) [function, total]

  syntax Stmts ::= "INNERBODY"  [macro]
                 | "OUTERBODY"  [macro]
                 | "GETROWBODY" [macro]
  syntax Val ::= "COLUMNCLOSURE" [macro]
               | "ROWCLOSURE"    [macro]
endmodule

module VERIFICATION
  imports ROW-MODEL
  imports VERIFICATION-SYNTAX

  rule <k> For(T:Expr, V:Val, B:Stmts)
        => #loop(list(rowContents(V)), T, B) ... </k>
       requires V ==K list(rowContents(V))
       [priority(40)]

  rule advanceIndex(I:Int, .ValSeq) => I
  rule advanceIndex(I:Int, vCons(_:Val, VS:ValSeq))
    => advanceIndex(I +Int 1, VS)

  rule scanAppend(ACC:ValSeq, .ValSeq, _:Int, _:Int, _:Int) => ACC
  rule scanAppend(ACC:ValSeq, vCons(V:Val, VS:ValSeq),
                  X:Int, RI:Int, CI:Int)
    => scanAppend(
         valSeqConcat(
           ACC,
           vCons(tuple(vCons(RI, vCons(CI, .ValSeq))), .ValSeq)),
         VS, X, RI, CI +Int 1)
    requires V ==K X
    [simplification]
  rule scanAppend(ACC:ValSeq, vCons(V:Val, VS:ValSeq),
                  X:Int, RI:Int, CI:Int)
    => scanAppend(ACC, VS, X, RI, CI +Int 1)
    requires notBool (V ==K X)
    [simplification]

  rule rowsAppend(ACC:ValSeq, .ValSeq, _:Int, _:Int) => ACC
  rule rowsAppend(ACC:ValSeq,
                  vCons(V:Val, RS:ValSeq),
                  X:Int, RI:Int)
    => rowsAppend(scanAppend(ACC, rowContents(V), X, RI, 0),
                  RS, X, RI +Int 1)
    requires V ==K list(rowContents(V))
    [simplification]

  rule INNERBODY
    => If(Compare(Name("value"),
                  CmpOp("in", TupleExpr((Name("x"), .Exprs)))),
          Expr(Call(Attribute(Name("coordinates"), "append"),
                    (TupleExpr((Name("row_index"), Name("column_index"), .Exprs)),
                     .Exprs)))
          .Stmts,
          .Stmts)
       AugAssign(Name("column_index"), "+", Int(1))
       .Stmts

  rule OUTERBODY
    => Assign(Name("column_index"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("row"), INNERBODY)
       AugAssign(Name("row_index"), "+", Int(1))
       .Stmts

  rule GETROWBODY
    => Assign(Name("coordinates"), ListExpr(.Exprs))
       Assign(Name("row_index"), Int(0))
       Assign(Name("row"), NoneVal)
       Assign(Name("column_index"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("row"), Name("lst"), OUTERBODY)
       Assign(Name("coordinates"),
              Call(Name("sorted"),
                   (Name("coordinates"),
                    KwArg("key", Name("_column_desc")),
                    .Exprs)))
       Return(Call(Name("sorted"),
                   (Name("coordinates"),
                    KwArg("key", Name("_row_asc")),
                    .Exprs)))
       .Stmts

  rule COLUMNCLOSURE
    => closureVal(("coordinate", .ParamNames),
                  Return(UnaryOp("-", Subscript(Name("coordinate"), Int(1))))
                  .Stmts,
                  0)

  rule ROWCLOSURE
    => closureVal(("coordinate", .ParamNames),
                  Return(Subscript(Name("coordinate"), Int(0)))
                  .Stmts,
                  0)
endmodule
