requires "reference-semantics/semantics.k"

module WORDS-STRING-VERIFICATION
  imports MPY

  // This is exactly the function body emitted in solution.mpy, represented as
  // a callable value so that a symbolic claim can invoke it with any string.
  syntax Val ::= "wordsStringFunction" [function]
  rule wordsStringFunction =>
    closureVal(
      ("s", .ParamNames),
      Return(
        Call(
          Attribute(
            Call(
              Attribute(Name("s"), "replace"),
              (Str(","), Str(" "), .Exprs)),
            "split"),
          .Exprs))
      .Stmts,
      0)

  // Contract oracle: commas become spaces, then Python whitespace splitting
  // drops empty fields. Both helpers are defined by the reference semantics.
  syntax ValSeq ::= wordsStringExpected(IntSeq) [function, total]
  rule wordsStringExpected(CS:IntSeq) =>
    splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq)
endmodule
