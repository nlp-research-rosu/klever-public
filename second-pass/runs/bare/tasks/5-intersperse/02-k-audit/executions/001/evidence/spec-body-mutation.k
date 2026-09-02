requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Sensitivity test: the source body now inserts the first input element
  // instead of delimeter. The original result contract is deliberately kept.
  claim <k>
    Invoke(
      Module(
        ImportFrom("typing", "List")
        FuncDef("intersperse", Params("numbers", "delimeter"),
          If(Compare(Call(Name("len"), Name("numbers")), CmpOp("<=", Int(1))),
            Return(Name("numbers")),
            .Stmts)
          Return(
            BinOp(
              "+",
              ListExpr(
                Subscript(Name("numbers"), Int(0)),
                Subscript(Name("numbers"), Int(0))),
              Call(
                Name("intersperse"),
                Subscript(Name("numbers"), Slice(Int(1), NoBound, NoBound)),
                Name("delimeter")))))),
      "intersperse",
      VList([IS]), VInt(D)) ~> KONT:K
    => VList([intersperseSpec(IS, D)]) ~> KONT
  </k>
endmodule
