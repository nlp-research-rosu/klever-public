requires "semantic.k"

module XOR-VERIFICATION-NO-BRIDGES
  imports XOR-SEMANTICS

  // A named copy of the exact term emitted in solution.mpy.  This keeps the
  // claims readable; prove.sh checks equivalence, parsing, and execution.
  syntax Module ::= "solutionProgram" [macro]
  // BEGIN EXACT SOLUTION TERM
  rule solutionProgram =>
    Module(
      FuncDef("string_xor", Params("a", "b"),
        If(Compare(Name("a"), CmpOp("==", Str(""))),
          Return(Str("")),
          .Stmts)
        If(Compare(Name("b"), CmpOp("==", Str(""))),
          Return(Str("")),
          .Stmts)
        If(Compare(
          Subscript(Name("a"), Int(0)),
          CmpOp("==", Subscript(Name("b"), Int(0)))),
          Return(
            BinOp(
              "+",
              Str("0"),
              Call(
                Name("string_xor"),
                Subscript(Name("a"), Slice(Int(1), NoBound, NoBound)),
                Subscript(Name("b"), Slice(Int(1), NoBound, NoBound))))),
          .Stmts)
        Return(
          BinOp(
            "+",
            Str("1"),
            Call(
              Name("string_xor"),
              Subscript(Name("a"), Slice(Int(1), NoBound, NoBound)),
              Subscript(Name("b"), Slice(Int(1), NoBound, NoBound)))))))
  // END EXACT SOLUTION TERM

  syntax Stmts ::= "solutionBody" [macro]
  rule solutionBody =>
    If(Compare(Name("a"), CmpOp("==", Str(""))),
      Return(Str("")),
      .Stmts)
    If(Compare(Name("b"), CmpOp("==", Str(""))),
      Return(Str("")),
      .Stmts)
    If(Compare(
      Subscript(Name("a"), Int(0)),
      CmpOp("==", Subscript(Name("b"), Int(0)))),
      Return(
        BinOp(
          "+",
          Str("0"),
          Call(
            Name("string_xor"),
            Subscript(Name("a"), Slice(Int(1), NoBound, NoBound)),
            Subscript(Name("b"), Slice(Int(1), NoBound, NoBound))))),
      .Stmts)
    Return(
      BinOp(
        "+",
        Str("1"),
        Call(
          Name("string_xor"),
          Subscript(Name("a"), Slice(Int(1), NoBound, NoBound)),
          Subscript(Name("b"), Slice(Int(1), NoBound, NoBound)))))

  // Mathematical reference function, deliberately separate from the AST
  // evaluator above.  xorText consumes bits until either input is exhausted.
  syntax Text ::= "xorText" "(" Int "," Int "," Stream "," Stream ")" [function]
  rule xorText(N, _, _, _) => empty
    requires N ==Int 0
  rule xorText(N, M, _, _) => empty
    requires N >Int 0 andBool M ==Int 0
  rule xorText(N, M, S1, S2) =>
    cons(head(S1) xorBool head(S2),
         xorText(N -Int 1, M -Int 1, next(S1), next(S2)))
    requires N >Int 0 andBool M >Int 0

endmodule
