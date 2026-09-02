requires "reference-semantics/semantics.k"

module ROUNDED-AVG-VERIFICATION-BODY-MUTANT
  imports MPY

  // This is exactly the translated body of rounded_avg from solution.mpy.
  // Naming it here keeps each reachability claim focused on its input class
  // and expected result.
  syntax Stmts ::= "roundedAvgBody" [function, total]
  rule roundedAvgBody
    => If(Compare(Name("n"), CmpOp(">", Name("m"))),
         Return(UnaryOp("-", Int(1))),
         .Stmts)
       Assign(Name("total"), BinOp("+", Name("n"), Name("m")))
       Assign(Name("average"), BinOp("//", Name("total"), Int(2)))
       If(Compare(BinOp("%", Name("total"), Int(2)),
                  CmpOp("==", Int(1))),
          If(Compare(BinOp("%", Name("average"), Int(2)),
                     CmpOp("==", Int(1))),
             Assign(Name("average"),
                    BinOp("+", Name("average"), Int(2))),
             .Stmts),
          .Stmts)
       Return(Call(Name("bin"), Name("average"), .Exprs))
       .Stmts

  // A direct entry-point call. Its closure has the module scope as parent,
  // just as the closure produced by the module-level FuncDef in solution.mpy.
  syntax Expr ::= roundedAvgCall(Int, Int) [function, total]
  rule roundedAvgCall(N:Int, M:Int)
    => Call(closureVal(("n", "m", .ParamNames), roundedAvgBody, 0),
            (N, M, .Exprs))
endmodule
