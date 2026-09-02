module MODP-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "Call" "(" Expr "," Expr "," Expr "," Expr ")"

  syntax Params ::= "Params" "(" String "," String ")"

  syntax Stmt ::= "Return" "(" Expr ")"
                | "FuncDef" "(" String "," Params "," Stmt ")"

  syntax Program ::= "Module" "(" Stmt ")"
endmodule

module MODP-SEMANTIC
  imports MODP-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  syntax Formals ::= "noFormals" | formals(String, String)
  syntax Result ::= "noResult" | result(Int)

  configuration
    <modp>
      <k> $PGM:Program </k>
      <n> $N:Int </n>
      <p> $P:Int </p>
      <formals> noFormals </formals>
      <result> noResult </result>
    </modp>

  syntax Int ::= evalInt(Expr, String, String, Int, Int) [function]

  rule evalInt(Int(I), _X, _Y, _N, _P) => I
  rule evalInt(Name(X), X, _Y, N, _P) => N
  rule evalInt(Name(Y), X, Y, _N, P) => P
    requires X =/=String Y
  rule evalInt(Call(Name("pow"), BASE, EXP, MOD), X, Y, N, P)
    => evalInt(BASE, X, Y, N, P)
       ^%Int evalInt(EXP, X, Y, N, P)
             evalInt(MOD, X, Y, N, P)

  rule <k> Module(FuncDef(_F, Params(X, Y), BODY)) => BODY </k>
       <formals> noFormals => formals(X, Y) </formals>

  rule <k> Return(E) => .K </k>
       <n> N </n>
       <p> P </p>
       <formals> formals(X, Y) </formals>
       <result> noResult => result(evalInt(E, X, Y, N, P)) </result>
endmodule
