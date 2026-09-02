requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  // The universal claim instantiated at numbers=[7,8], delimeter=99.
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
              ListExpr(Subscript(Name("numbers"), Int(0)), Name("delimeter")),
              Call(
                Name("intersperse"),
                Subscript(Name("numbers"), Slice(Int(1), NoBound, NoBound)),
                Name("delimeter")))))),
      "intersperse",
      VList([7, 8]), VInt(99)) ~> KONT:K
    => VList([7, 99, 8]) ~> KONT
  </k>
endmodule
