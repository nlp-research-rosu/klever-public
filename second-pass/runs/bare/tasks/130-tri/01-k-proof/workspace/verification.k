requires "semantic.k"

module TRI-VERIFICATION
  imports TRI-SEMANTIC

  // This macro is the exact constructor tree emitted in solution.mpy.
  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("tri", Params("n"),
        If(Compare(Name("n"), CmpOp("==", Int(0))),
          Return(ListExpr(Int(1))),
          .Stmts)
        If(Compare(BinOp("%", Name("n"), Int(2)),
                   CmpOp("==", Int(0))),
          Return(
            BinOp("+",
              Call(Name("tri"), BinOp("-", Name("n"), Int(1))),
              ListExpr(BinOp("+", Int(1),
                             BinOp("//", Name("n"), Int(2)))))),
          .Stmts)
        Return(
          BinOp("+",
            Call(Name("tri"), BinOp("-", Name("n"), Int(1))),
            ListExpr(
              BinOp("*",
                BinOp("//", BinOp("+", Name("n"), Int(1)), Int(2)),
                BinOp("//", BinOp("+", Name("n"), Int(5)), Int(2))))))))

  // Mathematical sequence value.  The odd clause is the closed form of the
  // prompt's recurrence; the two rules are exhaustive for N >= 0.
  syntax Int ::= triValue ( Int ) [function]
  rule triValue(N) => 1 +Int (N /Int 2)
    requires N >=Int 0 andBool N %Int 2 ==Int 0
  rule triValue(N) => ((N +Int 1) /Int 2) *Int ((N +Int 5) /Int 2)
    requires N >=Int 0 andBool N %Int 2 =/=Int 0

  syntax IntSeq ::= triPrefix ( Int ) [function]
  rule triPrefix(0) => cons(1, nil)
  rule triPrefix(N) => append(triPrefix(N -Int 1), cons(triValue(N), nil))
    requires N >Int 0

endmodule
