module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports LIST

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Params  ::= "Params" "(" String "," String ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt  ::= "FuncDef" "(" String "," Params "," Stmts ")"
                 | "Assign" "(" Expr "," Expr ")"
                 | "While" "(" Expr "," Stmts ")"
                 | "If" "(" Expr "," Stmts "," Stmts ")"
                 | "Return" "(" Expr ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "BoolOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Subscript" "(" Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports LIST
  imports MAP

  syntax Value ::= Int | Bool | List
  syntax KResult ::= Value
  syntax Result ::= "noResult" | "result" "(" Value ")"

  // Python arrays are lists of integers for this task.  Keeping lookup as a
  // typed function makes the contract's element type explicit to the prover.
  syntax Int ::= "intAt" "(" List "," Int ")" [function]
  rule intAt(ListItem(I:Int) _REST, 0) => I
  rule intAt(ListItem(_I:Int) REST, N) => intAt(REST, N -Int 1)
    requires N >Int 0

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "setVar" "(" String ")"
                 | "ifBranches" "(" Stmts "," Stmts ")"
                 | "whileBody" "(" Expr "," Stmts ")"
                 | "negate"
                 | "addRight" "(" Expr ")"
                 | "addLeft" "(" Int ")"
                 | "andRight" "(" Expr ")"
                 | "compareRight" "(" Expr ")"
                 | "lessThanLeft" "(" Int ")"
                 | "subscriptIndex" "(" Expr ")"
                 | "getAt" "(" List ")"
                 | "doReturn"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <env> .Map </env>
      <input>
        <arr> $ARR:List </arr>
        <n> $N:Int </n>
      </input>
      <result> noResult </result>
    </mpy>

  rule <k> Module(FuncDef("add_elements", Params("arr", "k"), BODY))
         => exec(BODY) ... </k>
       <env> .Map => "arr" |-> A "k" |-> N </env>
       <arr> A </arr>
       <n> N </n>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>

  rule <k> Assign(Name(X), E) => E ~> setVar(X) ... </k>
  rule <k> V:Value ~> setVar(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> If(E, THEN, ELSE) => E ~> ifBranches(THEN, ELSE) ... </k>
  rule <k> true  ~> ifBranches(THEN, _ELSE) => exec(THEN) ... </k>
  rule <k> false ~> ifBranches(_THEN, ELSE) => exec(ELSE) ... </k>

  rule <k> While(E, BODY) => E ~> whileBody(E, BODY) ... </k>
  rule <k> true  ~> whileBody(E, BODY) => exec(BODY) ~> While(E, BODY) ... </k>
  rule <k> false ~> whileBody(_E, _BODY) => .K ... </k>

  rule <k> Return(E) => E ~> doReturn ... </k>
  rule <k> V:Value ~> doReturn ~> _REST:K => .K </k>
       <result> noResult => result(V) </result>

  rule <k> Int(I) => I ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V:Value ... </env>

  rule <k> UnaryOp("-", E) => E ~> negate ... </k>
  rule <k> I:Int ~> negate => 0 -Int I ... </k>

  rule <k> BinOp("+", E1, E2) => E1 ~> addRight(E2) ... </k>
  rule <k> I:Int ~> addRight(E2) => E2 ~> addLeft(I) ... </k>
  rule <k> J:Int ~> addLeft(I) => I +Int J ... </k>

  rule <k> BoolOp("and", E1, E2) => E1 ~> andRight(E2) ... </k>
  rule <k> true  ~> andRight(E2) => E2 ... </k>
  rule <k> false ~> andRight(_E2) => false ... </k>

  rule <k> Compare(E1, CmpOp("<", E2)) => E1 ~> compareRight(E2) ... </k>
  rule <k> I:Int ~> compareRight(E2) => E2 ~> lessThanLeft(I) ... </k>
  rule <k> J:Int ~> lessThanLeft(I) => I <Int J ... </k>

  rule <k> Subscript(E1, E2) => E1 ~> subscriptIndex(E2) ... </k>
  rule <k> A:List ~> subscriptIndex(E2) => E2 ~> getAt(A) ... </k>
  rule <k> I:Int ~> getAt(A) => intAt(A, I) ... </k>
endmodule
