requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTICS
  imports K-EQUAL

  // A closed K representation of the AST emitted in solution.mpy.  The
  // execution claims use this term, while prove.sh separately regenerates and
  // executes solution.mpy through the parser.
  syntax Pgm ::= "solutionProgram" [function]
  syntax Stmts ::= "solutionDefs" [function]

  rule solutionProgram => Module(solutionDefs)
  rule solutionDefs
    => FuncDef(
         "order_by_points", Params("nums"),
         Return(
           Call(
             Name("sorted"),
             Name("nums"),
             KwArg(
               "key",
               Lambda(
                 Params("n"), CellVars(.Ids), FreeVars(.Ids),
                 BinOp(
                   "-",
                   Call(
                     Name("sum"),
                     Call(
                       Name("map"), Name("int"),
                       Call(Name("str"), Call(Name("abs"), Name("n"))))),
                   IfExp(
                     Compare(Name("n"), CmpOp("<", Int(0))),
                     BinOp(
                       "*", Int(2),
                       Call(
                         Name("int"),
                         Subscript(
                           Call(
                             Name("str"), Call(Name("abs"), Name("n"))),
                           Int(0)))),
                     Int(0))))))))

  // Independent, declarative reference sort.  Inserting the head before an
  // equal-score element makes this stable with respect to original position.
  syntax Vals ::= specSort(Vals) [function]
                | specInsert(Val, Vals) [function]

  rule specSort(.Vals) => .Vals
  rule specSort((IntVal(N), VS))
    => specInsert(IntVal(N), specSort(VS))

  rule specInsert(V, .Vals) => V
  rule specInsert(IntVal(N), (IntVal(M), VS))
    => IntVal(N), IntVal(M), VS
    requires pointScore(N) <=Int pointScore(M)
  rule specInsert(IntVal(N), (IntVal(M), VS))
    => IntVal(M), specInsert(IntVal(N), VS)
    requires pointScore(N) >Int pointScore(M)

  syntax Bool ::= isOrdered(Vals) [function]
  rule isOrdered(.Vals) => true
  rule isOrdered(IntVal(_)) => true
  rule isOrdered((IntVal(N), IntVal(M), VS)) => isOrdered((IntVal(M), VS))
    requires pointScore(N) <=Int pointScore(M)
  rule isOrdered((IntVal(N), IntVal(M), _)) => false
    requires pointScore(N) >Int pointScore(M)
endmodule
