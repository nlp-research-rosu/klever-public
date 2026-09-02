module MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," "Params" "(" Ids ")" "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "Return" "(" Expr ")"

  syntax Ids ::= List{String, ","}
  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX

  syntax Val ::= intVal(Int) | boolVal(Bool)

  syntax KItem ::= exec(Stmts)
                 | eval(Expr)
                 | store(String)
                 | binLeft(String, Expr)
                 | binApply(String, Int)
                 | cmpLeft(String, Expr)
                 | cmpApply(String, Int)
                 | branch(Stmts, Stmts, Stmts)
                 | whileBranch(Expr, Stmts, Stmts)
                 | "doReturn"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <env> .Map </env>
      <n> $N:Int </n>
      <x> $X:Int </x>
      <y> $Y:Int </y>
      <result> .K </result>
    </mpy>

  rule <k> Module(FuncDef("x_or_y", Params("n", "x", "y"), BODY))
            => exec(BODY) ...</k>
       <env> .Map =>
         ("n" |-> intVal(N))
         ("x" |-> intVal(X))
         ("y" |-> intVal(Y))
       </env>
       <n> N </n>
       <x> X </x>
       <y> Y </y>

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => S ~> exec(SS)

  rule If(COND, THEN, ELSE) => eval(COND) ~> branch(THEN, ELSE, .Stmts)
  rule While(COND, BODY) => eval(COND) ~> whileBranch(COND, BODY, .Stmts)
  rule Assign(Name(A), E) => eval(E) ~> store(A)
  rule Return(E) => eval(E) ~> doReturn

  rule boolVal(true) ~> branch(THEN, _ELSE, REST)
    => exec(THEN) ~> exec(REST)
  rule boolVal(false) ~> branch(_THEN, ELSE, REST)
    => exec(ELSE) ~> exec(REST)

  rule boolVal(true) ~> whileBranch(COND, BODY, REST)
    => exec(BODY) ~> eval(COND) ~> whileBranch(COND, BODY, REST)
  rule boolVal(false) ~> whileBranch(_COND, _BODY, REST)
    => exec(REST)

  rule <k> V:Val ~> store(A) => .K ...</k>
       <env> ENV => ENV [ A <- V ] </env>

  rule <k> V:Val ~> doReturn ~> _REST => .K </k>
       <result> .K => V </result>

  rule eval(Int(I)) => intVal(I)
  rule <k> eval(Name(A)) => V ...</k>
       <env>... A |-> V ...</env>

  rule eval(BinOp(OP, LEFT, RIGHT))
    => eval(LEFT) ~> binLeft(OP, RIGHT)
  rule intVal(I) ~> binLeft(OP, RIGHT)
    => eval(RIGHT) ~> binApply(OP, I)
  rule intVal(J) ~> binApply("+", I) => intVal(I +Int J)
  rule intVal(J) ~> binApply("*", I) => intVal(I *Int J)
  rule intVal(J) ~> binApply("%", I) => intVal(I %Int J)
    requires J =/=Int 0

  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)))
    => eval(LEFT) ~> cmpLeft(OP, RIGHT)
  rule intVal(I) ~> cmpLeft(OP, RIGHT)
    => eval(RIGHT) ~> cmpApply(OP, I)
  rule intVal(J) ~> cmpApply("<", I) => boolVal(I <Int J)
  rule intVal(J) ~> cmpApply("<=", I) => boolVal(I <=Int J)
  rule intVal(J) ~> cmpApply("==", I) => boolVal(I ==Int J)
endmodule
