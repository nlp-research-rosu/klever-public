module MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "ListExpr" "(" Exprs ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Exprs ::= List{Expr, ","}

  syntax Args ::= "args" "(" Int "," Int "," Int ")"
  syntax Result ::= "result" "(" Int "," Int ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports MAP

  syntax PyVal ::= "intVal" "(" Int ")"
                 | "boolVal" "(" Bool ")"
                 | "listVal" "(" PyVals ")"
  syntax PyVals ::= List{PyVal, ","}

  syntax Outcome ::= "normal"
                   | "returned" "(" PyVal ")"

  syntax KItem ::= "run" "(" Pgm "," Args ")"

  // Symbols whose defining equations live in the proof layer.
  syntax Result ::= carrotContract(Int, Int, Int) [function, total]
  syntax Bool ::= validInput(Int, Int, Int) [function, total]
  syntax Pgm ::= "solutionProgram" [function]

  syntax PyVal ::= lookup(String, Map) [function, total]
  rule lookup(X, (X |-> V:PyVal) _REST) => V

  syntax PyVal ::= evalExpr(Expr, Map) [function, total]
  rule evalExpr(Int(I), _) => intVal(I)
  rule evalExpr(Name(X), RHO) => lookup(X, RHO)
  rule evalExpr(BinOp("+", LEFT, RIGHT), RHO)
    => addVals(evalExpr(LEFT, RHO), evalExpr(RIGHT, RHO))
  rule evalExpr(BinOp("-", LEFT, RIGHT), RHO)
    => subVals(evalExpr(LEFT, RHO), evalExpr(RIGHT, RHO))
  rule evalExpr(Compare(LEFT, CmpOp("<=", RIGHT)), RHO)
    => leVals(evalExpr(LEFT, RHO), evalExpr(RIGHT, RHO))
  rule evalExpr(ListExpr(FIRST, SECOND), RHO)
    => listVal(evalExpr(FIRST, RHO), evalExpr(SECOND, RHO))

  syntax PyVal ::= addVals(PyVal, PyVal) [function, total]
                 | subVals(PyVal, PyVal) [function, total]
                 | leVals(PyVal, PyVal) [function, total]
  rule addVals(intVal(A), intVal(B)) => intVal(A +Int B)
  rule subVals(intVal(A), intVal(B)) => intVal(A -Int B)
  rule leVals(intVal(A), intVal(B)) => boolVal(true)
    requires A <=Int B
  rule leVals(intVal(A), intVal(B)) => boolVal(false)
    requires B <Int A

  syntax Outcome ::= evalStmts(Stmts, Map) [function, total]
                   | evalStmt(Stmt, Map) [function, total]
                   | continueWith(Outcome, Stmts, Map) [function, total]
                   | chooseBranch(PyVal, Stmts, Stmts, Map) [function, total]
  rule evalStmts(.Stmts, _) => normal
  rule evalStmts(S:Stmt REST:Stmts, RHO)
    => continueWith(evalStmt(S, RHO), REST, RHO)
  rule continueWith(normal, REST, RHO) => evalStmts(REST, RHO)
  rule continueWith(returned(V), _, _) => returned(V)

  rule evalStmt(Return(E), RHO) => returned(evalExpr(E, RHO))
  rule evalStmt(If(COND, THEN, ELSE), RHO)
    => chooseBranch(evalExpr(COND, RHO), THEN, ELSE, RHO)
  rule chooseBranch(boolVal(true), THEN, _, RHO) => evalStmts(THEN, RHO)
  rule chooseBranch(boolVal(false), _, ELSE, RHO) => evalStmts(ELSE, RHO)

  syntax Result ::= resultOf(Outcome) [function, total]
  rule resultOf(returned(listVal(intVal(A), intVal(B)))) => result(A, B)

  configuration
    <mpy>
      <k> run($PGM:Pgm, $ARGS:Args) </k>
    </mpy>

  rule run(
         Module(FuncDef("eat", Params("number", "need", "remaining"), BODY)),
         args(NUMBER, NEED, REMAINING)
       )
    => resultOf(evalStmts(
         BODY,
         ("number" |-> intVal(NUMBER))
         ("need" |-> intVal(NEED))
         ("remaining" |-> intVal(REMAINING))
       ))
endmodule
