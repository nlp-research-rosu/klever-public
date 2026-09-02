requires "verification.k"

module AUDIT-PINNING-SPEC
  imports VERIFICATION

  // The RHS is the trusted-translator output in regenerated-solution.mpy.
  // This auxiliary claim checks that the term used by the entry claim unfolds
  // to that exact submitted program AST.
  claim [exact-module]:
    <k>
      solutionModule()
      =>
      Module(
      FuncDef("_number_value", Params("number"),
        If(Compare(Name("number"), CmpOp("==", Str("zero"))),
          Return(Int(0)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("one"))),
          Return(Int(1)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("two"))),
          Return(Int(2)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("three"))),
          Return(Int(3)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("four"))),
          Return(Int(4)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("five"))),
          Return(Int(5)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("six"))),
          Return(Int(6)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("seven"))),
          Return(Int(7)),
          .Stmts)
        If(Compare(Name("number"), CmpOp("==", Str("eight"))),
          Return(Int(8)),
          .Stmts)
        Return(Int(9)) .Stmts)
      FuncDef("sort_numbers", Params("numbers"),
        Return(
          Call(
            Attribute(Str(" "), "join"),
            Call(
              Name("sorted"),
              Call(Attribute(Name("numbers"), "split"), .Exprs),
              KwArg("key", Name("_number_value")))))
        .Stmts))
    </k>
endmodule
