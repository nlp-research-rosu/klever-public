requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")" [symbol]

  syntax Params ::= "Params" "(" String ")" [symbol]

  syntax Expr ::= "Int" "(" Int ")" [symbol]
                | "Name" "(" String ")" [symbol]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol]
                | "Compare" "(" Expr "," CmpOp ")" [symbol]
                | "TupleExpr" "(" Expr "," Expr ")" [symbol]
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol]
                | "Assign" "(" Expr "," Expr ")" [symbol]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol]
                | "Return" "(" Expr ")" [symbol]
  syntax Stmts ::= List{Stmt, ""}
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Value ::= "VInt" "(" Int ")" [symbol]
                 | "VBool" "(" Bool ")" [symbol]
                 | "VTuple" "(" Value "," Value ")" [symbol]

  syntax ReturnState ::= "noReturn" [symbol]
                       | "returned" "(" Value ")" [symbol]

  syntax KItem ::= "run" "(" Pgm "," Int ")" [symbol]
                 | "exec" "(" Stmts ")" [symbol]
                 | "finish" [symbol]

  configuration
    <mpy>
      <k> run($PGM:Pgm, $N:Int) </k>
      <env> .Map </env>
      <return> noReturn </return>
    </mpy>

  syntax Value ::= "eval" "(" Expr "," Map ")" [function]
                 | "lookupValue" "(" Map "," String ")" [function]
  syntax Int ::= "getInt" "(" Value ")" [function]
  syntax Bool ::= "getBool" "(" Value ")" [function]

  rule getInt(VInt(I)) => I
  rule getBool(VBool(B)) => B

  rule eval(Int(I), _) => VInt(I)
  rule lookupValue((X |-> V:Value) REST, X) => V
  rule eval(Name(X), ENV) => lookupValue(ENV, X)

  rule eval(BinOp("+", A, B), ENV)
    => VInt(getInt(eval(A, ENV)) +Int getInt(eval(B, ENV)))
  rule eval(BinOp("-", A, B), ENV)
    => VInt(getInt(eval(A, ENV)) -Int getInt(eval(B, ENV)))
  rule eval(BinOp("*", A, B), ENV)
    => VInt(getInt(eval(A, ENV)) *Int getInt(eval(B, ENV)))
  rule eval(BinOp("//", A, B), ENV)
    => VInt(getInt(eval(A, ENV)) /Int getInt(eval(B, ENV)))
  rule eval(BinOp("%", A, B), ENV)
    => VInt(getInt(eval(A, ENV)) %Int getInt(eval(B, ENV)))

  rule eval(Compare(A, CmpOp("<", B)), ENV)
    => VBool(getInt(eval(A, ENV)) <Int getInt(eval(B, ENV)))
  rule eval(Compare(A, CmpOp("<=", B)), ENV)
    => VBool(getInt(eval(A, ENV)) <=Int getInt(eval(B, ENV)))
  rule eval(Compare(A, CmpOp(">", B)), ENV)
    => VBool(getInt(eval(A, ENV)) >Int getInt(eval(B, ENV)))
  rule eval(Compare(A, CmpOp(">=", B)), ENV)
    => VBool(getInt(eval(A, ENV)) >=Int getInt(eval(B, ENV)))
  rule eval(Compare(A, CmpOp("==", B)), ENV)
    => VBool(getInt(eval(A, ENV)) ==Int getInt(eval(B, ENV)))

  rule eval(TupleExpr(A, B), ENV) => VTuple(eval(A, ENV), eval(B, ENV))

  rule <k> run(Module(FuncDef("even_odd_palindrome", Params("n"), BODY)), N)
        => exec(BODY) ~> finish ... </k>
       <env> _ => "n" |-> VInt(N) </env>
       <return> _ => noReturn </return>

  rule exec(.Stmts) => .
  rule <k> exec(_:Stmts) => . ... </k>
       <return> returned(_) </return>

  rule <k> exec(Assign(Name(X), E) REST) => exec(REST) ... </k>
       <env> ENV => ENV [ X <- eval(E, ENV) ] </env>
       <return> noReturn </return>

  rule <k> exec(If(COND, THEN, ELSE) REST)
        => exec(THEN) ~> exec(REST) ... </k>
       <env> ENV </env>
       <return> noReturn </return>
    requires getBool(eval(COND, ENV))
  rule <k> exec(If(COND, THEN, ELSE) REST)
        => exec(ELSE) ~> exec(REST) ... </k>
       <env> ENV </env>
       <return> noReturn </return>
    requires notBool getBool(eval(COND, ENV))

  rule <k> exec(Return(E) _REST) => . ... </k>
       <env> ENV </env>
       <return> noReturn => returned(eval(E, ENV)) </return>

  rule <k> finish => V ... </k>
       <return> returned(V) => noReturn </return>
endmodule
