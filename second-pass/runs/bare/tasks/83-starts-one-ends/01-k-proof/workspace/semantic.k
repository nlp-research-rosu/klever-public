module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The constructor grammar needed by solution.mpy.  Constructor names and
  // argument order deliberately match py2mpy.py exactly.
  syntax Pgm ::= "Module" "(" Stmts ")" [symbol(Module)]

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Return" "(" Expr ")"                         [symbol(Return)]
                | "If" "(" Expr "," Stmts "," Stmts ")"       [symbol(If)]
                | "Expr" "(" Expr ")"                           [symbol(ExprStmt)]

  syntax Params ::= "Params" "(" String ")" [symbol(Params)]

  syntax Expr ::= "Int" "(" Int ")"                            [symbol(IntExpr)]
                | "Str" "(" String ")"                          [symbol(StrExpr)]
                | "Name" "(" String ")"                         [symbol(NameExpr)]
                | "BinOp" "(" String "," Expr "," Expr ")"    [symbol(BinOp)]
                | "Compare" "(" Expr "," CmpOp ")"             [symbol(Compare)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports MAP

  syntax FunctionValue ::= "noFunction"
                         | "function" "(" String "," String "," Stmts ")"
  syntax Control ::= "normal" | "returned"
  syntax Result ::= "noResult" | "result" "(" Int ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "entry" "(" String "," Int ")"
                 | "endCall"

  configuration
    <mpy>
      <k> $PGM:Pgm ~> entry("starts_one_ends", $N:Int) </k>
      <function> noFunction </function>
      <env> .Map </env>
      <control> normal </control>
      <result> noResult </result>
    </mpy>

  // Module evaluation registers top-level functions before the configured
  // entry call is made.
  rule <k> Module(SS) => exec(SS) ... </k>
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>
       <control> normal </control>
  rule <k> exec(_SS) => .K ... </k>
       <control> returned </control>

  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <function> _ => function(F, P, BODY) </function>

  rule <k> entry(F, N) => exec(BODY) ~> endCall ... </k>
       <function> function(F, P, BODY) </function>
       <env> _ => P |-> N </env>
       <control> normal </control>
       <result> noResult </result>

  rule <k> endCall => .K ... </k>
       <control> returned => normal </control>

  // A standalone expression (the function docstring here) has no externally
  // observable effect in this integer-only fragment.
  rule <k> Expr(_E) => .K ... </k>

  rule <k> If(COND, THEN, _ELSE) => exec(THEN) ... </k>
       <env> ENV </env>
    requires evalBool(COND, ENV)
  rule <k> If(COND, _THEN, ELSE) => exec(ELSE) ... </k>
       <env> ENV </env>
    requires notBool evalBool(COND, ENV)

  rule <k> Return(E) => .K ... </k>
       <env> ENV </env>
       <control> normal => returned </control>
       <result> noResult => result(evalInt(E, ENV)) </result>

  // Pure expression semantics.  Keeping this layer independent of statement
  // control makes it directly simplifiable in both execution and proofs.
  syntax Int ::= evalInt(Expr, Map) [function]
  rule evalInt(Int(I), _ENV) => I
  rule evalInt(Name(X), (X |-> I) M) => I
    requires notBool (X in_keys(M))
  rule evalInt(BinOp("+", A, B), ENV) => evalInt(A, ENV) +Int evalInt(B, ENV)
  rule evalInt(BinOp("-", A, B), ENV) => evalInt(A, ENV) -Int evalInt(B, ENV)
  rule evalInt(BinOp("*", A, B), ENV) => evalInt(A, ENV) *Int evalInt(B, ENV)
  rule evalInt(BinOp("**", A, B), ENV) => evalInt(A, ENV) ^Int evalInt(B, ENV)

  syntax Bool ::= evalBool(Expr, Map) [function]
  rule evalBool(Compare(A, CmpOp("==", B)), ENV)
    => evalInt(A, ENV) ==Int evalInt(B, ENV)
endmodule
