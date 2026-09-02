module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The concrete constructor syntax emitted by py2mpy.py for the subset used
  // by solution.py.  Statement lists use juxtaposition, exactly as the
  // translator prints them.
  syntax Pgm    ::= "Module" "(" Stmts ")"                     [symbol(Module)]
  syntax Params ::= "Params" "(" String ")"                    [symbol(Params)]
  syntax Expr   ::= "Int" "(" Int ")"                          [symbol(IntExpr)]
                  | "Name" "(" String ")"                      [symbol(Name)]
                  | "BinOp" "(" String "," Expr "," Expr ")" [symbol(BinOp)]
                  | "Compare" "(" Expr "," CmpOp ")"          [symbol(Compare)]
  syntax CmpOp  ::= "CmpOp" "(" String "," Expr ")"           [symbol(CmpOp)]
  syntax Stmt   ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                  | "Assign" "(" Expr "," Expr ")"             [symbol(Assign)]
                  | "While" "(" Expr "," Stmts ")"             [symbol(While)]
                  | "If" "(" Expr "," Stmts "," Stmts ")"      [symbol(If)]
                  | "Return" "(" Expr ")"                       [symbol(Return)]
  syntax Stmts ::= List{Stmt, ""}
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports MAP

  syntax KItem ::= "noResult"

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <arg> $ARG:Int </arg>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  // Environment lookup and expression evaluation are semantic functions.
  syntax Int ::= envInt(Map, String) [function]
  rule envInt(ENV, X) => {ENV [ X ]}:>Int

  syntax Int ::= evalInt(Expr, Map) [function]
  rule evalInt(Int(I),             _)   => I
  rule evalInt(Name(X),            ENV) => envInt(ENV, X)
  rule evalInt(BinOp("-", A, B),   ENV) => evalInt(A, ENV) -Int  evalInt(B, ENV)
  rule evalInt(BinOp("%", A, B),   ENV) => evalInt(A, ENV) modInt evalInt(B, ENV)

  syntax Bool ::= evalBool(Expr, Map) [function]
  rule evalBool(Compare(A, CmpOp("!=", B)), ENV)
    => evalInt(A, ENV) =/=Int evalInt(B, ENV)
  rule evalBool(Compare(A, CmpOp("==", B)), ENV)
    => evalInt(A, ENV) ==Int evalInt(B, ENV)
  rule evalBool(Compare(A, CmpOp(">", B)), ENV)
    => evalInt(A, ENV) >Int evalInt(B, ENV)

  // A module containing one entry point is invoked with the configured
  // integer argument.  The remaining rules are ordinary small-step rules.
  rule <k> Module(FuncDef(_, Params(P), BODY)) => BODY ... </k>
       <arg> N </arg>
       <env> .Map => P |-> N </env>

  rule <k> S:Stmt REST:Stmts => S ~> REST ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> ENV => ENV [ X <- evalInt(E, ENV) ] </env>

  // Keep the recursive loop marker in K (rather than appending it to BODY's
  // list).  This makes list cleanup happen before the next test and exposes a
  // stable loop-head configuration for invariant proofs.
  syntax KItem ::= "whileBranch" "(" Expr "," Stmts ")"
  rule <k> While(COND, BODY) => evalBool(COND, ENV) ~> whileBranch(COND, BODY) ... </k>
       <env> ENV </env>
  rule <k> true  ~> whileBranch(COND, BODY) => BODY ~> While(COND, BODY) ... </k>
  rule <k> false ~> whileBranch(_, _) => .K ... </k>

  syntax KItem ::= "branch" "(" Stmts "," Stmts ")"
  rule <k> If(COND, THEN, ELSE) => evalBool(COND, ENV) ~> branch(THEN, ELSE) ... </k>
       <env> ENV </env>
  rule <k> true  ~> branch(THEN, _) => THEN ... </k>
  rule <k> false ~> branch(_, ELSE) => ELSE ... </k>

  rule <k> Return(E) ~> _:K => .K </k>
       <env> ENV </env>
       <result> noResult => evalInt(E, ENV) </result>
endmodule
