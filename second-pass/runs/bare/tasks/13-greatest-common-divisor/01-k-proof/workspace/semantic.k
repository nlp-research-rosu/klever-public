module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Result ::= "noResult" | "result" "(" Int ")"

  configuration
    <gcd-program>
      <k> $PGM:Pgm </k>
      <env> .Map </env>
      <inputA> $A:Int </inputA>
      <inputB> $B:Int </inputB>
      <result> noResult </result>
    </gcd-program>

  syntax KItem ::= "execStmts" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"

  syntax Int ::= "evalInt" "(" Expr "," Map ")" [function]
  syntax Bool ::= "evalBool" "(" Expr "," Map ")" [function]

  rule evalInt(Int(I), _ENV) => I
  rule evalInt(Name(X), (X |-> I) _REST) => I
  rule evalInt(UnaryOp("-", E), ENV) => 0 -Int evalInt(E, ENV)
  rule evalInt(BinOp("%", E1, E2), ENV)
    => evalInt(E1, ENV) %Int evalInt(E2, ENV)

  rule evalBool(Compare(E1, CmpOp("<", E2)), ENV)
    => evalInt(E1, ENV) <Int evalInt(E2, ENV)
  rule evalBool(Compare(E1, CmpOp("!=", E2)), ENV)
    => evalInt(E1, ENV) =/=Int evalInt(E2, ENV)

  rule <k> Module(FuncDef("greatest_common_divisor", Params(X:String, Y:String), BODY))
            => execStmts(BODY) ... </k>
       <env> .Map => (X |-> A) (Y |-> B) </env>
       <inputA> A </inputA>
       <inputB> B </inputB>

  rule <k> execStmts(.Stmts) => .K ... </k>
  rule <k> execStmts(S SS) => execStmt(S) ~> execStmts(SS) ... </k>

  rule <k> execStmt(Assign(Name(X), E)) => .K ... </k>
       <env> ENV => ENV [ X <- evalInt(E, ENV) ] </env>

  rule <k> execStmt(If(COND, THEN, _ELSE)) => execStmts(THEN) ... </k>
       <env> ENV </env>
    requires evalBool(COND, ENV)
  rule <k> execStmt(If(COND, _THEN, ELSE)) => execStmts(ELSE) ... </k>
       <env> ENV </env>
    requires notBool evalBool(COND, ENV)

  rule <k> execStmt(While(COND, BODY))
            => execStmts(BODY) ~> execStmt(While(COND, BODY)) ... </k>
       <env> ENV </env>
    requires evalBool(COND, ENV)
  rule <k> execStmt(While(COND, _BODY)) => .K ... </k>
       <env> ENV </env>
    requires notBool evalBool(COND, ENV)

  rule <k> execStmt(Return(E)) ~> _REST:K => .K </k>
       <env> ENV </env>
       <result> noResult => result(evalInt(E, ENV)) </result>
endmodule
