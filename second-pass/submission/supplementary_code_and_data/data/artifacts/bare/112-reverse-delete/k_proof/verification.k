// Contract vocabulary kept separate from the execution semantics.  The
// contract says: retain, in order, exactly the characters of s which do not
// occur in c, and report whether that retained string equals its reversal.

requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A named copy of the transliterated program keeps proof claims readable.
  // prove.sh regenerates solution.mpy and checks its SHA-256 before proof, so
  // this constructor tree is pinned to the submitted translated artifact.
  syntax Pgm ::= "solutionPgm" [function]
  rule solutionPgm =>
    Module(
      FuncDef("reverse_delete", Params("s", "c"),
        Assign(Name("result"), Str(""))
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

  syntax Val ::= expectedResult(String, String) [function]
  rule expectedResult(S, C)
    => tupleVal(
         strVal(deleteChars(S, C)),
         boolVal(deleteChars(S, C)
                 ==String reverseString(deleteChars(S, C))))
endmodule
