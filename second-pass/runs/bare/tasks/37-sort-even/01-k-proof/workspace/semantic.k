requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports LIST

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Slice" "(" Bound "," Bound "," Bound ")"
                | "Call" "(" Expr "," Exprs ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Bound ::= Expr | "NoBound"

  syntax PyVal ::= "pyInt" "(" Int ")"
                 | "pyBool" "(" Bool ")"
                 | "pyList" "(" List ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  // Runtime lists contain K Int values. This is the task-relevant fragment of
  // Python lists; the AST syntax remains the translator's literal structure.

  configuration
    <mpy>
      <k> run($INPUT:PyVal) </k>
      <program> $PGM:Program </program>
    </mpy>

  syntax KItem ::= "run" "(" PyVal ")"
                 | "applyFunction" "(" String "," List ")"
                 | "applyFound" "(" Function "," List ")"
                 | "exec" "(" Stmts "," Map ")"
                 | "eval" "(" Expr "," Map ")"
                 | "ifResult" "(" Stmts "," Stmts "," Map ")"
                 | "plusLeft" "(" Expr "," Map ")"
                 | "plusRight" "(" PyVal ")"
                 | "compareLeft" "(" String "," Expr "," Map ")"
                 | "compareRight" "(" String "," PyVal ")"
                 | "indexResult" "(" Int ")"
                 | "sliceResult" "(" Int ")"
                 | "evalCallArgs" "(" String "," Exprs "," Map "," List ")"
                 | "callArgResult" "(" String "," Exprs "," Map "," List ")"
                 | "evalListItems" "(" Exprs "," Map "," List ")"
                 | "listItemResult" "(" Exprs "," Map "," List ")"
  syntax PyVal ::= "comparison" "(" String "," Int "," Int ")"
  syntax Function ::= "findFunction" "(" String "," Stmts ")" [function]
  syntax Map ::= "bind" "(" Params "," List ")" [function]
  syntax List ::= "dropList" "(" List "," Int ")" [function, total]
  syntax Int ::= "headInt" "(" List ")" [function, total, smtlib(headInt)]
  syntax Function ::= "function" "(" Params "," Stmts ")"

  rule dropList(L, 0) => L
  rule dropList(L, I) => range(L, minInt(I, size(L)), 0)
    requires I >Int 0
  rule headInt(ListItem(I:Int) _REST) => I

  rule run(V) => applyFunction("sort_even", ListItem(V))

  rule <k> applyFunction(F, VS) => applyFound(findFunction(F, S), VS) ... </k>
       <program> Module(S) </program>
  rule applyFound(function(PS, BODY), VS) => exec(BODY, bind(PS, VS))

  rule findFunction(F, FuncDef(F, PS, BODY) _REST)
    => function(PS, BODY)
  rule findFunction(F, FuncDef(G, _PS, _BODY) REST)
    => findFunction(F, REST)
    requires F =/=String G

  rule bind(Params(.Strings), .List) => .Map
  rule bind(Params(X, XS), ListItem(V) VS)
    => (X |-> V) bind(Params(XS), VS)

  rule exec(Return(E) _REST, ENV) => eval(E, ENV)
  rule exec(If(COND, THEN, ELSE) _REST, ENV)
    => eval(COND, ENV) ~> ifResult(THEN, ELSE, ENV)
  rule comparison("==", I, J) ~> ifResult(THEN, _ELSE, ENV) => exec(THEN, ENV)
    requires I ==Int J
  rule comparison("==", I, J) ~> ifResult(_THEN, ELSE, ENV) => exec(ELSE, ENV)
    requires I =/=Int J
  rule comparison("<=", I, J) ~> ifResult(THEN, _ELSE, ENV) => exec(THEN, ENV)
    requires I <=Int J
  rule comparison("<=", I, J) ~> ifResult(_THEN, ELSE, ENV) => exec(ELSE, ENV)
    requires I >Int J

  rule eval(Int(I), _ENV) => pyInt(I)
  rule eval(Name(X), (X |-> V) _REST) => V
  rule eval(ListExpr(ES), ENV) => evalListItems(ES, ENV, .List)
  rule eval(BinOp("+", E1, E2), ENV)
    => eval(E1, ENV) ~> plusLeft(E2, ENV)
  rule V1:PyVal ~> plusLeft(E2, ENV)
    => eval(E2, ENV) ~> plusRight(V1)
  rule pyList(L2) ~> plusRight(pyList(L1)) => pyList(L1 L2)

  rule eval(Compare(E1, CmpOp("==", E2)), ENV)
    => eval(E1, ENV) ~> compareLeft("==", E2, ENV)
  rule eval(Compare(E1, CmpOp("<=", E2)), ENV)
    => eval(E1, ENV) ~> compareLeft("<=", E2, ENV)
  rule V1:PyVal ~> compareLeft(OP, E2, ENV)
    => eval(E2, ENV) ~> compareRight(OP, V1)
  rule pyList(.List) ~> compareRight("==", pyList(L))
    => comparison("==", size(L), 0)
  rule pyInt(J) ~> compareRight("==", pyInt(I)) => comparison("==", I, J)
  rule pyInt(J) ~> compareRight("<=", pyInt(I)) => comparison("<=", I, J)

  rule eval(Subscript(E, Int(I)), ENV)
    => eval(E, ENV) ~> indexResult(I)
  rule eval(Subscript(E, Slice(Int(I), NoBound, NoBound)), ENV)
    => eval(E, ENV) ~> sliceResult(I)

  rule pyList(L) ~> indexResult(I) => pyInt(headInt(dropList(L, I)))

  rule pyList(L) ~> sliceResult(I) => pyList(dropList(L, I))

  rule eval(Call(Name(F), ES), ENV)
    => evalCallArgs(F, ES, ENV, .List)

  rule evalCallArgs(F, .Exprs, _ENV, VS) => applyFunction(F, VS)
  rule evalCallArgs(F, E, ES, ENV, VS)
    => eval(E, ENV) ~> callArgResult(F, ES, ENV, VS)
  rule V:PyVal ~> callArgResult(F, ES, ENV, VS)
    => evalCallArgs(F, ES, ENV, VS ListItem(V))

  rule evalListItems(.Exprs, _ENV, ITEMS) => pyList(ITEMS)
  rule evalListItems(E, ES, ENV, ITEMS)
    => eval(E, ENV) ~> listItemResult(ES, ENV, ITEMS)
  rule pyInt(I) ~> listItemResult(ES, ENV, ITEMS)
    => evalListItems(ES, ENV, ITEMS ListItem(I))
endmodule
