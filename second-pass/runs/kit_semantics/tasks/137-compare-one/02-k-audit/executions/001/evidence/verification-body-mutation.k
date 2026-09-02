requires "/tmp/audit-work/reconstruction/reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTATION
  imports MPY

  // Material mutation: in the first greater-than branch, return b instead of a.
  syntax Module ::= mutatedSolutionModule() [function, total]
  rule mutatedSolutionModule()
    => Module(
         FuncDef("compare_one", Params("a", "b"),
           If(Call(Name("isinstance"), Name("a"), Name("str")),
             Assign(Name("a_value"),
               Call(Name("float"),
                 Call(Attribute(Name("a"), "replace"), Str(","), Str(".")))) .Stmts,
             Assign(Name("a_value"), Name("a")) .Stmts)
           If(Call(Name("isinstance"), Name("b"), Name("str")),
             Assign(Name("b_value"),
               Call(Name("float"),
                 Call(Attribute(Name("b"), "replace"), Str(","), Str(".")))) .Stmts,
             Assign(Name("b_value"), Name("b")) .Stmts)
           If(Compare(Name("a_value"), CmpOp(">", Name("b_value"))),
             Return(Name("b")) .Stmts, .Stmts)
           If(Compare(Name("b_value"), CmpOp(">", Name("a_value"))),
             Return(Name("b")) .Stmts, .Stmts)
           Return(NoneVal) .Stmts))
endmodule
