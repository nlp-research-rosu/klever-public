requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Reviewer mutation: preserve the exact executed program, but demand that
  // inserted delimiters are D + 1. For IS = 1,2,.Ints, D = 4, KONT = .K,
  // Python and the semantics return [1,4,2], while this requires [1,5,2].
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
      VList([IS]), VInt(D)) ~> KONT:K
    => VList([intersperseSpec(IS, D +Int 1)]) ~> KONT
  </k>
endmodule
