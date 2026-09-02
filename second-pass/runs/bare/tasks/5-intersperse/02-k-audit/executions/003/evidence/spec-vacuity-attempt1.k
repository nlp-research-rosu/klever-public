requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Rejected reviewer attempt: this mutation parsed, but the backend stopped
  // on an unrelated DecidePredicateUnknown state, so it is not non-vacuity
  // evidence.
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
    => VList([D, intersperseSpec(IS, D)]) ~> KONT
  </k>
endmodule
