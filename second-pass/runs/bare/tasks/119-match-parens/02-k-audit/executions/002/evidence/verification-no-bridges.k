requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTICS

  syntax Pgm ::= "solutionProgram"

  // Independent mathematical contract used by spec.k.
  syntax Bool ::= "balanced" "(" PString "," Int ")" [function]
  syntax PyString ::= "contractAnswer" "(" PString "," PString ")" [function]

  rule balanced(_, D) => false requires D <Int 0
  rule balanced(.PString, D) => D ==Int 0 requires D >=Int 0
  rule balanced(lp S, D) => balanced(S, D +Int 1) requires D >=Int 0
  rule balanced(rp S, D) => balanced(S, D -Int 1) requires D >=Int 0

  rule contractAnswer(A, B) => yesString
    requires balanced(pconcat(A, B), 0)
      orBool balanced(pconcat(B, A), 0)
  rule contractAnswer(_A, _B) => noString [owise]

  // This is the exact constructor tree generated in solution.mpy.  prove.sh
  // regenerates solution.mpy and checks it byte-for-byte before proving.
  rule solutionProgram =>
    Module(
      FuncDef("is_balanced", Params("s", "depth"),
        If(Compare(Name("depth"), CmpOp("<", Int(0))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Name("s"), CmpOp("==", Str(""))),
          Return(Compare(Name("depth"), CmpOp("==", Int(0)))),
          .Stmts)
        If(Compare(Subscript(Name("s"), Int(0)), CmpOp("==", Str("("))),
          Return(
            Call(
              Name("is_balanced"),
              Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
              BinOp("+", Name("depth"), Int(1)))),
          .Stmts)
        Return(
          Call(
            Name("is_balanced"),
            Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
            BinOp("-", Name("depth"), Int(1)))))
      FuncDef("match_parens", Params("lst"),
        If(Call(
          Name("is_balanced"),
          BinOp(
            "+",
            Subscript(Name("lst"), Int(0)),
            Subscript(Name("lst"), Int(1))),
          Int(0)),
          Return(Str("Yes")),
          .Stmts)
        If(Call(
          Name("is_balanced"),
          BinOp(
            "+",
            Subscript(Name("lst"), Int(1)),
            Subscript(Name("lst"), Int(0))),
          Int(0)),
          Return(Str("Yes")),
          .Stmts)
        Return(Str("No"))))
endmodule

module VERIFICATION
  imports MPY-VERIFICATION
endmodule
