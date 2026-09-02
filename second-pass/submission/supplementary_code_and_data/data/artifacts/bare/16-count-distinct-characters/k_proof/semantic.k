// A deliberately small semantics for the py2mpy constructors exercised by
// solution.mpy.  Values are explicit, so AST constructors are never confused
// with evaluated Python values.

module MPY-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt  ::= "FuncDef" "(" String "," Params "," Stmts ")"
                 | "Return" "(" Expr ")"

  syntax Params  ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
  syntax Exprs ::= List{Expr, ","}
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports SET
  imports MAP

  syntax Value ::= StrVal(String)
                 | SetVal(Set)
                 | IntVal(Int)
  syntax Result ::= "noResult" | Value
  syntax KResult ::= Value

  syntax KItem ::= "#lower"
                 | "#set"
                 | "#len"
                 | "#finish"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <env> .Map </env>
      <input> $INPUT:String </input>
      <result> noResult </result>
    </mpy>

  // Loading this translated module binds its sole formal parameter to the
  // input configuration variable and starts executing the function body.
  rule <k> Module(FuncDef(F, Params(P, .Strings), BODY)) => BODY ... </k>
       <env> .Map => P |-> StrVal(S) </env>
       <input> S </input>
    requires F ==String "count_distinct_characters"

  rule <k> Return(E) .Stmts => E ~> #finish ... </k>

  rule <k> Name(X) => V ... </k>
       <env>... X |-> V ...</env>

  // Evaluate the receiver/argument before applying each primitive operation.
  rule <k> Call(Attribute(E, "lower"), .Exprs) => E ~> #lower ... </k>
  rule <k> StrVal(S) ~> #lower => StrVal(lowerString(S)) ... </k>

  rule <k> Call(Name("set"), E, .Exprs) => E ~> #set ... </k>
  rule <k> StrVal(S) ~> #set => SetVal(charsSet(S)) ... </k>

  rule <k> Call(Name("len"), E, .Exprs) => E ~> #len ... </k>
  rule <k> SetVal(S) ~> #len => IntVal(size(S)) ... </k>

  rule <k> IntVal(I) ~> #finish => .K </k>
       <result> noResult => IntVal(I) </result>

  // This task's string fragment gives lower() its ordinary case-insensitive
  // behavior for the Latin alphabet.  Non-capital code points are unchanged.
  // The recursive definition is also executable on concrete K strings.
  syntax String ::= lowerString(String) [function]
  rule lowerString("") => ""
  rule lowerString(S) =>
         lowerChar(substrString(S, 0, 1))
         +String lowerString(substrString(S, 1, lengthString(S)))
    requires S =/=String ""

  syntax String ::= lowerChar(String) [function]
  rule lowerChar(C) => chrChar(ordChar(C) +Int 32)
    requires 65 <=Int ordChar(C) andBool ordChar(C) <=Int 90
  rule lowerChar(C) => C [owise]

  // Python set(string) iterates through code points; native K sets provide
  // idempotence, so repeated characters disappear by construction.
  syntax Set ::= charsSet(String) [function]
  rule charsSet("") => .Set
  rule charsSet(S) =>
         SetItem(substrString(S, 0, 1))
         |Set charsSet(substrString(S, 1, lengthString(S)))
    requires S =/=String ""
endmodule
