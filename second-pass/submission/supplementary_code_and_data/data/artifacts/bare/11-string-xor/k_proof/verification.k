requires "semantic.k"

module XOR-VERIFICATION
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

  // A one-unfold symbolic acceleration of the operational rules.  Its first
  // argument is the exact translated body above, so changing the program
  // invalidates the match.  Recursive calls remain operational and therefore
  // require the circular claim in spec.k.
  syntax Sem ::= "prependResult" "(" Bool "," Sem ")" [strict(2)]
  rule prependResult(B, returned(str(T))) => returned(str(cons(B, T)))

  rule exec(solutionBody,
            env(str(segment(N, _S1)), str(segment(_M, _S2))),
            solutionBody)
    => returned(str(empty))
    requires N ==Int 0
    [priority(40)]

  rule exec(solutionBody,
            env(str(segment(N, _S1)), str(segment(M, _S2))),
            solutionBody)
    => returned(str(empty))
    requires N >Int 0 andBool M ==Int 0
    [priority(40)]

  rule exec(solutionBody,
            env(str(segment(N, S1)), str(segment(M, S2))),
            solutionBody)
    => prependResult(
         head(S1) xorBool head(S2),
         exec(solutionBody,
              env(str(segment(N -Int 1, next(S1))),
                  str(segment(M -Int 1, next(S2)))),
              solutionBody))
    requires N >Int 0 andBool M >Int 0
    [priority(40)]
endmodule
