requires "/tmp/audit-work/fresh/reference-semantics/semantics.k"

module HOW-MANY-TIMES-FIXED-AUDIT
  imports MPY

  // Exact submitted function body, but deliberately no candidate proof bridge.
  syntax Stmts ::= "howManyTimesBodyFixed" [macro]
  rule howManyTimesBodyFixed
    => If(Compare(Name("substring"), CmpOp("==", Str(""))),
          Return(BinOp("+", Call(Name("len"), Name("string")), Int(1))),
          .Stmts)
       If(Compare(Name("string"), CmpOp("==", Str(""))),
          Return(Int(0)),
          .Stmts)
       Return(
         BinOp(
           "+",
           IfExp(
             Call(Attribute(Name("string"), "startswith"), Name("substring")),
             Int(1),
             Int(0)),
           Call(
             Name("how_many_times"),
             Subscript(Name("string"), Slice(Int(1), NoBound, NoBound)),
             Name("substring"))))
       .Stmts
endmodule
