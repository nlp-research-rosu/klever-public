module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The constructors emitted by py2mpy.py for this program.  Statement and
  // comprehension lists use juxtaposition, exactly as the translator does.
  syntax Module ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "ListExpr" "(" Exprs ")"
                | "Call" "(" Expr "," Exprs ")"
                | "ListComp" "(" Expr "," CompFors ")"
  syntax Exprs ::= List{Expr, ","}
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  syntax CompFors ::= List{CompFor, ""}

  // Runtime values are deliberately distinct from source expressions.
  // VBool is an instance of int in Python, a detail captured by isInt below.
  syntax PyVal ::= "VInt" "(" Int ")"
                 | "VBool" "(" Bool ")"
                 | "VString" "(" String ")"
                 | "VFloat" "(" String ")"
                 | "VList" "(" PyVals ")"
                 | "VDict"
                 | "VNone"
                 | "VOpaque" "(" String ")"
  syntax PyVals ::= List{PyVal, ","}
endmodule

module MPY
  imports MPY-SYNTAX
  imports STRING

  syntax RuntimeFunction ::= "function" "(" String "," Stmts ")"
  syntax Functions ::= ".Functions"
                     | "bindFunction" "(" String "," RuntimeFunction "," Functions ")"
  syntax Env ::= ".Env"
               | "bind" "(" String "," PyVal "," Env ")"
  syntax Result ::= "noResult"
                  | "result" "(" PyVal ")"

  syntax KItem ::= "bootstrap"
                 | "load" "(" Stmts ")"
                 | "invoke" "(" String "," PyVal ")"
                 | "exec" "(" Stmts ")"
                 | "finish" "(" PyVal ")"

  configuration
    <mpy>
      <k> bootstrap ~> invoke("filter_integers", $INPUT:PyVal) </k>
      <program> $PGM:Module </program>
      <functions> .Functions </functions>
      <env> .Env </env>
      <return> noResult </return>
    </mpy>

  rule <k> bootstrap => load(SS) ... </k>
       <program> Module(SS) </program>

  rule <k> load(.Stmts) => .K ... </k>
  rule <k> load(ImportFrom(_, _) SS) => load(SS) ... </k>
  rule <k> load(FuncDef(F, Params(P), BODY) SS) => load(SS) ... </k>
       <functions> FUNS => bindFunction(F, function(P, BODY), FUNS) </functions>

  rule <k> invoke(F, V) => exec(BODY) ... </k>
       <functions> bindFunction(F, function(P, BODY), _) </functions>
       <env> _ => bind(P, V, .Env) </env>

  rule <k> exec(Return(E)) => finish(eval(E, ENV)) ... </k>
       <env> ENV </env>

  rule <k> finish(V) => .K ... </k>
       <return> _ => result(V) </return>

  syntax PyVal ::= eval(Expr, Env) [function]
  rule eval(Int(I), _) => VInt(I)
  rule eval(Bool(B), _) => VBool(B)
  rule eval(Str(S), _) => VString(S)
  rule eval(Name(X), bind(X, V, _)) => V
  rule eval(Name(X), bind(Y, _, ENV)) => eval(Name(X), ENV)
    requires X =/=String Y
  rule eval(ListExpr(.Exprs), _) => VList(.PyVals)
  rule eval(Call(Name("isinstance"), E, Name("int")), ENV)
    => VBool(pythonIsInteger(eval(E, ENV)))
  rule eval(ListComp(E, CompFor(Name(X), ITER, COND)), ENV)
    => comprehend(eval(ITER, ENV), X, E, COND, ENV)

  syntax Bool ::= pythonIsInteger(PyVal) [function, total]
  rule pythonIsInteger(VInt(_)) => true
  rule pythonIsInteger(VBool(_)) => true
  rule pythonIsInteger(_) => false [owise]

  syntax PyVal ::= comprehend(PyVal, String, Expr, Expr, Env)
                   [function]
  rule comprehend(VList(.PyVals), _, _, _, _) => VList(.PyVals)
  rule comprehend(VList(V, VS), X, E, C, ENV)
    => keepIf(eval(C, bind(X, V, ENV)),
              eval(E, bind(X, V, ENV)),
              comprehend(VList(VS), X, E, C, ENV))

  syntax PyVal ::= keepIf(PyVal, PyVal, PyVal) [function]
  rule keepIf(VBool(true), V, TAIL) => prepend(V, TAIL)
  rule keepIf(VBool(false), _, TAIL) => TAIL

  // Prepending is kept separate so symbolic proofs can expose one filtering
  // step without first having to evaluate an arbitrary list tail.
  syntax PyVal ::= prepend(PyVal, PyVal) [function]
  rule prepend(V, VList(VS)) => VList(V, VS)
endmodule
