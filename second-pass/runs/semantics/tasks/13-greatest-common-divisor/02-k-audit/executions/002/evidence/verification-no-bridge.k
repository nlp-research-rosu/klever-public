requires "reference-semantics/semantics.k"

module GCD-VERIFICATION
  imports MPY

  // These macros are the exact constructor tree emitted in solution.mpy.
  // Keeping the tree here lets kprove reason about the submitted program,
  // while the shell check in prove.sh prevents the two copies from drifting.
  syntax Stmt ::= "GcdDef" [macro]
  syntax Stmts ::= "GcdBody" [macro]
  syntax Expr ::= "GcdCondition" [macro]
  syntax Stmts ::= "GcdLoopBody" [macro]

  rule GcdDef =>
    FuncDef("greatest_common_divisor", Params("a", "b"), GcdBody)

  rule GcdCondition =>
    Compare(Name("b"), CmpOp("!=", Int(0)))

  rule GcdLoopBody =>
    Assign(TupleExpr((Name("a"), Name("b"), .Exprs)),
           TupleExpr((Name("b"),
                      BinOp("%", Name("a"), Name("b")), .Exprs)))
    .Stmts

  rule GcdBody =>
    Assign(Name("a"), Call(Name("abs"), (Name("a"), .Exprs)))
    Assign(Name("b"), Call(Name("abs"), (Name("b"), .Exprs)))
    While(GcdCondition, GcdLoopBody)
    Return(Name("a"))
    .Stmts

  syntax Val ::= "GcdClosure" [macro]
  rule GcdClosure =>
    closureVal(("a", "b", .ParamNames), GcdBody, 0)

  // Mathematical gcd, characterized by Euclid's recurrence.  It stays opaque
  // to the backend so symbolic terms do not expand forever.
  syntax Int ::= gcdSpec(Int, Int)
    [function, symbol(gcdSpec), no-evaluators]
  rule gcdSpec(A:Int, 0) => A
    requires A >=Int 0
    [concrete]
  rule gcdSpec(A:Int, B:Int) => gcdSpec(B, pyMod(A, B))
    requires A >=Int 0 andBool B >Int 0
    [concrete]

endmodule
