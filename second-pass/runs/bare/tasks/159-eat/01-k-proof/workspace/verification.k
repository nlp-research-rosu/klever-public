requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // The independently stated mathematical contract for the rabbit task.
  rule carrotContract(NUMBER, NEED, REMAINING)
    => result(NUMBER +Int NEED, REMAINING -Int NEED)
    requires NEED <=Int REMAINING
  rule carrotContract(NUMBER, NEED, REMAINING)
    => result(NUMBER +Int REMAINING, 0)
    requires REMAINING <Int NEED

  rule validInput(NUMBER, NEED, REMAINING)
    => (0 <=Int NUMBER andBool NUMBER <=Int 1000)
       andBool (0 <=Int NEED andBool NEED <=Int 1000)
       andBool (0 <=Int REMAINING andBool REMAINING <=Int 1000)

  // This is exactly the constructor tree generated in solution.mpy.
  rule solutionProgram
    => Module(
         FuncDef("eat", Params("number", "need", "remaining"),
           If(Compare(Name("need"), CmpOp("<=", Name("remaining"))),
             Return(ListExpr(
               BinOp("+", Name("number"), Name("need")),
               BinOp("-", Name("remaining"), Name("need"))
             )),
             .Stmts
           )
           Return(ListExpr(
             BinOp("+", Name("number"), Name("remaining")),
             Int(0)
           ))
         )
       )
endmodule
