requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTIC
  imports K-EQUAL

  // A named, immutable copy of the actual translated solution.  Keeping this
  // in constructor form makes the proof exercise the same AST that krun does.
  syntax Pgm ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      FuncDef("correct_bracketing", Params("brackets"),
        Assign(Name("count"), Int(0))
        For(Name("bracket"), Name("brackets"),
          If(Compare(Name("bracket"), CmpOp("==", Str("("))),
            Assign(Name("count"),
              BinOp("+", Name("count"), Int(1))),
            If(Compare(Name("count"), CmpOp("==", Int(0))),
              Return(Bool(false)),
              .Stmts)
            Assign(Name("count"),
              BinOp("-", Name("count"), Int(1)))))
        Return(Compare(Name("count"), CmpOp("==", Int(0))))))

  // Declarative reference checker.  N is the number of unmatched opening
  // brackets before S.  An empty suffix is accepted exactly at depth zero;
  // '(' increases the depth; every other character is treated as ')' by the
  // implementation.  On the prompt's stated domain { '(', ')' }, this is
  // precisely the usual prefix-nonnegative/final-depth-zero specification.
  syntax Bool ::= "bracketSpec" "(" Int "," String ")" [function, total]

  rule bracketSpec(N, "") => N ==Int 0 [simplification]
  rule bracketSpec(N, S)
    => bracketSpec(N +Int 1, substrString(S, 1, lengthString(S)))
    requires notBool (S ==String "")
     andBool substrString(S, 0, 1) ==String "(" [simplification]
  rule bracketSpec(0, S) => false
    requires notBool (S ==String "")
     andBool notBool (substrString(S, 0, 1) ==String "(") [simplification]
  rule bracketSpec(N, S)
    => bracketSpec(N -Int 1, substrString(S, 1, lengthString(S)))
    requires notBool (S ==String "")
     andBool notBool (substrString(S, 0, 1) ==String "(")
     andBool N >Int 0 [simplification]
endmodule
