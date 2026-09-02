requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}
  syntax Exprs  ::= List{Expr, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Expr" "(" Expr ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," Cmp ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")"
                | "ListExpr" "(" Exprs ")"
  syntax Cmp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  syntax Val ::= "vInt" "(" Int ")"
               | "vBool" "(" Bool ")"
               | "vList" "(" List ")"
               | "vNone"
  syntax Expr ::= Val
  syntax Fn ::= "fn" "(" Params "," Stmts ")"
  syntax Result ::= "none" | "some" "(" Val ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "start" "(" Val "," Int ")"
                 | "assignName" "(" String ")"
                 | "discard"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Val ")"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareRight" "(" String "," Val ")"
                 | "subscriptLeft" "(" Expr ")"
                 | "subscriptRight" "(" Val ")"
                 | "lengthOf"
                 | "appendTo" "(" String ")"
                 | "ifResult" "(" Stmts "," Stmts ")"
                 | "whileResult" "(" Expr "," Stmts ")"
                 | "setResult"

  syntax Int ::= listLength(List) [function]
  rule listLength(.List) => 0
  rule listLength(ListItem(_) REST) => 1 +Int listLength(REST)

  syntax Val ::= getVal(List, Int) [function]
  rule getVal(ListItem(V:Val) _REST, 0) => V
  rule getVal(ListItem(_V:Val) REST, I) => getVal(REST, I -Int 1)
    requires I >Int 0

  configuration
    <py>
      <k> $PGM:Program ~> start($GRID:Val, $KLEN:Int) </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> none </result>
    </py>

  rule <k> Module(SS) => exec(SS) ... </k>
  rule <k> exec(.Stmts) => . ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>

  rule <k> FuncDef(F, PS, BODY) => . ... </k>
       <functions> FS => FS [ F <- fn(PS, BODY) ] </functions>

  rule <k> start(GRID, KLEN) => exec(BODY) ... </k>
       <functions> ... "minPath" |-> fn(Params("grid", "k"), BODY) ... </functions>
       <env> _ => "grid" |-> GRID "k" |-> vInt(KLEN) </env>

  rule <k> Assign(Name(X), E) => E ~> assignName(X) ... </k>
  rule <k> V:Val ~> assignName(X) => . ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> Expr(E) => E ~> discard ... </k>
  rule <k> _V:Val ~> discard => . ... </k>

  rule <k> Return(E) => E ~> setResult ... </k>
  rule <k> V:Val ~> setResult => . ... </k>
       <result> none => some(V) </result>

  rule <k> If(E, THEN, ELSE) => E ~> ifResult(THEN, ELSE) ... </k>
  rule <k> vBool(true) ~> ifResult(THEN, _ELSE) => exec(THEN) ... </k>
  rule <k> vBool(false) ~> ifResult(_THEN, ELSE) => exec(ELSE) ... </k>

  rule <k> While(E, BODY) => E ~> whileResult(E, BODY) ... </k>
  rule <k> vBool(true) ~> whileResult(E, BODY)
         => exec(BODY) ~> While(E, BODY) ... </k>
  rule <k> vBool(false) ~> whileResult(_E, _BODY) => . ... </k>

  rule <k> Int(I) => vInt(I) ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V ... </env>
  rule <k> ListExpr(.Exprs) => vList(.List) ... </k>

  rule <k> BinOp(OP, E1, E2) => E1 ~> binLeft(OP, E2) ... </k>
  rule <k> V1:Val ~> binLeft(OP, E2) => E2 ~> binRight(OP, V1) ... </k>
  rule <k> vInt(I2) ~> binRight("+", vInt(I1)) => vInt(I1 +Int I2) ... </k>
  rule <k> vInt(I2) ~> binRight("-", vInt(I1)) => vInt(I1 -Int I2) ... </k>
  rule <k> vInt(I2) ~> binRight("*", vInt(I1)) => vInt(I1 *Int I2) ... </k>
  rule <k> vInt(I2) ~> binRight("%", vInt(I1)) => vInt(I1 %Int I2) ... </k>

  rule <k> Compare(E1, CmpOp(OP, E2)) => E1 ~> compareLeft(OP, E2) ... </k>
  rule <k> V1:Val ~> compareLeft(OP, E2) => E2 ~> compareRight(OP, V1) ... </k>
  rule <k> vInt(I2) ~> compareRight("<",  vInt(I1)) => vBool(I1 <Int  I2) ... </k>
  rule <k> vInt(I2) ~> compareRight(">",  vInt(I1)) => vBool(I1 >Int  I2) ... </k>
  rule <k> vInt(I2) ~> compareRight("==", vInt(I1)) => vBool(I1 ==Int I2) ... </k>

  rule <k> Subscript(E1, E2) => E1 ~> subscriptLeft(E2) ... </k>
  rule <k> V1:Val ~> subscriptLeft(E2) => E2 ~> subscriptRight(V1) ... </k>
  rule <k> vInt(I) ~> subscriptRight(vList(L)) => getVal(L, I) ... </k>

  rule <k> Call(Name("len"), E, .Exprs) => E ~> lengthOf ... </k>
  rule <k> vList(L) ~> lengthOf => vInt(listLength(L)) ... </k>

  rule <k> Call(Attribute(Name(X), "append"), E, .Exprs) => E ~> appendTo(X) ... </k>
  rule <k> V:Val ~> appendTo(X) => vNone ... </k>
       <env> ... X |-> vList(L => L ListItem(V)) ... </env>
endmodule
