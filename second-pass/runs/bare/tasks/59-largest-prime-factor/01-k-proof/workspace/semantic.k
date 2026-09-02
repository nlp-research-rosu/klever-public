module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax PyModule ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Result ::= "noResult" | "result" "(" Int ")"

  configuration
    <py>
      <k> $PGM:PyModule </k>
      <input> $N:Int </input>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  // This task only needs integers, integer arithmetic, comparisons,
  // assignment, conditionals, while, return, and one top-level function.
  syntax Int ::= evalInt(Expr, Map) [function]
  rule evalInt(Int(I), _) => I
  rule evalInt(Name(X), X |-> I _M) => I
  rule evalInt(BinOp("+", A, B), M) => evalInt(A, M) +Int evalInt(B, M)
  rule evalInt(BinOp("*", A, B), M) => evalInt(A, M) *Int evalInt(B, M)
  rule evalInt(BinOp("//", A, B), M) => evalInt(A, M) /Int evalInt(B, M)
    requires evalInt(B, M) =/=Int 0
  rule evalInt(BinOp("%", A, B), M) => evalInt(A, M) %Int evalInt(B, M)
    requires evalInt(B, M) =/=Int 0

  syntax Bool ::= evalBool(Expr, Map) [function]
  rule evalBool(Compare(A, CmpOp("<=", B)), M)
    => evalInt(A, M) <=Int evalInt(B, M)
  rule evalBool(Compare(A, CmpOp("==", B)), M)
    => evalInt(A, M) ==Int evalInt(B, M)

  syntax KItem ::= exec(Stmts)
                 | execStmt(Stmt)
                 | setVar(String, Int)

  // Loading the translated module invokes its required entry point with N.
  rule <k> Module(FuncDef("largest_prime_factor", Params("n"), BODY))
            => exec(BODY) ... </k>
       <input> N </input>
       <env> .Map => "n" |-> N </env>

  rule exec(.Stmts) => .K
  rule exec(S SS) => execStmt(S) ~> exec(SS)

  rule <k> execStmt(Assign(Name(X), E)) => setVar(X, evalInt(E, M)) ... </k>
       <env> M </env>
  rule <k> setVar(X, I) => .K ... </k>
       <env> M => M [ X <- I ] </env>

  rule <k> execStmt(If(COND, THEN, _ELSE)) => exec(THEN) ... </k>
       <env> M </env>
    requires evalBool(COND, M)
  rule <k> execStmt(If(COND, _THEN, ELSE)) => exec(ELSE) ... </k>
       <env> M </env>
    requires notBool evalBool(COND, M)

  rule <k> execStmt(While(COND, BODY))
            => exec(BODY) ~> execStmt(While(COND, BODY)) ... </k>
       <env> M </env>
    requires evalBool(COND, M)
  rule <k> execStmt(While(COND, _BODY)) => .K ... </k>
       <env> M </env>
    requires notBool evalBool(COND, M)

  rule <k> execStmt(Return(E)) => .K ... </k>
       <env> M </env>
       <result> noResult => result(evalInt(E, M)) </result>
endmodule
