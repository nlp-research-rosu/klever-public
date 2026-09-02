requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Readable name for the exact constructor tree emitted in solution.mpy.
  syntax ModuleAst ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("mean_absolute_deviation", Params("numbers"),
              CellVars("mean"), FreeVars(.Strings),
        Assign(
          Name("mean"),
          BinOp("/",
            Call(Name("sum"), Name("numbers")),
            Call(Name("len"), Name("numbers"))))
        Return(
          BinOp("/",
            Call(Name("sum"),
              ListComp(
                Call(Name("abs"), BinOp("-", Name("x"), Name("mean"))),
                CompFor(Name("x"), Name("numbers"), Bool(true)))),
            Call(Name("len"), Name("numbers"))))))

  // Mathematical contract, separate from the operational evaluator:
  // MAD(xs) = sum(|x - sum(xs)/|xs||)/|xs|.
  syntax Num ::= "mathMAD" "(" Nums ")" [function]
  rule mathMAD(NS) =>
    divNum(sumAbs(NS, divNum(sumNums(NS), countNums(NS))), countNums(NS))
endmodule
