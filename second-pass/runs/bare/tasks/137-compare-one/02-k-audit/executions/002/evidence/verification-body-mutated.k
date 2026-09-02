requires "semantic.k"

module VERIFICATION-BODY-MUTATED
  imports MPY-SEMANTIC

  syntax Pgm ::= "theSolutionBodyMutated" [macro]
  rule theSolutionBodyMutated =>
    Module(
      FuncDef("compare_one", Params("a", "b"),
        If(Compare(Call(Name("type"), Name("a")), CmpOp("==", Name("str"))),
          Assign(
            Name("a_value"),
            Call(
              Name("float"),
              Call(Attribute(Name("a"), "replace"), Str(","), Str(".")))),
          Assign(Name("a_value"), Call(Name("float"), Name("a"))))
        If(Compare(Call(Name("type"), Name("b")), CmpOp("==", Name("str"))),
          Assign(
            Name("b_value"),
            Call(
              Name("float"),
              Call(Attribute(Name("b"), "replace"), Str(","), Str(".")))),
          Assign(Name("b_value"), Call(Name("float"), Name("b"))))
        If(Compare(Name("a_value"), CmpOp("==", Name("b_value"))),
          Return(NoneVal),
          .Stmts)
        If(Compare(Name("a_value"), CmpOp(">", Name("b_value"))),
          Return(Name("a")),
          .Stmts)
        // Reviewer mutation: the final return is a instead of b.
        Return(Name("a"))))
endmodule
