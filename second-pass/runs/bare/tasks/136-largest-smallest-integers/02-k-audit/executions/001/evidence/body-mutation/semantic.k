requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports MAP
  imports LIST

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}

  syntax Params ::= "Params" "(" String ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax IntSeq ::= "nil"
                  | "icon" "(" Int "," IntSeq ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "NoneVal"
                | "Compare" "(" Expr "," CmpOp ")"
                | "ListExpr" "(" Exprs ")"
                | "TupleExpr" "(" Expr "," Expr ")"
                | "Value" "(" PyVal ")"

  syntax OptInt ::= "pyInt" "(" Int ")"
                  | "pyNone"

  syntax PyVal ::= OptInt
                 | "pyBool" "(" Bool ")"
                 | "pyList" "(" List ")"
                 | "pyIntList" "(" IntSeq ")"
                 | "pyTuple" "(" PyVal "," PyVal ")"

  syntax KResult ::= PyVal
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  configuration
    <mpy>
      <k> run($PGM:Program, $INPUT:Expr) </k>
      <env> .Map </env>
      <steps> 0 </steps>
    </mpy>

  syntax KItem ::= "run" "(" Program "," Expr ")"
                 | "start" "(" Program ")"
                 | "exec" "(" Stmts ")"
                 | "bind" "(" String "," PyVal ")"
                 | "store" "(" String ")"
                 | "branch" "(" Stmts "," Stmts ")"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareRight" "(" String "," PyVal ")"
                 | "tupleLeft" "(" Expr ")"
                 | "tupleRight" "(" PyVal ")"
                 | "makeList" "(" Exprs "," List ")"
                 | "listValue" "(" Exprs "," List ")"
                 | "loop" "(" String "," Stmts ")"
                 | "iterate" "(" String "," List "," Stmts ")"
                 | "iterateIntSeq" "(" String "," IntSeq "," Stmts ")"
                 | "bindIteration" "(" String "," PyVal ")"
                 | "iterationDone"

  rule <k> run(P, E) => E ~> start(P) ... </k>
  rule <k> V:PyVal ~> start(
              Module(FuncDef(_F, Params(X), BODY))
            )
         => bind(X, V) ~> exec(BODY) ... </k>

  rule <k> bind(X, V) => .K ... </k>
       <env> ... X |-> (_ => V) ... </env>
  rule <k> bind(X, V) => .K ... </k>
       <env> M => M [ X <- V ] </env>
    requires notBool (X in_keys(M))

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt SS:Stmts) => S ~> exec(SS) ... </k>

  rule <k> Int(I) => pyInt(I) ... </k>
  rule <k> NoneVal => pyNone ... </k>
  rule <k> Value(V) => V ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V ... </env>

  rule <k> Assign(Name(X), E) => E ~> store(X) ... </k>
  rule <k> V:PyVal ~> store(X) => .K ... </k>
       <env> ... X |-> (_ => V) ... </env>
  rule <k> V:PyVal ~> store(X) => .K ... </k>
       <env> M => M [ X <- V ] </env>
    requires notBool (X in_keys(M))

  rule <k> Compare(E1, CmpOp(OP, E2))
         => E1 ~> compareLeft(OP, E2) ... </k>
  rule <k> V1:PyVal ~> compareLeft(OP, E2)
         => E2 ~> compareRight(OP, V1) ... </k>
  rule <k> pyInt(I2) ~> compareRight("<", pyInt(I1))
         => pyBool(I1 <Int I2) ... </k>
  rule <k> pyInt(I2) ~> compareRight(">", pyInt(I1))
         => pyBool(I1 >Int I2) ... </k>
  rule <k> pyNone ~> compareRight("is", pyNone)
         => pyBool(true) ... </k>
  rule <k> pyNone ~> compareRight("is", pyInt(_I))
         => pyBool(false) ... </k>

  rule <k> If(E, THEN, ELSE)
         => E ~> branch(THEN, ELSE) ... </k>
  rule <k> pyBool(true) ~> branch(THEN, _ELSE)
         => exec(THEN) ... </k>
  rule <k> pyBool(false) ~> branch(_THEN, ELSE)
         => exec(ELSE) ... </k>

  rule <k> TupleExpr(E1, E2) => E1 ~> tupleLeft(E2) ... </k>
  rule <k> V1:PyVal ~> tupleLeft(E2)
         => E2 ~> tupleRight(V1) ... </k>
  rule <k> V2:PyVal ~> tupleRight(V1)
         => pyTuple(V1, V2) ... </k>

  rule <k> ListExpr(ES) => makeList(ES, .List) ... </k>
  rule <k> makeList(.Exprs, VS) => pyList(VS) ... </k>
  rule <k> makeList(E:Expr, VS)
         => E ~> listValue(.Exprs, VS) ... </k>
  rule <k> makeList(E:Expr, ES:Exprs, VS)
         => E ~> listValue(ES, VS) ... </k>
  rule <k> V:PyVal ~> listValue(ES, VS)
         => makeList(ES, VS ListItem(V)) ... </k>

  rule <k> For(Name(X), E, BODY)
         => E ~> loop(X, BODY) ... </k>
  rule <k> pyList(VS) ~> loop(X, BODY)
         => iterate(X, VS, BODY) ... </k>
  rule <k> pyIntList(IS) ~> loop(X, BODY)
         => iterateIntSeq(X, IS, BODY) ... </k>
  rule <k> iterate(_X, .List, _BODY) => .K ... </k>
  rule <k> iterate(X, ListItem(V) REST, BODY)
         => bindIteration(X, V)
         ~> exec(BODY)
         ~> iterationDone
         ~> iterate(X, REST, BODY) ... </k>
  rule <k> iterateIntSeq(_X, nil, _BODY) => .K ... </k>
  rule <k> iterateIntSeq(X, icon(I, IS), BODY)
         => bindIteration(X, pyInt(I))
         ~> exec(BODY)
         ~> iterationDone
         ~> iterateIntSeq(X, IS, BODY) ... </k>
  rule <k> bindIteration(X, V) => .K ... </k>
       <env> ... X |-> (_ => V) ... </env>
  rule <k> bindIteration(X, V) => .K ... </k>
       <env> M => M [ X <- V ] </env>
    requires notBool (X in_keys(M))
  rule <k> iterationDone => .K ... </k>
       <steps> S => S +Int 1 </steps>

  // A return abandons the remaining statement sequence in its function.
  rule <k> Return(E) ~> exec(_SS) => E ... </k>
endmodule
