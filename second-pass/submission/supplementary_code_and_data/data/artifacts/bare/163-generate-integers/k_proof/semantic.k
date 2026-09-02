requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= Module(Stmts)

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= FuncDef(String, Params, Stmts)
                | Assign(Expr, Expr)
                | If(Expr, Stmts, Stmts)
                | Return(Expr)

  syntax Params ::= Params(Strings)
  syntax Strings ::= List{String, ","}

  syntax Expr ::= Name(String)
                | Int(Int)
                | ListExpr(Exprs)
                | Compare(Expr, CmpOps)
                | BinOp(String, Expr, Expr)
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= CmpOp(String, Expr)
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports LIST
  imports MAP

  syntax Input ::= pair(Int, Int)
  syntax Value ::= intVal(Int) | boolVal(Bool) | listVal(List)
  syntax Result ::= "noResult" | Value

  syntax KItem ::= exec(Stmts)
                 | execStmt(Stmt)
                 | eval(Expr)
                 | assignTo(String)
                 | binRight(String, Value)
                 | cmpLeft(String, Expr)
                 | cmpRight(String, Value)
                 | choose(Stmts, Stmts)
                 | "returnValue"

  configuration
    <py>
      <k> $PGM:Program </k>
      <input> pair($A:Int, $B:Int) </input>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  rule <k> Module(FuncDef("generate_integers", Params("a", "b"), BODY))
        => exec(BODY) ... </k>
       <input> pair(A, B) </input>
       <env> .Map => ("a" |-> intVal(A)) ("b" |-> intVal(B)) </env>

  rule exec(.Stmts) => .K
  rule exec((S:Stmt REST:Stmts)) => execStmt(S) ~> exec(REST)

  rule execStmt(Assign(Name(X), E)) => eval(E) ~> assignTo(X)
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule execStmt(If(COND, THEN, ELSE))
    => eval(COND) ~> choose(THEN, ELSE)
  rule boolVal(true) ~> choose(THEN, _) => exec(THEN)
  rule boolVal(false) ~> choose(_, ELSE) => exec(ELSE)

  rule execStmt(Return(E)) => eval(E) ~> returnValue
  rule <k> V:Value ~> returnValue => .K ... </k>
       <result> _ => V </result>

  rule eval(Int(I)) => intVal(I)
  rule <k> eval(Name(X)) => V ... </k>
       <env>... X |-> V ...</env>
  rule eval(ListExpr(.Exprs)) => listVal(.List)
  rule eval(ListExpr(Int(I))) => listVal(ListItem(I))

  rule eval(BinOp(OP, LEFT, RIGHT))
    => eval(LEFT) ~> binRight(OP, evalPlaceholder(RIGHT))

  syntax Value ::= evalPlaceholder(Expr)
  rule V:Value ~> binRight(OP, evalPlaceholder(RIGHT))
    => eval(RIGHT) ~> binRight(OP, V)
  rule listVal(RIGHT) ~> binRight("+", listVal(LEFT))
    => listVal(LEFT RIGHT)

  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)))
    => eval(LEFT) ~> cmpLeft(OP, RIGHT)
  rule V:Value ~> cmpLeft(OP, RIGHT)
    => eval(RIGHT) ~> cmpRight(OP, V)
  rule intVal(RIGHT) ~> cmpRight("<=", intVal(LEFT))
    => boolVal(true)
    requires LEFT <=Int RIGHT
  rule intVal(RIGHT) ~> cmpRight("<=", intVal(LEFT))
    => boolVal(false)
    requires notBool (LEFT <=Int RIGHT)
endmodule
