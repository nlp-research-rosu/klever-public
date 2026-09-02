requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  // RHS is the byte-regenerated solution.mpy constructor tree.
  claim <k> solutionProgram ~> invoke(S) =>
    Module(
      FuncDef("sort_numbers", Params("numbers"),
        Return(
          Call(
            Attribute(
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
                                  "*",
                                  Str("zero "),
                                  Call(
                                    Attribute(Name("numbers"), "count"),
                                    Str("zero"))),
                                BinOp(
                                  "*",
                                  Str("one "),
                                  Call(
                                    Attribute(Name("numbers"), "count"),
                                    Str("one")))),
                              BinOp(
                                "*",
                                Str("two "),
                                Call(
                                  Attribute(Name("numbers"), "count"),
                                  Str("two")))),
                            BinOp(
                              "*",
                              Str("three "),
                              Call(
                                Attribute(Name("numbers"), "count"),
                                Str("three")))),
                          BinOp(
                            "*",
                            Str("four "),
                            Call(
                              Attribute(Name("numbers"), "count"),
                              Str("four")))),
                        BinOp(
                          "*",
                          Str("five "),
                          Call(
                            Attribute(Name("numbers"), "count"),
                            Str("five")))),
                      BinOp(
                        "*",
                        Str("six "),
                        Call(
                          Attribute(Name("numbers"), "count"),
                          Str("six")))),
                    BinOp(
                      "*",
                      Str("seven "),
                      Call(
                        Attribute(Name("numbers"), "count"),
                        Str("seven")))),
                  BinOp(
                    "*",
                    Str("eight "),
                    Call(
                      Attribute(Name("numbers"), "count"), Str("eight")))),
                BinOp(
                  "*",
                  Str("nine "),
                  Call(Attribute(Name("numbers"), "count"), Str("nine")))),
              "strip"),
            .Exprs)))) ~> invoke(S) </k>
endmodule
