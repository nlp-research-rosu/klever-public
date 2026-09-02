requires "verification.k"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // Concrete string lists used both for inputs and Python list values.
  syntax StrList ::= "nil"
                   | "cons" "(" String "," StrList ")"

  syntax Module ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Expr" "(" Expr ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= Val
                | "Name" "(" String ")"
                | "ListExpr" "(" ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Expr ")"

  syntax Val ::= "strVal" "(" String ")"
               | "listVal" "(" StrList ")"
               | "boolVal" "(" Bool ")"
               | "noneVal"
               | "boundString" "(" String "," String ")"
               | "boundRef" "(" String "," String ")"

  syntax Function ::= "function" "(" Params "," Stmts ")"
  syntax Output ::= "noOutput" | Val
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports MAP-SYMBOLIC

  configuration
    <t>
      <k> $PGM:Module </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <input> $INPUT:StrList </input>
      <prefix> $PREFIX:String </prefix>
      <output> noOutput </output>
    </t>

  syntax KItem ::= "launch"
                 | "assignTo" "(" String ")"
                 | "startFor" "(" String "," Stmts ")"
                 | "loop" "(" String "," Stmts "," StrList ")"
                 | "choose" "(" Stmts "," Stmts ")"
                 | "discard"
                 | "bindStartsWith"
                 | "callArg" "(" Expr ")"
                 | "apply" "(" Val ")"
                 | "doReturn"
                 | "functionEnd"

  syntax StrList ::= appendOne(StrList, String) [function]
  rule appendOne(nil, S) => cons(S, nil)
  rule appendOne(cons(H, T), S) => cons(H, appendOne(T, S))

  syntax Bool ::= startsWith(String, String) [function, total]
  rule startsWith(S, P) => false
       requires lengthString(P) >Int lengthString(S)
  rule startsWith(S, P) => substrString(S, 0, lengthString(P)) ==String P
       requires lengthString(P) <=Int lengthString(S)

  // Load a translated module, ignore the type-only import, and register defs.
  rule <k> Module(SS) => SS ~> launch ...</k>
  rule <k> (S:Stmt SS:Stmts) => S ~> SS ...</k>
  rule <k> .Stmts => .K ...</k>
  rule <k> ImportFrom(_, _) => .K ...</k>
  rule <k> FuncDef(F, PS, BODY) => .K ...</k>
       <functions> FUNS => FUNS [ F <- function(PS, BODY) ] </functions>

  // The task entry point has two positional arguments: a string list and prefix.
  rule <k> launch => BODY ~> functionEnd ...</k>
       <functions> ... "filter_by_prefix" |-> function(Params(P1:String, P2:String, .Strings), BODY) ...</functions>
       <input> IN </input>
       <prefix> PRE </prefix>
       <env> ENV => (ENV [ P1 <- listVal(IN) ]) [ P2 <- strVal(PRE) ] </env>

  // Expressions and calls required by the translated implementation.
  rule <k> Name(X) => ENV [ X ] ...</k>
       <env> ENV </env>
  rule <k> ListExpr() => listVal(nil) ...</k>
  rule <k> Attribute(Name(X), "startswith") => ENV [ X ] ~> bindStartsWith ...</k>
       <env> ENV </env>
  rule <k> strVal(S) ~> bindStartsWith => boundString(S, "startswith") ...</k>
  rule <k> Attribute(Name(X), "append") => boundRef(X, "append") ...</k>
  rule <k> Call(F, A) => F ~> callArg(A) ...</k>
  rule <k> V:Val ~> callArg(A) => A ~> apply(V) ...</k>
  rule <k> strVal(P) ~> apply(boundString(S, "startswith"))
        => boolVal(startsWith(S, P)) ...</k>
  rule <k> strVal(S) ~> apply(boundRef(X, "append")) => noneVal ...</k>
       <env> ... X |-> (listVal(L) => listVal(appendOne(L, S))) ...</env>

  // Statements, sequencing, and loop control.
  rule <k> Assign(Name(X), E) => E ~> assignTo(X) ...</k>
  rule <k> V:Val ~> assignTo(X) => .K ...</k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> For(Name(X), E, BODY) => E ~> startFor(X, BODY) ...</k>
  rule <k> listVal(L) ~> startFor(X, BODY) => loop(X, BODY, L) ...</k>
  rule <k> loop(_, _, nil) => .K ...</k>
  rule <k> loop(X, BODY, cons(H, T)) => BODY ~> loop(X, BODY, T) ...</k>
       <env> ENV => ENV [ X <- strVal(H) ] </env>

  rule <k> If(E, THEN, ELSE) => E ~> choose(THEN, ELSE) ...</k>
  rule <k> boolVal(B) ~> choose(THEN, _) => THEN ...</k>
       requires B ==Bool true
  rule <k> boolVal(B) ~> choose(_, ELSE) => ELSE ...</k>
       requires B ==Bool false

  rule <k> Expr(E) => E ~> discard ...</k>
  rule <k> _:Val ~> discard => .K ...</k>

  rule <k> Return(E) => E ~> doReturn ...</k>
  rule <k> V:Val ~> doReturn ~> _REST => .K </k>
       <output> _ => V </output>
  rule <k> functionEnd => .K ...</k>
       <output> noOutput => noneVal </output>
endmodule

module SEMANTIC
  imports MPY
  imports VERIFICATION
endmodule
