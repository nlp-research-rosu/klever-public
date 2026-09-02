requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")" [symbol(module)]

  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" String "," String ")" [symbol(params)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(funcDef)]
                | "Assign" "(" Expr "," Expr ")"                 [symbol(assign)]
                | "If" "(" Expr "," Stmts "," Stmts ")"       [symbol(ifStmt)]
                | "While" "(" Expr "," Stmts ")"               [symbol(whileStmt)]
                | "Return" "(" Expr ")"                         [symbol(returnStmt)]

  syntax Cmp ::= "CmpOp" "(" String "," Expr ")" [symbol(cmpOp)]

  syntax Expr ::= "Int" "(" Int ")"                         [symbol(intExpr)]
                | "Str" "(" String ")"                      [symbol(strExpr)]
                | "Name" "(" String ")"                     [symbol(nameExpr)]
                | "TupleExpr" "(" Expr "," Expr ")"        [symbol(tupleExpr)]
                | "Subscript" "(" Expr "," Expr ")"        [symbol(subscript)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(binOp)]
                | "Compare" "(" Expr "," Cmp ")"            [symbol(compare)]
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Value ::= "intVal" "(" Int ")"
                 | "strVal" "(" String ")"
                 | "boolVal" "(" Bool ")"
                 | "tupleVal" "(" Value "," Value ")"
                 | "unbound"
  syntax Expr ::= Value
  syntax KResult ::= Value

  syntax Function ::= "function" "(" String "," String "," Stmts ")"

  syntax KItem ::= Program | Stmt | Stmts | Expr
                 | "runWith" "(" Expr "," Expr ")"
                 | "saveFirstArg" "(" Expr ")"
                 | "saveSecondArg" "(" Value ")"
                 | "invoke" "(" String "," Value "," Value ")"
                 | "assignTo" "(" String ")"
                 | "choose" "(" Stmts "," Stmts ")"
                 | "loopGuard" "(" Expr "," Stmts ")"
                 | "functionReturn"

  configuration
    <mpy>
      <k> $PGM:Program ~> runWith($INTERVAL1:Expr, $INTERVAL2:Expr) </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </mpy>

  // Module loading and entry-point invocation.
  rule <k> Module(S) => S ...</k>
  rule <k> .Stmts => .K ...</k>
  rule <k> (S:Stmt SS:Stmts) => S ~> SS ...</k>

  rule <k> FuncDef(F, Params(P1, P2), BODY) => .K ...</k>
       <functions> .Map => F |-> function(P1, P2, BODY) </functions>

  rule <k> runWith(A, B) => A ~> saveFirstArg(B) ...</k>
  rule <k> V:Value ~> saveFirstArg(B) => B ~> saveSecondArg(V) ...</k>
  rule <k> V2:Value ~> saveSecondArg(V1) => invoke("intersection", V1, V2) ...</k>

  rule <k> invoke(F, V1, V2) => BODY ...</k>
       <functions> F |-> function(P1, P2, BODY) </functions>
       <env> _ =>
         P1 |-> V1
         P2 |-> V2
         "left"    |-> unbound
         "right"   |-> unbound
         "length"  |-> unbound
         "divisor" |-> unbound
       </env>

  // Statement execution.
  rule <k> Assign(Name(X), E) => E ~> assignTo(X) ...</k>
  rule <k> V:Value ~> assignTo(X) => .K ...</k>
       <env>... X |-> (_ => V) ...</env>

  rule <k> If(COND, THEN, ELSE) => COND ~> choose(THEN, ELSE) ...</k>
  rule <k> boolVal(true)  ~> choose(THEN, _) => THEN ...</k>
  rule <k> boolVal(false) ~> choose(_, ELSE) => ELSE ...</k>

  rule <k> While(COND, BODY) => COND ~> loopGuard(COND, BODY) ...</k>
  rule <k> boolVal(true)  ~> loopGuard(COND, BODY) => BODY ~> While(COND, BODY) ...</k>
  rule <k> boolVal(false) ~> loopGuard(_, _) => .K ...</k>

  // A return abandons the rest of the current function body, including a
  // surrounding loop continuation, and leaves the returned Value in <k>.
  rule <k> Return(E) ~> _REST => E ~> functionReturn </k>
  rule <k> V:Value ~> functionReturn => V ...</k>

  // Expression execution.  Contexts make operands evaluate left-to-right.
  rule <k> Int(I) => intVal(I) ...</k>
  rule <k> Str(S) => strVal(S) ...</k>
  rule <k> Name(X) => V ...</k>
       <env>... X |-> V ...</env>

  context TupleExpr(HOLE, _)
  context TupleExpr(_V:Value, HOLE)
  rule <k> TupleExpr(V1:Value, V2:Value) => tupleVal(V1, V2) ...</k>

  context Subscript(HOLE, _)
  context Subscript(_V:Value, HOLE)
  rule <k> Subscript(tupleVal(V0, _), intVal(0)) => V0 ...</k>
  rule <k> Subscript(tupleVal(_, V1), intVal(1)) => V1 ...</k>

  context BinOp(_, HOLE, _)
  context BinOp(_, _V:Value, HOLE)
  rule <k> BinOp("+", intVal(A), intVal(B)) => intVal(A +Int B) ...</k>
  rule <k> BinOp("-", intVal(A), intVal(B)) => intVal(A -Int B) ...</k>
  rule <k> BinOp("*", intVal(A), intVal(B)) => intVal(A *Int B) ...</k>
  rule <k> BinOp("%", intVal(A), intVal(B)) => intVal(A %Int B) ...</k>
       requires B =/=Int 0

  rule <k> Compare(A, CmpOp(OP, B)) => compareValues(OP, A, B) ...</k>
  syntax Expr ::= "compareValues" "(" String "," Expr "," Expr ")"
  context compareValues(_, HOLE, _)
  context compareValues(_, _V:Value, HOLE)
  rule <k> compareValues("<",  intVal(A), intVal(B)) => boolVal(A <Int B) ...</k>
  rule <k> compareValues("<=", intVal(A), intVal(B)) => boolVal(A <=Int B) ...</k>
  rule <k> compareValues(">",  intVal(A), intVal(B)) => boolVal(A >Int B) ...</k>
  rule <k> compareValues("==", intVal(A), intVal(B)) => boolVal(A ==Int B) ...</k>
endmodule
