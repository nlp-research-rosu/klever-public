module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Exprs  ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "ListExpr" "(" Exprs ")"
                | "TupleExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Call" "(" Expr "," Exprs ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax VList ::= "vnil" | "vcons" "(" Value "," VList ")"
  syntax Value ::= "pyInt" "(" Int ")"
                 | "pyBool" "(" Bool ")"
                 | "pyList" "(" VList ")"
                 | "pyTuple" "(" VList ")"

  syntax Function ::= "function" "(" Params "," Stmts ")"
  syntax Result ::= "noResult" | "returned" "(" Value ")"
  syntax Args ::= "pyArgs" "(" Value "," Value ")"

  configuration
    <py>
      <k> $PGM:Program ~> start </k>
      <args> pyArgs($LST:Value, $X:Value) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult </result>
    </py>

  syntax KItem ::= "start"
                 | "exec" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"
                 | "eval" "(" Expr ")"
                 | "assignTo" "(" String ")"
                 | "forReady" "(" String "," Stmts ")"
                 | "forLoop" "(" String "," VList "," Stmts ")"
                 | "whileLoop" "(" Expr "," Stmts ")"
                 | "whileGuard" "(" Expr "," Stmts ")"
                 | "ifGuard" "(" Stmts "," Stmts ")"
                 | "evalExprs" "(" Exprs ")"
                 | "evalExprsTail" "(" Exprs ")"
                 | "prependValue" "(" Value ")"
                 | "asTuple"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "cmpLeft" "(" String "," Expr ")"
                 | "cmpRight" "(" String "," Value ")"
                 | "subscriptBase" "(" Expr ")"
                 | "subscriptIndex" "(" Value ")"
                 | "doLen"
                 | "doReturn"

  syntax Int ::= "vlen" "(" VList ")" [function]
  rule vlen(vnil) => 0
  rule vlen(vcons(_, VS)) => 1 +Int vlen(VS)

  syntax VList ::= "vconcat" "(" VList "," VList ")" [function]
  rule vconcat(vnil, VS) => VS
  rule vconcat(vcons(V, VS), WS) => vcons(V, vconcat(VS, WS))

  syntax Value ::= "vnth" "(" VList "," Int ")" [function]
  rule vnth(vcons(V, _), 0) => V
  rule vnth(vcons(_, VS), I) => vnth(VS, I -Int 1) requires I >Int 0

  rule <k> Module(SS) => exec(SS) ... </k>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt SS:Stmts) => execStmt(S) ~> exec(SS) ... </k>

  rule <k> execStmt(FuncDef(F, P, SS)) => .K ... </k>
       <functions> FS => FS [ F <- function(P, SS) ] </functions>

  rule <k> start => exec(SS) ... </k>
       <args> pyArgs(LST, X) </args>
       <functions> ... "get_row" |-> function(Params("lst", "x"), SS) ... </functions>
       <env> _ => "lst" |-> LST  "x" |-> X </env>

  rule <k> execStmt(Assign(Name(N), E)) => eval(E) ~> assignTo(N) ... </k>
  rule <k> V:Value ~> assignTo(N) => .K ... </k>
       <env> ENV => ENV [ N <- V ] </env>

  rule <k> execStmt(For(Name(N), E, BODY)) => eval(E) ~> forReady(N, BODY) ... </k>
  rule <k> pyList(VS) ~> forReady(N, BODY) => forLoop(N, VS, BODY) ... </k>
  rule <k> forLoop(_, vnil, _) => .K ... </k>
  rule <k> forLoop(N, vcons(V, VS), BODY) => exec(BODY) ~> forLoop(N, VS, BODY) ... </k>
       <env> ENV => ENV [ N <- V ] </env>

  rule <k> execStmt(While(COND, BODY)) => whileLoop(COND, BODY) ... </k>
  rule <k> whileLoop(COND, BODY) => eval(COND) ~> whileGuard(COND, BODY) ... </k>
  rule <k> pyBool(true) ~> whileGuard(COND, BODY) => exec(BODY) ~> whileLoop(COND, BODY) ... </k>
  rule <k> pyBool(false) ~> whileGuard(_, _) => .K ... </k>

  rule <k> execStmt(If(COND, THEN, ELSE)) => eval(COND) ~> ifGuard(THEN, ELSE) ... </k>
  rule <k> pyBool(true) ~> ifGuard(THEN, _) => exec(THEN) ... </k>
  rule <k> pyBool(false) ~> ifGuard(_, ELSE) => exec(ELSE) ... </k>

  rule <k> execStmt(Return(E)) => eval(E) ~> doReturn ... </k>
  rule <k> V:Value ~> doReturn ~> _REST:K => .K </k>
       <result> noResult => returned(V) </result>
       <env> _ => .Map </env>
       <functions> _ => .Map </functions>

  rule <k> eval(Int(I)) => pyInt(I) ... </k>
  rule <k> eval(Bool(B)) => pyBool(B) ... </k>
  rule <k> eval(Name(N)) => V ... </k>
       <env> ... N |-> V:Value ... </env>

  rule <k> eval(ListExpr(ES)) => evalExprs(ES) ... </k>
  rule <k> eval(TupleExpr(ES)) => evalExprs(ES) ~> asTuple ... </k>
  rule <k> pyList(VS) ~> asTuple => pyTuple(VS) ... </k>

  rule <k> evalExprs(.Exprs) => pyList(vnil) ... </k>
  rule <k> evalExprs(E:Expr, ES:Exprs) => eval(E) ~> evalExprsTail(ES) ... </k>
  rule <k> V:Value ~> evalExprsTail(ES) => evalExprs(ES) ~> prependValue(V) ... </k>
  rule <k> pyList(VS) ~> prependValue(V) => pyList(vcons(V, VS)) ... </k>

  rule <k> eval(BinOp(OP, L, R)) => eval(L) ~> binLeft(OP, R) ... </k>
  rule <k> LV:Value ~> binLeft(OP, R) => eval(R) ~> binRight(OP, LV) ... </k>
  rule <k> pyInt(R) ~> binRight("-", pyInt(L)) => pyInt(L -Int R) ... </k>
  rule <k> pyInt(R) ~> binRight("+", pyInt(L)) => pyInt(L +Int R) ... </k>
  rule <k> pyList(R) ~> binRight("+", pyList(L)) => pyList(vconcat(L, R)) ... </k>

  rule <k> eval(Compare(L, CmpOp(OP, R))) => eval(L) ~> cmpLeft(OP, R) ... </k>
  rule <k> LV:Value ~> cmpLeft(OP, R) => eval(R) ~> cmpRight(OP, LV) ... </k>
  rule <k> pyInt(R) ~> cmpRight(">=", pyInt(L)) => pyBool(L >=Int R) ... </k>
  rule <k> pyInt(R) ~> cmpRight("==", pyInt(L)) => pyBool(L ==Int R) ... </k>

  rule <k> eval(Subscript(BASE, INDEX)) => eval(BASE) ~> subscriptBase(INDEX) ... </k>
  rule <k> BV:Value ~> subscriptBase(INDEX) => eval(INDEX) ~> subscriptIndex(BV) ... </k>
  rule <k> pyInt(I) ~> subscriptIndex(pyList(VS)) => vnth(VS, I) ... </k>

  rule <k> eval(Call(Name("len"), E)) => eval(E) ~> doLen ... </k>
  rule <k> pyList(VS) ~> doLen => pyInt(vlen(VS)) ... </k>
endmodule

module SEMANTIC
  imports MPY-SEMANTIC
endmodule
