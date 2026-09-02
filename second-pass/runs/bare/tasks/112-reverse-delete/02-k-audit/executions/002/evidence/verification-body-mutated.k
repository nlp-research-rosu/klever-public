requires "semantic.k"

module VERIFICATION-BODY-MUTATED
  imports SEMANTIC

  syntax Pgm ::= "mutatedSolutionPgm" [function]
  rule mutatedSolutionPgm =>
    Module(
      FuncDef("reverse_delete", Params("s", "c"),
        // Deliberate body mutation: the submitted program initializes with "".
        Assign(Name("result"), Str("X"))
        For(Name("ch"), Name("s"),
          If(Compare(Name("ch"), CmpOp("not in", Name("c"))),
            Assign(Name("result"), BinOp("+", Name("result"), Name("ch"))),
            .Stmts))
        Return(
          TupleExpr(
            Name("result"),
            Compare(
              Name("result"),
              CmpOp(
                "==",
                Subscript(
                  Name("result"),
                  Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))))

  syntax Val ::= expectedMutatedResult(String, String) [function]
  rule expectedMutatedResult(S, C)
    => tupleVal(
         strVal(deleteChars(S, C)),
         boolVal(deleteChars(S, C)
                 ==String reverseString(deleteChars(S, C))))
endmodule
