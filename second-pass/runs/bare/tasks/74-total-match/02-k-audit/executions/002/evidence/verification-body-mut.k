requires "semantic.k"

module VERIFICATION-BODY-MUT
  imports SEMANTIC

  // Material body mutation: swap the conditional's returned branches.
  syntax Program ::= "mutatedSolutionProgram" [macro]
  rule mutatedSolutionProgram =>
    Module(
      FuncDef("total_match", Params("lst1", "lst2"),
        Return(
          IfExp(
            Compare(
              Call(Name("sum"), Call(Name("map"), Name("len"), Name("lst1"))),
              CmpOp("<=",
                Call(Name("sum"), Call(Name("map"), Name("len"), Name("lst2"))))),
            Name("lst2"),
            Name("lst1")))))

  syntax Int ::= totalCharsMut(StrVals) [function]
  rule totalCharsMut(SS) => sumInts(mapLengths(SS))
endmodule
