requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Mathematical reference model, defined independently of the program AST.
  syntax Int ::= absNum(Int) [function, total]
               | evenDigits(Int) [function, total]
               | oddDigits(Int) [function, total]
               | evenFrom(Int, Int) [function, total]
               | oddFrom(Int, Int) [function, total]
  syntax Val ::= expected(Int) [function, total]

  rule absNum(N) => 0 -Int N requires N <Int 0
  rule absNum(N) => N requires N >=Int 0

  rule evenFrom(E, N) => E requires N <=Int 0
  rule evenFrom(E, N) => evenFrom(E +Int 1, N /Int 10)
    requires N >Int 0 andBool N %Int 2 ==Int 0
  rule evenFrom(E, N) => evenFrom(E, N /Int 10)
    requires N >Int 0 andBool N %Int 2 =/=Int 0

  rule oddFrom(O, N) => O requires N <=Int 0
  rule oddFrom(O, N) => oddFrom(O, N /Int 10)
    requires N >Int 0 andBool N %Int 2 ==Int 0
  rule oddFrom(O, N) => oddFrom(O +Int 1, N /Int 10)
    requires N >Int 0 andBool N %Int 2 =/=Int 0

  rule evenDigits(N) => evenFrom(0, N)
  rule oddDigits(N) => oddFrom(0, N)

  rule expected(N) => pairVal(
                          intVal(evenDigits(absNum(N))),
                          intVal(oddDigits(absNum(N))))

  // Names for exact subtrees occurring in solution.mpy.  They are functions,
  // so the proof expands them to the same constructors consumed by SEMANTIC.
  syntax Expr ::= numPositive() [function, total]
                | numNegative() [function, total]
                | digitIsEven() [function, total]
                | returnedCounts() [function, total]
  syntax Stmts ::= digitBody() [function, total]
                 | functionBody() [function, total]
                 | returnCounts() [function, total]
  syntax Pgm ::= solutionProgram() [function, total]

  rule numPositive() => Compare(Name("num"), CmpOp(">", Int(0)))
  rule numNegative() => Compare(Name("num"), CmpOp("<", Int(0)))
  rule digitIsEven() => Compare(
                          BinOp("%", Name("num"), Int(2)),
                          CmpOp("==", Int(0)))
  rule returnedCounts() => TupleExpr(Name("even"), Name("odd"))

  rule digitBody() =>
    If(digitIsEven(),
      AugAssign(Name("even"), "+", Int(1)),
      AugAssign(Name("odd"), "+", Int(1)))
    Assign(Name("num"), BinOp("//", Name("num"), Int(10)))

  rule returnCounts() => Return(returnedCounts())

  rule functionBody() =>
    If(numNegative(),
      Assign(Name("num"), UnaryOp("-", Name("num"))),
      .Stmts)
    Assign(Name("even"), Int(0))
    Assign(Name("odd"), Int(0))
    While(numPositive(), digitBody())
    Return(TupleExpr(Name("odd"), Name("even")))

  rule solutionProgram() =>
    Module(FuncDef("even_odd_count", Params("num"), functionBody()))
endmodule
