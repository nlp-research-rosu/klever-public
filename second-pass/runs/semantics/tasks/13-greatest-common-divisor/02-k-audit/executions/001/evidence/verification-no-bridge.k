requires "reference-semantics/semantics.k"

module GCD-VERIFICATION-NO-BRIDGE
  imports MPY

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

  syntax Int ::= gcdSpec(Int, Int)
    [function, symbol(gcdSpec), no-evaluators]
  rule gcdSpec(A:Int, 0) => A
    requires A >=Int 0
    [concrete]
  rule gcdSpec(A:Int, B:Int) => gcdSpec(B, pyMod(A, B))
    requires A >=Int 0 andBool B >Int 0
    [concrete]
endmodule
