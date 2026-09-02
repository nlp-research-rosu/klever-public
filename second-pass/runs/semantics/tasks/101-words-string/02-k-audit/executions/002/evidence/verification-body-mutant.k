requires "verification.k"

module WORDS-STRING-BODY-MUTANT
  imports WORDS-STRING-VERIFICATION

  syntax Val ::= "wordsStringFunctionMutant" [function]
  rule wordsStringFunctionMutant =>
    closureVal(
      ("s", .ParamNames),
      Return(
        Call(
          Attribute(
            Call(
              Attribute(Name("s"), "replace"),
              (Str(","), Str("x"), .Exprs)),
            "split"),
          .Exprs))
      .Stmts,
      0)
endmodule
