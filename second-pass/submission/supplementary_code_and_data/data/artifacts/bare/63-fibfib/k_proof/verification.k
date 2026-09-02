module FIBFIB-VERIFICATION
  imports FIBFIB-SYNTAX
  imports INT

  syntax Int ::= fibfibMath(Int) [function, total]
  syntax Pgm ::= "fibfibProgram" [macro]
  syntax Expr ::= "loopCondition" [macro]
  syntax Stmts ::= "loopBody" [macro]

  rule loopCondition
    => Compare(Name("i"), CmpOp("<", Name("n")))

  rule loopBody
    => Assign(
         TupleExpr(Name("a"), Name("b"), Name("c")),
         TupleExpr(Name("b"), Name("c"),
           BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c"))))
       Assign(Name("i"), BinOp("+", Name("i"), Int(1)))

  rule fibfibProgram
    => Module(
         FuncDef("fibfib", Params("n"),
           Assign(Name("a"), Int(0))
           Assign(Name("b"), Int(0))
           Assign(Name("c"), Int(1))
           Assign(Name("i"), Int(0))
           While(loopCondition, loopBody)
           Return(Name("a"))))

  rule fibfibMath(N) => 0 requires N <=Int 1
  rule fibfibMath(2) => 1
  rule fibfibMath(N) => fibfibMath(N -Int 1)
                         +Int fibfibMath(N -Int 2)
                         +Int fibfibMath(N -Int 3)
    requires N >=Int 3
endmodule
