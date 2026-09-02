requires "verification.k"

module MUTATION-SYNTAX
  imports VERIFICATION-SYNTAX

  syntax Stmts ::= "GETROWBODYMUTANT" [macro]
endmodule

module MUTATION
  imports VERIFICATION
  imports MUTATION-SYNTAX

  // Material mutation: matching elements no longer append a coordinate.
  rule GETROWBODYMUTANT
    => Assign(Name("coordinates"), ListExpr(.Exprs))
       Assign(Name("row_index"), Int(0))
       Assign(Name("row"), NoneVal)
       Assign(Name("column_index"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("row"), Name("lst"),
         Assign(Name("column_index"), Int(0))
         Assign(Name("value"), Int(0))
         For(Name("value"), Name("row"),
           If(Compare(Name("value"),
                      CmpOp("in", TupleExpr((Name("x"), .Exprs)))),
              .Stmts,
              .Stmts)
           AugAssign(Name("column_index"), "+", Int(1))
           .Stmts)
         AugAssign(Name("row_index"), "+", Int(1))
         .Stmts)
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
endmodule
