requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact constructor body emitted for split_words by py2mpy.py.
  syntax Stmts ::= "splitWordsBody" [function, total]
  rule splitWordsBody =>
    Assign(Name("parts"), Call(Attribute(Name("txt"), "split"), .Exprs))
    If(
      BoolOp(
        "and",
        Name("txt"),
        Compare(Name("parts"), CmpOp("!=", ListExpr(Name("txt"), .Exprs))),
        .Exprs
      ),
      Return(Name("parts")) .Stmts,
      .Stmts
    )
    If(
      Compare(Str(","), CmpOp("in", Name("txt"))),
      Return(Call(Attribute(Name("txt"), "split"), Str(","), .Exprs)) .Stmts,
      .Stmts
    )
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
                              Call(Attribute(Name("txt"), "count"), Str("b"), .Exprs),
                              Call(Attribute(Name("txt"), "count"), Str("d"), .Exprs)
                            ),
                            Call(Attribute(Name("txt"), "count"), Str("f"), .Exprs)
                          ),
                          Call(Attribute(Name("txt"), "count"), Str("h"), .Exprs)
                        ),
                        Call(Attribute(Name("txt"), "count"), Str("j"), .Exprs)
                      ),
                      Call(Attribute(Name("txt"), "count"), Str("l"), .Exprs)
                    ),
                    Call(Attribute(Name("txt"), "count"), Str("n"), .Exprs)
                  ),
                  Call(Attribute(Name("txt"), "count"), Str("p"), .Exprs)
                ),
                Call(Attribute(Name("txt"), "count"), Str("r"), .Exprs)
              ),
              Call(Attribute(Name("txt"), "count"), Str("t"), .Exprs)
            ),
            Call(Attribute(Name("txt"), "count"), Str("v"), .Exprs)
          ),
          Call(Attribute(Name("txt"), "count"), Str("x"), .Exprs)
        ),
        Call(Attribute(Name("txt"), "count"), Str("z"), .Exprs)
      )
    ) .Stmts

  // Direct mathematical restatement of the requested odd zero-based
  // lowercase alphabet positions: b, d, ..., z.
  syntax Int ::= oddAlphabetCount(IntSeq) [function, total]
  rule oddAlphabetCount(CS) =>
    cntSub(CS, iCons(98,  .IntSeq))
      +Int cntSub(CS, iCons(100, .IntSeq))
      +Int cntSub(CS, iCons(102, .IntSeq))
      +Int cntSub(CS, iCons(104, .IntSeq))
      +Int cntSub(CS, iCons(106, .IntSeq))
      +Int cntSub(CS, iCons(108, .IntSeq))
      +Int cntSub(CS, iCons(110, .IntSeq))
      +Int cntSub(CS, iCons(112, .IntSeq))
      +Int cntSub(CS, iCons(114, .IntSeq))
      +Int cntSub(CS, iCons(116, .IntSeq))
      +Int cntSub(CS, iCons(118, .IntSeq))
      +Int cntSub(CS, iCons(120, .IntSeq))
      +Int cntSub(CS, iCons(122, .IntSeq))
endmodule
