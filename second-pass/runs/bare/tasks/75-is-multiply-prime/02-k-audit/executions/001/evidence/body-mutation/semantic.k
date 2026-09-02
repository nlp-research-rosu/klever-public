requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // Concrete syntax emitted by py2mpy.py for the subset used by solution.py.
  syntax Pgm
  syntax Stmt
  syntax Expr
  syntax Params
  syntax CmpOp
  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}
  syntax Strings ::= List{String, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Pgm ::= "Module" "(" Stmts ")"
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
  syntax Params ::= "Params" "(" Strings ")"
  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "BoolOp" "(" String "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports MAP
  imports INT
  imports BOOL

  syntax Result ::= "noResult" | Expr
  syntax KItem ::= "execute" "(" Stmts ")"

  // Big-step expression evaluators.  The rules implement Python equality and
  // short-circuit `or` for the expression forms present in the translated AST.
  syntax Bool ::= evalBool(Expr, Map) [function]
  syntax Bool ::= evalOr(Exprs, Map) [function]

  rule evalBool(Bool(B), _) => B
  rule evalBool(
         Compare(Name(X), (CmpOp("==", Int(I)), .CmpOps)),
         X |-> Int(A))
    => A ==Int I
  rule evalBool(BoolOp("or", ES), ENV) => evalOr(ES, ENV)

  rule evalOr(.Exprs, _) => false
  rule evalOr((E:Expr, ES:Exprs), ENV)
    => evalBool(E, ENV) orElseBool evalOr(ES, ENV)

  configuration
    <k> $PGM:Pgm </k>
    <arg> $ARG:Int </arg>
    <env> .Map </env>
    <result> noResult </result>

  // The task has one module-level, unary entry point.  Loading the module binds
  // its formal to the supplied <arg> and executes its body.
  rule <k> Module(FuncDef(_F, Params(P:String), BODY)) => execute(BODY) </k>
       <arg> A </arg>
       <env> .Map => P |-> Int(A) </env>

  rule <k> execute(Return(E)) => .K </k>
       <env> ENV => .Map </env>
       <result> noResult => Bool(evalBool(E, ENV)) </result>
endmodule
