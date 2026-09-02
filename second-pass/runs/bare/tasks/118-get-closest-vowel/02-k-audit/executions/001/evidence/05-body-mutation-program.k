module SOLUTION-PROGRAM
  imports MPY-SYNTAX
  syntax Module ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("get_closest_vowel", Params("word"),
        Assign(Name("vowels"), Str(""))
        If(Compare(Call(Name("len"), Name("word")), CmpOp("<", Int(3))),
          Return(Str("")),
          .Stmts)
        If(Compare(
          Subscript(Name("word"), UnaryOp("-", Int(2))),
          CmpOp("in", Name("vowels"))),
          If(Compare(
            Subscript(Name("word"), UnaryOp("-", Int(3))),
            CmpOp("not in", Name("vowels"))),
            If(Compare(
              Subscript(Name("word"), UnaryOp("-", Int(1))),
              CmpOp("not in", Name("vowels"))),
              Return(Subscript(Name("word"), UnaryOp("-", Int(2)))),
              .Stmts),
            .Stmts),
          .Stmts)
        Return(
          Call(
            Name("get_closest_vowel"),
            Subscript(
              Name("word"),
              Slice(NoBound, UnaryOp("-", Int(1)), NoBound))))))
endmodule
