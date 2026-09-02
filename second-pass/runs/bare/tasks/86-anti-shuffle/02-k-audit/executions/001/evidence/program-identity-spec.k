module PROGRAM-IDENTITY-SPEC
  imports VERIFICATION

  // RHS is the trusted-translator output for the submitted solution.py.
  claim
    <python>
      <k>
        run(solutionProgram, S:String) =>
        run(Module(
      FuncDef("insert_char", Params("char", "word", "before"),
        If(Compare(Name("word"), CmpOp("==", Str(""))),
          Return(BinOp("+", Name("before"), Name("char"))),
          .Stmts)
        If(Compare(Name("char"), CmpOp("<=", Subscript(Name("word"), Int(0)))),
          Return(
            BinOp(
              "+",
              BinOp("+", Name("before"), Name("char")),
              Name("word"))),
          .Stmts)
        Return(
          Call(
            Name("insert_char"),
            Name("char"),
            Subscript(Name("word"), Slice(Int(1), NoBound, NoBound)),
            BinOp("+", Name("before"), Subscript(Name("word"), Int(0))))))
      FuncDef("process_words", Params("text", "word", "result"),
        If(Compare(Name("text"), CmpOp("==", Str(""))),
          Return(BinOp("+", Name("result"), Name("word"))),
          .Stmts)
        If(Compare(Subscript(Name("text"), Int(0)), CmpOp("==", Str(" "))),
          Return(
            Call(
              Name("process_words"),
              Subscript(Name("text"), Slice(Int(1), NoBound, NoBound)),
              Str(""),
              BinOp("+", BinOp("+", Name("result"), Name("word")), Str(" ")))),
          .Stmts)
        Return(
          Call(
            Name("process_words"),
            Subscript(Name("text"), Slice(Int(1), NoBound, NoBound)),
            Call(
              Name("insert_char"),
              Subscript(Name("text"), Int(0)),
              Name("word"),
              Str("")),
            Name("result"))))
      FuncDef("anti_shuffle", Params("s"),
        Return(Call(Name("process_words"), Name("s"), Str(""), Str(""))))), S)
      </k>
      <functions> .Stmts </functions>
      <env> .Map </env>
      <result> "" </result>
    </python>
endmodule
