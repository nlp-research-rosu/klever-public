module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Call" "(" Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  configuration
    <python>
      <k> $PGM:Program </k>
      <arg> $ARG:Int </arg>
      <env> .Map </env>
      <functions> .Map </functions>
    </python>

  syntax Function ::= "function" "(" String "," Stmts ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "topCall"
                 | "eval" "(" Expr ")"
                 | "evalRight" "(" String "," Expr ")"
                 | "applyBin" "(" String "," Int ")"
                 | "finishCompare" "(" String "," Expr ")"
                 | "applyCompare" "(" String "," Int ")"
                 | "prepareCall" "(" String ")"
                 | "invoke" "(" String "," Int ")"
                 | "functionEnd" "(" Map ")"
                 | "makeReturn"
                 | "returned" "(" Int ")"

  rule <k> Module(SS) => exec(SS) ~> topCall ... </k>

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => S ~> exec(SS)

  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <functions> FS => (F |-> function(P, BODY)) FS </functions>
    requires notBool (F in_keys(FS))

  rule <k> topCall => eval(Call(Name("fib"), Int(N))) ... </k>
       <arg> N </arg>

  rule eval(Int(I)) => I
  rule <k> eval(Name(X)) => I ... </k>
       <env>... X |-> I:Int ...</env>

  rule eval(BinOp(OP, LEFT, RIGHT))
    => eval(LEFT) ~> evalRight(OP, RIGHT)
  rule I:Int ~> evalRight(OP, RIGHT)
    => eval(RIGHT) ~> applyBin(OP, I)
  rule J:Int ~> applyBin("+", I) => I +Int J
  rule J:Int ~> applyBin("-", I) => I -Int J

  rule eval(Compare(LEFT, CmpOp(OP, RIGHT)))
    => eval(LEFT) ~> finishCompare(OP, RIGHT)
  rule I:Int ~> finishCompare(OP, RIGHT)
    => eval(RIGHT) ~> applyCompare(OP, I)
  rule J:Int ~> applyCompare("<=", I) => I <=Int J

  rule true  ~> finishIf(THEN, _ELSE) => exec(THEN)
  rule false ~> finishIf(_THEN, ELSE) => exec(ELSE)
  syntax KItem ::= "finishIf" "(" Stmts "," Stmts ")"
  rule If(TEST, THEN, ELSE) => eval(TEST) ~> finishIf(THEN, ELSE)

  rule eval(Call(Name(F), ARG)) => eval(ARG) ~> prepareCall(F)
  rule I:Int ~> prepareCall(F) => invoke(F, I)

  rule <k> invoke(F, I) => exec(BODY) ~> functionEnd(RHO) ... </k>
       <env> RHO => P |-> I </env>
       <functions>... F |-> function(P, BODY) ...</functions>

  rule Return(E) => eval(E) ~> makeReturn
  rule I:Int ~> makeReturn => returned(I)
  rule returned(I) ~> exec(_SS) => returned(I)
  rule <k> returned(I) ~> functionEnd(RHO) => I ... </k>
       <env> _ => RHO </env>
endmodule
