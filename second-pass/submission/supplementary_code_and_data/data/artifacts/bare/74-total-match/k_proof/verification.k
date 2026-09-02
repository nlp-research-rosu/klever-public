requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // The exact AST emitted into solution.mpy, named for readable claims.
  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("total_match", Params("lst1", "lst2"),
        Return(
          IfExp(
            Compare(
              Call(Name("sum"), Call(Name("map"), Name("len"), Name("lst1"))),
              CmpOp("<=",
                Call(Name("sum"), Call(Name("map"), Name("len"), Name("lst2"))))),
            Name("lst1"),
            Name("lst2")))))

  // Mathematical character-count measure used by the contract.
  syntax Int ::= totalChars(StrVals) [function]
  rule totalChars(SS) => sumInts(mapLengths(SS))
endmodule
