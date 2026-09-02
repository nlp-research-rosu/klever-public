module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Exprs ::= List{Expr, ","}

  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  syntax Value ::= "intVal" "(" Int ")"
                 | "boolVal" "(" Bool ")"
                 | "listVal" "(" List ")"

  syntax Result ::= "noResult" | "done" "(" Value ")"

  configuration
    <py>
      <k> $PGM:Program </k>
      <input> $INPUT:Int </input>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "store" "(" String ")"
                 | "singleton"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "cmpLeft" "(" String "," Expr ")"
                 | "cmpRight" "(" String "," Value ")"
                 | "ifBranch" "(" Stmts "," Stmts ")"
                 | "whileBranch" "(" Expr "," Stmts ")"
                 | "doReturn"

  rule <k> Module(FuncDef(_F, Params(P:String), BODY)) => exec(BODY) </k>
       <input> N </input>
       <env> .Map => P |-> intVal(N) </env>

  rule exec(.Stmts) => .K
  rule exec(S:Stmt REST:Stmts) => S ~> exec(REST)

  rule Assign(Name(X), E) => eval(E) ~> store(X)
  rule <k> V:Value ~> store(X) => .K ...</k>
       <env> ENV => ENV [ X <- V ] </env>

  rule If(COND, THEN, ELSE) => eval(COND) ~> ifBranch(THEN, ELSE)
  rule boolVal(true) ~> ifBranch(THEN, _ELSE) => exec(THEN)
  rule boolVal(false) ~> ifBranch(_THEN, ELSE) => exec(ELSE)

  rule While(COND, BODY) => eval(COND) ~> whileBranch(COND, BODY)
  rule boolVal(true) ~> whileBranch(COND, BODY)
    => exec(BODY) ~> While(COND, BODY)
  rule boolVal(false) ~> whileBranch(_COND, _BODY) => .K

  rule Return(E) => eval(E) ~> doReturn
  rule <k> V:Value ~> doReturn ~> _REST:K => .K </k>
       <result> noResult => done(V) </result>

  rule <k> eval(Int(I)) => intVal(I) ...</k>
  rule <k> eval(Name(X)) => V ...</k>
       <env>... X |-> V:Value ...</env>

  rule eval(ListExpr(.Exprs)) => listVal(.List)
  rule eval(ListExpr(E)) => eval(E) ~> singleton
  rule intVal(I) ~> singleton => listVal(ListItem(I))

  rule eval(BinOp(OP, LEFT, RIGHT)) => eval(LEFT) ~> binLeft(OP, RIGHT)
  rule V:Value ~> binLeft(OP, RIGHT) => eval(RIGHT) ~> binRight(OP, V)
  rule intVal(J) ~> binRight("+", intVal(I)) => intVal(I +Int J)
  rule intVal(J) ~> binRight("*", intVal(I)) => intVal(I *Int J)
  rule intVal(J) ~> binRight("%", intVal(I)) => intVal(I %Int J)
  rule listVal(L2) ~> binRight("+", listVal(L1)) => listVal(L1 L2)

  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)))
    => eval(LEFT) ~> cmpLeft(OP, RIGHT)
  rule V:Value ~> cmpLeft(OP, RIGHT) => eval(RIGHT) ~> cmpRight(OP, V)
  rule intVal(J) ~> cmpRight("<=", intVal(I)) => boolVal(I <=Int J)
  rule intVal(J) ~> cmpRight("==", intVal(I)) => boolVal(I ==Int J)
endmodule
