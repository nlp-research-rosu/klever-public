requires "semantic.k"

module VERIFICATION-BODY-MUTATION
  imports MPY

  // Reviewer mutation: for each selected value, add value^2 + 1.
  syntax Stmts ::= "mutatedLoopBody" [function]
  rule mutatedLoopBody
    => If(Call(Name("isinstance"), Name("value"), Name("int")),
         If(Compare(Name("value"), CmpOp(">=", Int(0))),
            If(Compare(BinOp("%", Name("value"), Int(2)),
                       CmpOp("==", Int(1))),
               Assign(Name("total"),
                      BinOp("+",
                        BinOp("+", Name("total"),
                             BinOp("*", Name("value"), Name("value"))),
                        Int(1))),
               .Stmts),
            .Stmts),
         .Stmts)

  syntax Module ::= "solutionProgramMutation" [function]
  rule solutionProgramMutation
    => Module(
         FuncDef("double_the_difference", Params("lst"),
           Assign(Name("total"), Int(0))
           For(Name("value"), Name("lst"), mutatedLoopBody)
           Return(Name("total"))))
endmodule
