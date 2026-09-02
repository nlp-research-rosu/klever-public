requires "/tmp/audit-work/130-tri-audit/reference-semantics/semantics.k"

module TRI-NEUTRAL-VERIFICATION
  imports MPY

  // Fresh constructor only: unlike the candidate theory, this module gives it
  // no bridge from a concrete ValSeq.
  syntax ValSeq ::= triPrefix(Int)

  syntax Expr ::= "NeutralTriLoopCond" [macro]
  rule NeutralTriLoopCond
    => Compare(Name("i"), CmpOp("<=", Name("n")))

  syntax Stmts ::= "NeutralTriLoopBody" [macro]
  rule NeutralTriLoopBody
    => If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
         Assign(Name("value"),
           BinOp("+", Int(1), BinOp("//", Name("i"), Int(2))))
         .Stmts,
         Assign(Name("value"),
           BinOp("+",
             BinOp("+", BinOp("+", Name("b"), Name("a")), Int(1)),
             BinOp("//", BinOp("+", Name("i"), Int(1)), Int(2))))
         .Stmts)
       Expr(Call(Attribute(Name("result"), "append"),
                 Name("value"), .Exprs))
       Assign(Name("a"), Name("b"))
       Assign(Name("b"), Name("value"))
       AugAssign(Name("i"), "+", Int(1))
       .Stmts

  syntax Stmts ::= "NeutralTriFunctionBody" [macro]
  rule NeutralTriFunctionBody
    => If(Compare(Name("n"), CmpOp("==", Int(0))),
         Return(ListExpr(Int(1), .Exprs)) .Stmts,
         .Stmts)
       Assign(Name("result"), ListExpr(Int(1), Int(3), .Exprs))
       Assign(Name("a"), Int(1))
       Assign(Name("b"), Int(3))
       Assign(Name("value"), Int(3))
       Assign(Name("i"), Int(2))
       While(NeutralTriLoopCond, NeutralTriLoopBody)
       Return(Name("result"))
       .Stmts
endmodule
