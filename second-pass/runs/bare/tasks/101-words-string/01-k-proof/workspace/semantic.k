requires "verification.k"

module SEMANTIC-SYNTAX
  imports STRING-SYNTAX

  // The concrete syntax emitted by py2mpy.py for the subset used here.
  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Ids    ::= List{String, ","}
  syntax Params ::= "Params" "(" Ids ")"
  syntax Exprs  ::= List{Expr, ","}
  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports VERIFICATION
  imports MAP

  syntax Function ::= function(String, Stmts)
  syntax PyVal ::= StrVal(String) | ListVal(List)

  syntax KItem ::= invoke(String, String)
                 | execute(Stmts, Map)

  syntax PyVal ::= eval(Expr, Map) [function]
  syntax String ::= asString(PyVal) [function]

  configuration
    <k> $PGM:Program ~> invoke("words_string", $INPUT:String) </k>
    <functions> .Map </functions>

  // Loading a module installs its (single, capture-free) function definition.
  rule <k> Module(FuncDef(F, Params(P), BODY)) => .K ... </k>
       <functions> .Map => F |-> function(P, BODY) </functions>

  // Invocation creates a fresh one-variable local environment.
  rule <k> invoke(F, S) => execute(BODY, P |-> StrVal(S)) ... </k>
       <functions>... F |-> function(P, BODY) ...</functions>

  rule <k> execute(Return(E), ENV) => eval(E, ENV) ... </k>

  rule eval(Name(X), X |-> V:PyVal) => V
  rule eval(Str(S), _) => StrVal(S)

  // Python str.replace(old, new) with no count replaces every occurrence.
  rule eval(Call(Attribute(RECV, "replace"), Str(OLD), Str(NEW)), ENV)
    => StrVal(replaceAll(asString(eval(RECV, ENV)), OLD, NEW))

  // Python str.split() without an explicit separator returns maximal words.
  rule eval(Call(Attribute(RECV, "split"), .Exprs), ENV)
    => ListVal(splitSpaces(asString(eval(RECV, ENV))))

  rule asString(StrVal(S)) => S
endmodule
