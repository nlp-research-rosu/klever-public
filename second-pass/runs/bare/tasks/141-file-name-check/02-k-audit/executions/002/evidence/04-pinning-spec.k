requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  claim <k> solutionProgram
          => Module(
    FuncDef("file_name_check", Params("file_name"),
      Assign(
        Name("digits"),
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
                            Attribute(Name("file_name"), "count"),
                            Str("0")),
                          Call(
                            Attribute(Name("file_name"), "count"),
                            Str("1"))),
                        Call(
                          Attribute(Name("file_name"), "count"),
                          Str("2"))),
                      Call(
                        Attribute(Name("file_name"), "count"),
                        Str("3"))),
                    Call(Attribute(Name("file_name"), "count"), Str("4"))),
                  Call(Attribute(Name("file_name"), "count"), Str("5"))),
                Call(Attribute(Name("file_name"), "count"), Str("6"))),
              Call(Attribute(Name("file_name"), "count"), Str("7"))),
            Call(Attribute(Name("file_name"), "count"), Str("8"))),
          Call(Attribute(Name("file_name"), "count"), Str("9"))))
      If(Compare(
        Call(Attribute(Name("file_name"), "count"), Str(".")),
        CmpOp("!=", Int(1))),
        Return(Str("No")),
        .Stmts)
      If(Compare(Name("digits"), CmpOp(">", Int(3))),
        Return(Str("No")),
        .Stmts)
      If(Compare(Call(Name("len"), Name("file_name")), CmpOp("==", Int(0))),
        Return(Str("No")),
        .Stmts)
      Assign(Name("first"), Subscript(Name("file_name"), Int(0)))
      If(UnaryOp(
        "not",
        BoolOp(
          "or",
          BoolOp(
            "and",
            Compare(Str("a"), CmpOp("<=", Name("first"))),
            Compare(Name("first"), CmpOp("<=", Str("z")))),
          BoolOp(
            "and",
            Compare(Str("A"), CmpOp("<=", Name("first"))),
            Compare(Name("first"), CmpOp("<=", Str("Z")))))),
        Return(Str("No")),
        .Stmts)
      If(BoolOp(
        "or",
        Call(Attribute(Name("file_name"), "endswith"), Str(".txt")),
        Call(Attribute(Name("file_name"), "endswith"), Str(".exe")),
        Call(Attribute(Name("file_name"), "endswith"), Str(".dll"))),
        Return(Str("Yes")),
        .Stmts)
      Return(Str("No"))))
        </k>
endmodule
