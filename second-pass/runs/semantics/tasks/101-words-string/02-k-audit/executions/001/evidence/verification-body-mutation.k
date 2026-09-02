requires "reference-semantics/semantics.k"

module WORDS-STRING-VERIFICATION-BODY-MUTATION
  imports MPY

  // Deliberate operational-sensitivity mutation: commas become "X", while
  // the postcondition summary below still requires commas to become spaces.
  syntax Val ::= "wordsStringFunctionBodyMutation" [function]
  rule wordsStringFunctionBodyMutation =>
    closureVal(
      ("s", .ParamNames),
      Return(
        Call(
          Attribute(
            Call(
              Attribute(Name("s"), "replace"),
              (Str(","), Str("X"), .Exprs)),
            "split"),
          .Exprs))
      .Stmts,
      0)

  syntax ValSeq ::= wordsStringExpectedBodyMutation(IntSeq) [function, total]
  rule wordsStringExpectedBodyMutation(CS:IntSeq) =>
    splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq)
endmodule
