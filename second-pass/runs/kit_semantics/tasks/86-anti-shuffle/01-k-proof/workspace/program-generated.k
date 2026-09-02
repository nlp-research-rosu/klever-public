// Generated from solution.py; sha256=e088ef66a781f529cf950b58790d19b7a2f8b37f2fd4b024bb23fc6840b948da
// Regenerate with: python3 generate_program_module.py
requires "reference-semantics/semantics.k"

module PROGRAM-GENERATED
  imports MPY

  syntax Module ::= solutionModule() [function, total]
  rule solutionModule()
    =>
      Module(
        FuncDef("anti_shuffle", Params("s"),
          Assign(Name("result"), Str(""))
          Assign(Name("word"), Str(""))
          Assign(Name("char"), Str(""))
          Assign(Name("new_word"), Str(""))
          Assign(Name("inserted"), Bool(false))
          Assign(Name("old_char"), Str(""))
          For(Name("char"), Name("s"),
            If(Compare(Name("char"), CmpOp("==", Str(" "))),
              AugAssign(Name("result"), "+", Name("word"))
              AugAssign(Name("result"), "+", Str(" "))
              Assign(Name("word"), Str("")),
              Assign(Name("new_word"), Str(""))
              Assign(Name("inserted"), Bool(false))
              For(Name("old_char"), Name("word"),
                If(BoolOp(
                  "and",
                  UnaryOp("not", Name("inserted")),
                  Compare(Name("char"), CmpOp("<", Name("old_char")))),
                  AugAssign(Name("new_word"), "+", Name("char"))
                  Assign(Name("inserted"), Bool(true)),
                  .Stmts)
                AugAssign(Name("new_word"), "+", Name("old_char")))
              If(UnaryOp("not", Name("inserted")),
                AugAssign(Name("new_word"), "+", Name("char"))
                Assign(Name("inserted"), Bool(true)),
                .Stmts)
              Assign(Name("word"), Name("new_word"))))
          AugAssign(Name("result"), "+", Name("word"))
          Return(Name("result"))))

  syntax Stmts ::= solutionBody() [function, total]
  rule solutionBody()
    =>
      Assign(Name("result"), Str(""))
      Assign(Name("word"), Str(""))
      Assign(Name("char"), Str(""))
      Assign(Name("new_word"), Str(""))
      Assign(Name("inserted"), Bool(false))
      Assign(Name("old_char"), Str(""))
      For(Name("char"), Name("s"),
        If(Compare(Name("char"), CmpOp("==", Str(" "))),
          AugAssign(Name("result"), "+", Name("word"))
          AugAssign(Name("result"), "+", Str(" "))
          Assign(Name("word"), Str("")),
          Assign(Name("new_word"), Str(""))
          Assign(Name("inserted"), Bool(false))
          For(Name("old_char"), Name("word"),
            If(BoolOp(
              "and",
              UnaryOp("not", Name("inserted")),
              Compare(Name("char"), CmpOp("<", Name("old_char")))),
              AugAssign(Name("new_word"), "+", Name("char"))
              Assign(Name("inserted"), Bool(true)),
              .Stmts)
            AugAssign(Name("new_word"), "+", Name("old_char")))
          If(UnaryOp("not", Name("inserted")),
            AugAssign(Name("new_word"), "+", Name("char"))
            Assign(Name("inserted"), Bool(true)),
            .Stmts)
          Assign(Name("word"), Name("new_word"))))
      AugAssign(Name("result"), "+", Name("word"))
      Return(Name("result"))
endmodule
