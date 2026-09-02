requires "verification.k"

module REVIEWER-PROGRAM-IDENTITY
  imports VERIFICATION

  // Constructor-level equality between the proof's body aliases and the body
  // in the trusted-regenerated solution.mpy.
  claim [constructor-identity]:
    <k>
      #loadAll(Module(
        FuncDef("select_words", Params("s", "n"), selectWordsBody)
        .Stmts))
      =>
      #loadAll(Module(
        FuncDef("select_words", Params("s", "n"),
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("word"), Str(""))
          Assign(Name("count"), Int(0))
          Assign(Name("ch"), Str(""))
          For(Name("ch"), Name("s"),
            If(Compare(Name("ch"), CmpOp("==", Str(" "))),
              If(BoolOp("and",
                   Compare(Name("count"), CmpOp("==", Name("n"))),
                   Compare(Name("word"), CmpOp("!=", Str("")))),
                Expr(Call(Attribute(Name("result"), "append"), Name("word")))
                .Stmts,
                .Stmts)
              Assign(Name("word"), Str(""))
              Assign(Name("count"), Int(0)),
              Assign(Name("word"), BinOp("+", Name("word"), Name("ch")))
              If(Compare(Name("ch"), CmpOp("not in", Str("aeiouAEIOU"))),
                Assign(Name("count"),
                  BinOp("+", Name("count"), Int(1)))
                .Stmts,
                .Stmts)
              .Stmts)
            .Stmts)
          If(BoolOp("and",
               Compare(Name("count"), CmpOp("==", Name("n"))),
               Compare(Name("word"), CmpOp("!=", Str("")))),
            Expr(Call(Attribute(Name("result"), "append"), Name("word")))
            .Stmts,
            .Stmts)
          Return(Name("result")))
        .Stmts))
    </k>
endmodule
