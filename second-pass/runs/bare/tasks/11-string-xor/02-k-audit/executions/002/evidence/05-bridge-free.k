requires "semantic.k"

module XOR-BRIDGE-FREE
  imports XOR-SEMANTICS

  syntax Module ::= "solutionProgramCore" [macro]
  rule solutionProgramCore =>
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

  syntax Stmts ::= "solutionBodyCore" [macro]
  rule solutionBodyCore =>
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

  syntax Text ::= "xorTextCore" "(" Int "," Int "," Stream "," Stream ")" [function]
  rule xorTextCore(N, _, _, _) => empty
    requires N ==Int 0
  rule xorTextCore(N, M, _, _) => empty
    requires N >Int 0 andBool M ==Int 0
  rule xorTextCore(N, M, S1, S2) =>
    cons(head(S1) xorBool head(S2),
         xorTextCore(N -Int 1, M -Int 1, next(S1), next(S2)))
    requires N >Int 0 andBool M >Int 0
endmodule
