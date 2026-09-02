requires "semantic.k"

module SOLUTION-PROGRAM
  imports MPY-SEMANTIC
  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("sorted_list_sum", Params("lst"),
        Return(
          Call(
            Name("sorted"),
            ListComp(Name("word"),
              CompFor(
                Name("word"),
                Name("lst"),
                Compare(
                  BinOp("%", Call(Name("len"), Name("word")), Int(2)),
                  CmpOp("==", Int(0))))),
            KwArg(
              "key",
              Lambda(
                Params("word"),
                CellVars(.Strings),
                FreeVars(.Strings),
                TupleExpr(Call(Name("len"), Name("word")), Name("word"))))))))
endmodule
