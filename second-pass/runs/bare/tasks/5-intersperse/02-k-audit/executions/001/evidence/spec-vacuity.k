requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false-result mutation: claim that D+1, rather than D, is inserted.
  // Satisfying counterexample: IS=7,8 and D=99 executes to [7,99,8], not [7,100,8].
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
