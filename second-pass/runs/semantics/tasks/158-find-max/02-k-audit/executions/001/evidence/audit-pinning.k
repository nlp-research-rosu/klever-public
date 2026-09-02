requires "verification.k"

module AUDIT-PINNING
  imports VERIFICATION

  claim [loop-alias-is-submitted-body]:
    findMaxLoopBody
    =>
    Assign(
      Name("unique"),
      Call(Name("len"), Call(Name("set"), Name("word"))))
    If(Compare(Name("unique"), CmpOp(">", Name("max_unique"))),
      Assign(Name("best"), Name("word"))
      Assign(Name("max_unique"), Name("unique")),
      If(Compare(Name("unique"), CmpOp("==", Name("max_unique"))),
        If(Compare(Name("word"), CmpOp("<", Name("best"))),
          Assign(Name("best"), Name("word")),
          .Stmts),
        .Stmts))

  claim [function-alias-is-submitted-body]:
    findMaxFunctionBody
    =>
    Assign(Name("best"), Str(""))
    Assign(Name("max_unique"), Int(0))
    Assign(Name("word"), Str(""))
    Assign(Name("unique"), Int(0))
    For(Name("word"), Name("words"),
      Assign(
        Name("unique"),
        Call(Name("len"), Call(Name("set"), Name("word"))))
      If(Compare(Name("unique"), CmpOp(">", Name("max_unique"))),
        Assign(Name("best"), Name("word"))
        Assign(Name("max_unique"), Name("unique")),
        If(Compare(Name("unique"), CmpOp("==", Name("max_unique"))),
          If(Compare(Name("word"), CmpOp("<", Name("best"))),
            Assign(Name("best"), Name("word")),
            .Stmts),
          .Stmts)))
    Return(Name("best"))
endmodule
