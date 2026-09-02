requires "reference-semantics/semantics.k"

module SIMPLE-POWER-VERIFICATION
  imports MPY

  // A total characterization over K integers.  On the meaningful power
  // domain X >= 1 and N >= 2, exact division removes one factor of N.
  syntax Bool ::= simplePower(Int, Int) [function]
                | positivePowerLoop(Int, Int) [function]

  rule simplePower(X, _N) => true
    requires X ==Int 1
  rule simplePower(X, _N) => false
    requires X <Int 1
  rule simplePower(X, N) => false
    requires X >Int 1 andBool N <=Int 1
  rule simplePower(X, N) => positivePowerLoop(X, N)
    requires X >Int 1 andBool N >Int 1

  rule positivePowerLoop(X, N) => positivePowerLoop(X /Int N, N)
    requires pyMod(X, N) ==Int 0
  rule positivePowerLoop(X, N) => X ==Int 1
    requires pyMod(X, N) =/=Int 0

  // Named pieces of the generated AST keep the claims readable.  Their
  // expansions are exactly the constructors in solution.mpy.
  syntax Expr ::= "powerCondition" [macro]
  rule powerCondition
    => Compare(BinOp("%", Name("x"), Name("n")), CmpOp("==", Int(0)))

  syntax Stmts ::= "powerLoopBody" [macro]
  rule powerLoopBody
    => Assign(Name("x"), Int(1))

  syntax Expr ::= "powerResult" [macro]
  rule powerResult
    => Compare(Name("x"), CmpOp("==", Int(1)))

  syntax Stmt ::= "powerLoop" [macro]
  rule powerLoop => While(powerCondition, powerLoopBody)

  syntax Stmts ::= "powerBody" [macro]
  rule powerBody
    => If(Compare(Name("x"), CmpOp("==", Int(1))),
          Return(Bool(true)), .Stmts)
       If(Compare(Name("x"), CmpOp("<", Int(1))),
          Return(Bool(false)), .Stmts)
       If(Compare(Name("n"), CmpOp("<=", Int(1))),
          Return(Bool(false)), .Stmts)
       powerLoop
       Return(powerResult)

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule
    => Module(FuncDef("is_simple_power", Params("x", "n"), powerBody))
endmodule
