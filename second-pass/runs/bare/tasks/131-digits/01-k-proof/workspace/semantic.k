requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program
  syntax Params
  syntax Stmt
  syntax Stmts ::= List{Stmt, ""}
  syntax Expr
  syntax CmpOp

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Params ::= "Params" "(" String ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax KItem ::= "Invoke" "(" Program "," String "," Int ")"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT

  configuration
    <mpy>
      <k> $PGM:K </k>
      <n> 0 </n>
      <acc> 0 </acc>
      <digit> 0 </digit>
      <answer> .K </answer>
    </mpy>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"
                 | "eval" "(" Expr ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Int ")"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareRight" "(" String "," Int ")"
                 | "write" "(" String ")"
                 | "ifCont" "(" Stmts "," Stmts ")"
                 | "loop" "(" Expr "," Stmts ")"
                 | "loopCont" "(" Expr "," Stmts ")"
                 | "doReturn"

  rule <k> Invoke(Module(FuncDef(F, Params("n"), BODY)), F, N)
            => exec(BODY) ... </k>
       <n> _ => N </n>
       <acc> _ => 0 </acc>
       <digit> _ => 0 </digit>
       <answer> _ => .K </answer>

  rule exec(.Stmts) => .K
  rule exec(S SS) => execStmt(S) ~> exec(SS)

  rule execStmt(Assign(Name(X), E)) => eval(E) ~> write(X)
  rule execStmt(If(COND, THEN, ELSE))
    => eval(COND) ~> ifCont(THEN, ELSE)
  rule execStmt(While(COND, BODY)) => loop(COND, BODY)
  rule execStmt(Return(E)) => eval(E) ~> doReturn

  rule eval(Int(I)) => I
  rule <k> eval(Name("n")) => I ... </k> <n> I </n>
  rule <k> eval(Name("result")) => I ... </k> <acc> I </acc>
  rule <k> eval(Name("digit")) => I ... </k> <digit> I </digit>
  rule eval(BinOp(OP, LEFT, RIGHT)) => eval(LEFT) ~> binLeft(OP, RIGHT)
  rule I:Int ~> binLeft(OP, RIGHT) => eval(RIGHT) ~> binRight(OP, I)
  rule J:Int ~> binRight("%", I) => I %Int J
  rule J:Int ~> binRight("//", I) => I /Int J
  rule J:Int ~> binRight("*", I) => I *Int J

  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)))
    => eval(LEFT) ~> compareLeft(OP, RIGHT)
  rule I:Int ~> compareLeft(OP, RIGHT)
    => eval(RIGHT) ~> compareRight(OP, I)
  rule J:Int ~> compareRight(">", I) => 1 requires I >Int J
  rule J:Int ~> compareRight(">", I) => 0 requires I <=Int J
  rule J:Int ~> compareRight("==", I) => 1 requires I ==Int J
  rule J:Int ~> compareRight("==", I) => 0 requires I =/=Int J

  rule <k> I:Int ~> write("n") => .K ... </k> <n> _ => I </n>
  rule <k> I:Int ~> write("result") => .K ... </k> <acc> _ => I </acc>
  rule <k> I:Int ~> write("digit") => .K ... </k> <digit> _ => I </digit>

  rule I:Int ~> ifCont(THEN, _ELSE) => exec(THEN)
    requires I =/=Int 0
  rule I:Int ~> ifCont(_THEN, ELSE) => exec(ELSE)
    requires I ==Int 0

  rule loop(COND, BODY) => eval(COND) ~> loopCont(COND, BODY)
  rule I:Int ~> loopCont(COND, BODY)
    => exec(BODY) ~> loop(COND, BODY)
    requires I =/=Int 0
  rule I:Int ~> loopCont(_COND, _BODY) => .K
    requires I ==Int 0

  rule <k> I:Int ~> doReturn ~> _REST => .K </k>
       <answer> _ => I </answer>
endmodule

module SEMANTIC
  imports MPY-SEMANTICS
endmodule
