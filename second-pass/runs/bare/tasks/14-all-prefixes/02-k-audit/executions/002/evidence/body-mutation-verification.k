requires "verified-lemma.k"

module BODY-MUTATION-VERIFICATION
  imports VERIFIED-LEMMA

  syntax Program ::= "mutatedProgram" [function]
  rule mutatedProgram =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("all_prefixes", Params("string"),
        Assign(Name("result"), ListExpr())
        Assign(Name("i"), Int(2))
        While(Compare(Name("i"), CmpOp("<=", Call(Name("len"), Name("string")))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              Subscript(Name("string"), Slice(NoBound, Name("i"), NoBound))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("result"))))
endmodule
