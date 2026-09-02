module MPY-SYNTAX
  imports INT
  imports STRING

  syntax Expr
  syntax Exprs   ::= List{Expr, ","}
  syntax CmpOp   ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps  ::= List{CmpOp, ","}
  syntax Strings ::= List{String, ","}
  syntax Params  ::= "Params" "(" Strings ")"
  syntax Stmt
  syntax Stmts   ::= List{Stmt, ""}

  syntax Expr ::= "NoneVal"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "ListExpr" "(" Exprs ")"

  syntax Stmt ::= "Module" "(" Stmts ")"
                | "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Return" "(" ")"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports BOOL
  imports MAP

  syntax Value
  syntax Values ::= List{Value, ","}
  syntax Value ::= "noneVal"
                 | "intVal" "(" Int ")"
                 | "strVal" "(" String ")"
                 | "boolVal" "(" Bool ")"
                 | "listVal" "(" Values ")"

  syntax Output ::= "noOutput" | Value
  syntax Function ::= "noFunction"
                    | "function" "(" Params "," Stmts ")"

  configuration
    <mpy>
      <k> $PGM:Stmt </k>
      <args> $ARGS:Value </args>
      <env> .Map </env>
      <function> noFunction </function>
      <out> noOutput </out>
    </mpy>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"
                 | "invokeEntry"
                 | "functionEnd"
                 | "branch" "(" Value "," Stmts "," Stmts ")"
                 | "forValues" "(" String "," Value "," Stmts ")"
                 | "returning" "(" Value ")"

  syntax Value ::= eval(Expr, Map)       [function]
                 | lookup(String, Map)   [function]
                 | pyLen(Value)          [function]
                 | isEmpty(Value)        [function]
                 | compare(String, Value, Value) [function]
                 | head(Value)           [function]

  rule <k> Module(SS) => exec(SS) ~> invokeEntry ... </k>

  rule exec(.Stmts) => .
  rule exec(S:Stmt SS:Stmts) => execStmt(S) ~> exec(SS)

  rule execStmt(ImportFrom(_, _)) => .
  rule <k> execStmt(FuncDef(_, P, BODY)) => . ... </k>
       <function> _ => function(P, BODY) </function>

  rule <k> invokeEntry => exec(BODY) ~> functionEnd ... </k>
       <args> V </args>
       <env> _ => X |-> V
                  "result" |-> noneVal
                  "string" |-> noneVal </env>
       <function> function(Params(X:String, .Strings), BODY) </function>

  rule <k> execStmt(Assign(Name(X), E)) => . ... </k>
       <env> (X |-> OLD REST)
               => (X |-> eval(E, X |-> OLD REST) REST) </env>

  rule <k> execStmt(If(E, THEN, ELSE))
            => branch(eval(E, ENV), THEN, ELSE) ... </k>
       <env> ENV </env>
  rule branch(boolVal(true),  THEN, _) => exec(THEN)
  rule branch(boolVal(false), _, ELSE) => exec(ELSE)

  rule <k> execStmt(For(Name(X), E, BODY))
            => forValues(X, eval(E, ENV), BODY) ... </k>
       <env> ENV </env>
  rule forValues(_, listVal(.Values), _) => .
  rule <k> forValues(X, listVal(V, VS), BODY)
            => exec(BODY) ~> forValues(X, listVal(VS), BODY) ... </k>
       <env> (X |-> _OLD REST) => (X |-> V REST) </env>

  rule <k> execStmt(Return(E)) => returning(eval(E, ENV)) ... </k>
       <env> ENV </env>
  rule <k> execStmt(Return()) => returning(noneVal) ... </k>

  rule returning(V) ~> exec(_) => returning(V)
  rule returning(V) ~> forValues(_, _, _) => returning(V)
  rule <k> returning(V) ~> functionEnd => . ... </k>
       <out> _ => V </out>

  rule eval(NoneVal, _) => noneVal
  rule eval(Int(I), _) => intVal(I)
  rule eval(Str(S), _) => strVal(S)
  rule eval(Name(X), ENV) => lookup(X, ENV)
  rule eval(Call(Name("len"), E), ENV) => pyLen(eval(E, ENV))
  rule eval(Compare(Call(Name("len"), E), CmpOp("==", Int(0))), ENV)
       => isEmpty(eval(E, ENV))
  rule eval(Compare(L, CmpOp(">", R)), ENV)
       => compare(">", eval(L, ENV), eval(R, ENV))
  rule eval(Subscript(E, Int(0)), ENV) => head(eval(E, ENV))

  rule lookup(X, (X |-> V) REST) => V
  rule lookup(X, ENV [ X <- V ]) => V [simplification]
  rule lookup(X, ENV [ Y <- _V ]) => lookup(X, ENV)
       requires X =/=String Y
       [simplification]

  rule pyLen(strVal(S)) => intVal(lengthString(S))
  rule pyLen(listVal(VS)) => intVal(sizeValues(VS))

  rule isEmpty(listVal(.Values)) => boolVal(true)
  rule isEmpty(listVal(_V, _VS)) => boolVal(false)
  rule isEmpty(strVal("")) => boolVal(true)
  rule isEmpty(strVal(S)) => boolVal(false) requires S =/=String ""

  syntax Int ::= sizeValues(Values) [function]
  rule sizeValues(.Values) => 0
  rule sizeValues(_V, VS) => 1 +Int sizeValues(VS)

  rule compare("==", intVal(I), intVal(J)) => boolVal(I ==Int J)
  rule compare(">", intVal(I), intVal(J)) => boolVal(I >Int J)

  rule head(listVal(V, _)) => V
endmodule
