module MPY-SYNTAX
  imports STRING-SYNTAX

  // The source grammar is intentionally the executable py2mpy fragment used
  // by solution.mpy.  Every constructor below is emitted directly from the
  // corresponding CPython AST node; no source-level desugaring is assumed.
  syntax Program ::= "Module" "(" FunctionDef ")"
  syntax FunctionDef ::= "FuncDef" "(" String "," Params "," Stmt ")"
  syntax Params ::= "Params" "(" String ")"

  syntax Stmt ::= "Return" "(" Expr ")"

  syntax Expr ::= "Name"      "(" String ")"
                | "Str"       "(" String ")"
                | "BinOp"     "(" String "," Expr "," Expr ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call"      "(" Expr "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports MAP

  syntax Val ::= strVal(String)
               | intVal(Int)
               | countMethod(String)
  syntax Result ::= "noResult" | Val
  syntax KItem ::= "#invoke" "(" String "," String ")"

  // A minimal environment-based expression semantics.  Attribute evaluation
  // binds Python's str.count method to its receiver; Call then applies it.
  syntax Val ::= eval(Expr, Map) [function]
  syntax String ::= asString(Val) [function]
  syntax String ::= countReceiver(Val) [function]
  syntax Int ::= asInt(Val) [function]

  rule eval(Name(X), X |-> V) => V
  rule eval(Str(S), _) => strVal(S)
  rule eval(Attribute(E, "count"), ENV)
    => countMethod(asString(eval(E, ENV)))
  rule eval(Call(F, A), ENV)
    => intVal(countAllOccurrences(countReceiver(eval(F, ENV)),
                                  asString(eval(A, ENV))))
  rule eval(BinOp("+", L, R), ENV)
    => intVal(asInt(eval(L, ENV)) +Int asInt(eval(R, ENV)))

  rule asString(strVal(S)) => S
  rule countReceiver(countMethod(S)) => S
  rule asInt(intVal(I)) => I

  configuration
    <hexKey>
      <k> $PGM:Program ~> #invoke("hex_key", $INPUT:String) </k>
      <env> .Map </env>
      <result> noResult </result>
    </hexKey>

  // Loading a one-argument definition and invoking it establishes its local
  // environment.  Return evaluates the expression and terminates the frame.
  rule <k> Module(FuncDef(F, Params(P), BODY)) ~> #invoke(F, ARG)
        => BODY </k>
       <env> .Map => P |-> strVal(ARG) </env>

  rule <k> Return(E) => .K </k>
       <env> ENV </env>
       <result> noResult => eval(E, ENV) </result>
endmodule
