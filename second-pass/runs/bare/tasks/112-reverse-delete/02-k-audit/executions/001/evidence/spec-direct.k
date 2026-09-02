requires "verification.k"

module SPEC-DIRECT
  imports VERIFICATION

  // Directly embeds the exact constructor tree regenerated into solution.mpy.
  claim [direct-program]:
        <k>
          execute(
            Module(
              FuncDef("reverse_delete", Params("s", "c"),
                Assign(Name("result"), Str(""))
                For(Name("ch"), Name("s"),
                  If(Compare(Name("ch"), CmpOp("not in", Name("c"))),
                    Assign(Name("result"),
                      BinOp("+", Name("result"), Name("ch"))),
                    .Stmts))
                Return(
                  TupleExpr(
                    Name("result"),
                    Compare(
                      Name("result"),
                      CmpOp(
                        "==",
                        Subscript(
                          Name("result"),
                          Slice(
                            NoBound,
                            NoBound,
                            UnaryOp("-", Int(1)))))))))),
            S:String,
            C:String)
          => returned(expectedResult(S, C))
        </k>
endmodule
