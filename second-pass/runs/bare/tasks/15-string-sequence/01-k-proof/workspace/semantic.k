requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Call" "(" Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP
  imports LIST

  syntax Val ::= IVal(Int) | SVal(String) | BVal(Bool)
  syntax Function ::= function(String, Stmts)
  syntax Frame ::= frame(Map, K)

  syntax KItem ::= init(Module, Int)
                 | run(Stmts)
                 | exec(Stmt)
                 | eval(Expr)
                 | store(String)
                 | binLeft(String, Expr)
                 | binRight(String, Val)
                 | cmpLeft(String, Expr)
                 | cmpRight(String, Val)
                 | ifGuard(Stmts, Stmts)
                 | whileGuard(Expr, Stmts)
                 | call(String)
                 | toStr()
                 | returning()
                 | functionEnd()

  configuration
    <mpy>
      <k> init($PGM:Module, $ARG:Int) </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <stack> .List </stack>
    </mpy>

  rule <k> init(Module(SS), N)
         => run(SS)
         ~> eval(Call(Name("string_sequence"), Int(N))) ... </k>

  rule run(.Stmts) => .K
  rule run(S SS) => exec(S) ~> run(SS)

  rule <k> exec(FuncDef(F, Params(P), BODY)) => .K ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>

  rule <k> exec(Assign(Name(X), E)) => eval(E) ~> store(X) ... </k>
  rule <k> V:Val ~> store(X) => .K ... </k>
       <env> ... X |-> (_ => V) ... </env>
  rule <k> V:Val ~> store(X) => .K ... </k>
       <env> ENV => X |-> V ENV </env>
       requires notBool (X in_keys(ENV))

  rule <k> exec(While(COND, BODY))
         => eval(COND) ~> whileGuard(COND, BODY) ... </k>
  rule BVal(true) ~> whileGuard(COND, BODY)
       => run(BODY) ~> exec(While(COND, BODY))
  rule BVal(false) ~> whileGuard(_, _) => .K

  rule <k> exec(If(COND, THEN, ELSE))
         => eval(COND) ~> ifGuard(THEN, ELSE) ... </k>
  rule BVal(true) ~> ifGuard(THEN, _) => run(THEN)
  rule BVal(false) ~> ifGuard(_, ELSE) => run(ELSE)

  rule <k> exec(Return(E)) => eval(E) ~> returning() ... </k>
  rule <k> V:Val ~> returning() ~> _REST:K => V ~> KREST </k>
       <env> _ => CALLER </env>
       <stack> ListItem(frame(CALLER, KREST)) STACK => STACK </stack>

  rule eval(Int(I)) => IVal(I)
  rule eval(Str(S)) => SVal(S)
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>

  rule eval(BinOp(OP, E1, E2)) => eval(E1) ~> binLeft(OP, E2)
  rule V:Val ~> binLeft(OP, E2) => eval(E2) ~> binRight(OP, V)
  rule IVal(I2) ~> binRight("+", IVal(I1)) => IVal(I1 +Int I2)
  rule SVal(S2) ~> binRight("+", SVal(S1)) => SVal(S1 +String S2)

  rule eval(Compare(E1, CmpOp(OP, E2)))
       => eval(E1) ~> cmpLeft(OP, E2)
  rule V:Val ~> cmpLeft("<=", E2) => eval(E2) ~> cmpRight("<=", V)
  rule IVal(I2) ~> cmpRight("<=", IVal(I1)) => BVal(I1 <=Int I2)
  rule V:Val ~> cmpLeft("<", E2) => eval(E2) ~> cmpRight("<", V)
  rule IVal(I2) ~> cmpRight("<", IVal(I1)) => BVal(I1 <Int I2)

  rule eval(Call(Name("str"), E)) => eval(E) ~> toStr()
  rule IVal(I) ~> toStr() => SVal(Int2String(I))

  rule <k> eval(Call(Name(F), E)) => eval(E) ~> call(F) ... </k>
       <functions> ... F |-> function(_, _) ... </functions>
       requires F =/=String "str"
  rule <k> V:Val ~> call(F) ~> KREST
         => run(BODY) ~> functionEnd() </k>
       <env> CALLER => P |-> V </env>
       <functions> ... F |-> function(P, BODY) ... </functions>
       <stack> STACK => ListItem(frame(CALLER, KREST)) STACK </stack>
endmodule
