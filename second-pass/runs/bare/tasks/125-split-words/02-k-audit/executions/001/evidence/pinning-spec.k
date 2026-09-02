requires "verification.k"

module AUDIT-PINNING-SPEC
  imports MPY-VERIFICATION

  // RHS is the byte-regenerated solution.mpy constructor term.
  claim <k> solutionAST =>
    Module(
      FuncDef("split_words", Params("txt"),
        Assign(Name("words"), Call(Attribute(Name("txt"), "split"), .Exprs))
        If(Compare(
          Call(Attribute(Str(""), "join"), Name("words")),
          CmpOp("!=", Name("txt"))),
          Return(Name("words")),
          .Stmts)
        If(Compare(Str(","), CmpOp("in", Name("txt"))),
          Return(Call(Attribute(Name("txt"), "split"), Str(","))),
          .Stmts)
        Return(
          BinOp(
            "+",
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            BinOp(
                              "+",
                              BinOp(
                                "+",
                                BinOp(
                                  "+",
                                  Call(
                                    Attribute(Name("txt"), "count"),
                                    Str("b")),
                                  Call(
                                    Attribute(Name("txt"), "count"),
                                    Str("d"))),
                                Call(
                                  Attribute(Name("txt"), "count"),
                                  Str("f"))),
                              Call(
                                Attribute(Name("txt"), "count"),
                                Str("h"))),
                            Call(Attribute(Name("txt"), "count"), Str("j"))),
                          Call(Attribute(Name("txt"), "count"), Str("l"))),
                        Call(Attribute(Name("txt"), "count"), Str("n"))),
                      Call(Attribute(Name("txt"), "count"), Str("p"))),
                    Call(Attribute(Name("txt"), "count"), Str("r"))),
                  Call(Attribute(Name("txt"), "count"), Str("t"))),
                Call(Attribute(Name("txt"), "count"), Str("v"))),
              Call(Attribute(Name("txt"), "count"), Str("x"))),
            Call(Attribute(Name("txt"), "count"), Str("z")))))) </k>
endmodule
