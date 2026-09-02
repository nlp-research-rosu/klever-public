module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The concrete constructors emitted by py2mpy.py for this solution.
  syntax Pgm ::= "Module" "(" Stmt ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= Value
                | "Name" "(" String ")"
                | "Call" "(" Expr "," Expr ")"

  syntax Value ::= "Str" "(" String ")"
                 | "Int" "(" Int ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports MAP
  imports INT
  imports STRING

  syntax KItem ::= "invoke" "(" String "," Value ")"
                 | "callLen"
                 | "finishReturn"
  syntax Function ::= "function" "(" String "," Stmt ")"
  syntax Result ::= "noResult" | Value

  configuration
    <py>
      <k> $PGM:Pgm ~> invoke("strlen", Str($INPUT:String)) </k>
      <functions> .Map </functions>
      <locals> .Map </locals>
      <result> noResult </result>
    </py>

  // Loading a module installs its top-level function definition.
  rule <k> Module(S:Stmt) => S ... </k>
  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <functions> FUNCTIONS => FUNCTIONS [ F <- function(P, BODY) ] </functions>

  // Calling a user function binds its sole formal parameter.
  rule <k> invoke(F, V) => BODY ... </k>
       <functions> ... F |-> function(P, BODY) ... </functions>
       <locals> _ => P |-> V </locals>

  // Expressions needed by strlen.
  rule <k> Name(X) => V ... </k>
       <locals> ... X |-> V ... </locals>
  rule <k> Call(Name("len"), E) => E ~> callLen ... </k>
  rule <k> Str(S) ~> callLen => Int(lengthString(S)) ... </k>

  // A return evaluates its expression, then exposes the value as the result.
  rule <k> Return(E) => E ~> finishReturn ... </k>
  rule <k> V:Value ~> finishReturn => .K ... </k>
       <result> _ => V </result>
endmodule
