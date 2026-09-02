requires "verification.k"

module BODY-MUTATION
  imports VERIFICATION

  syntax Pgm ::= "mutatedProgram" [function]
  syntax Stmts ::= "mutatedDefs" [function]

  rule mutatedProgram => Module(mutatedDefs)

  // Material body mutation: multiplier 2 becomes 3 in the term that executes.
  rule mutatedDefs
    => FuncDef(
         "order_by_points", Params("nums"),
         Return(
           Call(
             Name("sorted"),
             Name("nums"),
             KwArg(
               "key",
               Lambda(
                 Params("n"), CellVars(.Ids), FreeVars(.Ids),
                 BinOp(
                   "-",
                   Call(
                     Name("sum"),
                     Call(
                       Name("map"), Name("int"),
                       Call(Name("str"), Call(Name("abs"), Name("n"))))),
                   IfExp(
                     Compare(Name("n"), CmpOp("<", Int(0))),
                     BinOp(
                       "*", Int(3),
                       Call(
                         Name("int"),
                         Subscript(
                           Call(
                             Name("str"), Call(Name("abs"), Name("n"))),
                           Int(0)))),
                     Int(0))))))))
endmodule
