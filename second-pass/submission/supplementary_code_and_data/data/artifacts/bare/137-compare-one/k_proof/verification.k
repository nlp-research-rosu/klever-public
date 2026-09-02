requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTIC

  // This macro is deliberately the same constructor tree as solution.mpy.
  // prove.sh checks that solution.mpy parses and executes independently too.
  syntax Pgm ::= "theSolution" [macro]
  rule theSolution =>
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
        Return(Name("b"))))
endmodule
