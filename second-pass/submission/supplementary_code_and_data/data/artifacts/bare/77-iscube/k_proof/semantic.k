requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  // Statement lists are juxtaposed by py2mpy.py; the separator is empty.
  syntax Stmts ::= List{Stmt, ""}

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")" [strict(2)]
                | "BinOp" "(" String "," Expr "," Expr ")" [strict(2,3)]
                | "Compare" "(" Expr "," CmpOp ")" [strict(1)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "Return" "(" Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Value ::= "IntVal" "(" Int ")"
                 | "BoolVal" "(" Bool ")"
  syntax KResult ::= Value
  syntax Expr ::= Value

  syntax Function ::= "function" "(" String "," Stmts ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "invoke" "(" Value ")"
                 | "assignTo" "(" String ")"
                 | "ifKont" "(" Stmts "," Stmts ")"
                 | "whileKont" "(" Expr "," Stmts ")"
                 | "compareKont" "(" String "," Int ")"
                 | "returnKont"

  configuration
    <mpy>
      <k> $PGM:Pgm ~> invoke(IntVal($N:Int)) </k>
      <funs> .Map </funs>
      <env> .Map </env>
      <result> .K </result>
    </mpy>

  // Module loading and the single-argument function call used by this task.
  rule Module(STMTS) => exec(STMTS)
  rule exec(.Stmts) => .K
  rule exec(S:Stmt REST:Stmts) => S ~> exec(REST)

  rule <k> FuncDef(F, Params(P), BODY) => .K ...</k>
       <funs> .Map => F |-> function(P, BODY) </funs>

  rule <k> invoke(IntVal(A)) => exec(BODY) ...</k>
       <funs> ... "iscube" |-> function(P, BODY) ...</funs>
       <env> .Map => P |-> IntVal(A) </env>

  // Expression evaluation.  Strictness gives left-to-right evaluation for
  // unary and binary operators; comparisons explicitly evaluate their RHS.
  rule <k> Int(I) => IntVal(I) ...</k>
  rule <k> Name(X) => V ...</k>
       <env> ... X |-> V:Value ...</env>

  rule UnaryOp("-", IntVal(I)) => IntVal(0 -Int I)
  rule BinOp("+", IntVal(I), IntVal(J)) => IntVal(I +Int J)
  rule BinOp("*", IntVal(I), IntVal(J)) => IntVal(I *Int J)

  rule Compare(IntVal(I), CmpOp(OP, E)) => E ~> compareKont(OP, I)

  rule IntVal(J) ~> compareKont("<", I) => BoolVal(I <Int J)
  rule IntVal(J) ~> compareKont("==", I) => BoolVal(I ==Int J)

  // Statements and control flow.
  rule Assign(Name(X), E) => E ~> assignTo(X)
  rule <k> V:Value ~> assignTo(X) => .K ...</k>
       <env> RHO => RHO [ X <- V ] </env>

  rule If(COND, THEN, ELSE) => COND ~> ifKont(THEN, ELSE)
  rule BoolVal(true)  ~> ifKont(THEN, _ELSE) => exec(THEN)
  rule BoolVal(false) ~> ifKont(_THEN, ELSE) => exec(ELSE)

  rule While(COND, BODY) => COND ~> whileKont(COND, BODY)
  rule BoolVal(true)  ~> whileKont(COND, BODY) => exec(BODY) ~> While(COND, BODY)
  rule BoolVal(false) ~> whileKont(_COND, _BODY) => .K

  rule Return(E) => E ~> returnKont
  rule <k> V:Value ~> returnKont ~> _REST => .K </k>
       <result> .K => V </result>
endmodule
