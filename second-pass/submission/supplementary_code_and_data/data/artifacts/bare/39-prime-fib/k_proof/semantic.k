requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Value ::= Int | Bool
  syntax Result ::= "noResult" | Value

  syntax KItem ::= exec(Stmts)
                 | eval(Expr)
                 | assignTo(String)
                 | binLeft(String, Expr)
                 | binRight(String, Int)
                 | cmpLeft(String, Expr)
                 | cmpRight(String, Int)
                 | ifDecision(Stmts, Stmts)
                 | whileLoop(Expr, Stmts)
                 | whileDecision(Expr, Stmts)
                 | "returnValue"

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <env> .Map </env>
      <n> $N:Int </n>
      <result> noResult </result>
    </mpy>

  // A translated module in this task contains one top-level, one-argument
  // function.  The configuration supplies that argument and starts its body.
  rule <k> Module(FuncDef(_F, Params(P:String), BODY)) => exec(BODY) </k>
       <env> .Map => P |-> N </env>
       <n> N </n>

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => S ~> exec(SS)

  rule Assign(Name(X), E) => eval(E) ~> assignTo(X)
  rule <k> V:Value ~> assignTo(X) => .K ...</k>
       <env> ENV => ENV [ X <- V ] </env>

  rule If(COND, THEN, ELSE) => eval(COND) ~> ifDecision(THEN, ELSE)
  rule true  ~> ifDecision(THEN, _ELSE) => exec(THEN)
  rule false ~> ifDecision(_THEN, ELSE) => exec(ELSE)

  rule While(COND, BODY) => whileLoop(COND, BODY)
  rule whileLoop(COND, BODY) => eval(COND) ~> whileDecision(COND, BODY)
  rule true  ~> whileDecision(COND, BODY) => exec(BODY) ~> whileLoop(COND, BODY)
  rule false ~> whileDecision(_COND, _BODY) => .K

  rule Return(E) => eval(E) ~> returnValue
  rule <k> V:Value ~> returnValue ~> _REST => .K </k>
       <result> _ => V </result>

  rule eval(Int(I)) => I
  rule eval(Bool(B)) => B
  rule <k> eval(Name(X)) => V ...</k>
       <env> ... X |-> V:Value ...</env>

  rule eval(BinOp(OP, LEFT, RIGHT)) => eval(LEFT) ~> binLeft(OP, RIGHT)
  rule I:Int ~> binLeft(OP, RIGHT) => eval(RIGHT) ~> binRight(OP, I)
  rule J:Int ~> binRight("+", I) => I +Int J
  rule J:Int ~> binRight("*", I) => I *Int J
  rule J:Int ~> binRight("%", I) => I %Int J

  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)))
    => eval(LEFT) ~> cmpLeft(OP, RIGHT)
  rule I:Int ~> cmpLeft(OP, RIGHT) => eval(RIGHT) ~> cmpRight(OP, I)
  rule J:Int ~> cmpRight("<",  I) => I <Int  J
  rule J:Int ~> cmpRight("<=", I) => I <=Int J
  rule J:Int ~> cmpRight("==", I) => I ==Int J
endmodule
