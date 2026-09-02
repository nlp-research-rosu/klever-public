module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= Module ( Stmts )
                   | Run ( Program , Expr )

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}

  syntax Params ::= Params ( Strings )
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= FuncDef ( String , Params , Stmts )
                | Assign ( Expr , Expr )
                | AugAssign ( Expr , String , Expr )
                | If ( Expr , Stmts , Stmts )
                | For ( Expr , Expr , Stmts )
                | While ( Expr , Stmts )
                | Return ( Expr )

  syntax Expr ::= Int ( Int )
                | Bool ( Bool )
                | Name ( String )
                | ListExpr ( Exprs )
                | BinOp ( String , Expr , Expr )
                | Compare ( Expr , CmpOp )
                | Call ( Expr , Expr )

  syntax CmpOp ::= CmpOp ( String , Expr )
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Value ::= intVal ( Int )
                 | boolVal ( Bool )
                 | listVal ( Values )
                 | "none"
  syntax Values ::= List{Value, ","}
  syntax Function ::= function ( String , Stmts )

  syntax KItem ::= exec ( Stmts )
                 | "moduleDone"
                 | collectHead ( Exprs )
                 | prepend ( Value )
                 | assignTo ( String )
                 | augment ( String , String )
                 | binLeft ( String , Expr )
                 | binRight ( String , Value )
                 | cmpLeft ( String , Expr )
                 | cmpRight ( String , Value )
                 | branch ( Stmts , Stmts )
                 | startFor ( String , Stmts )
                 | setLocal ( String , Value )
                 | loopFor ( String , Value , Stmts )
                 | whileTest ( Expr , Stmts )
                 | invoke ( String )
                 | "makeReturn"
                 | returnScan ( Value )
                 | "implicitReturn"
                 | restoreEnv ( Map )

  syntax Value ::= #bin ( String , Value , Value ) [function, total]
                 | #cmp ( String , Value , Value ) [function, total]

  configuration
    <py>
      <k> $PGM:Program </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>

  rule <k> Run(P, E) => P ~> E ... </k>
  rule <k> Module(SS) => exec(SS) ~> moduleDone ... </k>
  rule <k> moduleDone => .K ... </k>

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => S ~> exec(SS)

  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>

  rule Int(I) => intVal(I)
  rule Bool(B) => boolVal(B)
  rule <k> Name(X) => V ... </k> <env> ... X |-> V ... </env>

  rule ListExpr(.Exprs) => listVal(.Values)
  rule ListExpr(E:Expr) => E ~> collectHead(.Exprs)
  rule ListExpr(E:Expr, ES:Exprs) => E ~> collectHead(ES)
  rule V:Value ~> collectHead(ES) => ListExpr(ES) ~> prepend(V)
  rule listVal(VS) ~> prepend(V) => listVal(V, VS)

  rule Assign(Name(X), E) => E ~> assignTo(X)
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule AugAssign(Name(X), OP, E) => E ~> augment(X, OP)
  rule <k> V:Value ~> augment(X, OP) => .K ... </k>
       <env> (X |-> OLD) REST => (X |-> #bin(OP, OLD, V)) REST </env>

  rule BinOp(OP, L, R) => L ~> binLeft(OP, R)
  rule V:Value ~> binLeft(OP, R) => R ~> binRight(OP, V)
  rule V2:Value ~> binRight(OP, V1) => #bin(OP, V1, V2)

  rule #bin("+",  intVal(A), intVal(B)) => intVal(A +Int B)
  rule #bin("//", intVal(A), intVal(B)) => intVal(A /Int B)
    requires B =/=Int 0
  rule #bin("%",  intVal(A), intVal(B)) => intVal(A %Int B)
    requires B =/=Int 0

  rule Compare(L, CmpOp(OP, R)) => L ~> cmpLeft(OP, R)
  rule V:Value ~> cmpLeft(OP, R) => R ~> cmpRight(OP, V)
  rule V2:Value ~> cmpRight(OP, V1) => #cmp(OP, V1, V2)

  rule #cmp(">",  intVal(A), intVal(B)) => boolVal(A >Int B)
  rule #cmp(">=", intVal(A), intVal(B)) => boolVal(A >=Int B)
  rule #cmp("==", intVal(A), intVal(B)) => boolVal(A ==Int B)

  rule If(COND, YES, NO) => COND ~> branch(YES, NO)
  rule boolVal(true)  ~> branch(YES, _) => exec(YES)
  rule boolVal(false) ~> branch(_, NO)  => exec(NO)

  rule For(Name(X), ITER, BODY) => ITER ~> startFor(X, BODY)
  rule listVal(VS) ~> startFor(X, BODY) => loopFor(X, listVal(VS), BODY)
  rule <k> setLocal(X, V) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>
  rule loopFor(_, listVal(.Values), _) => .K
  rule loopFor(X, listVal(V, VS), BODY)
    => setLocal(X, V) ~> exec(BODY) ~> loopFor(X, listVal(VS), BODY)

  rule While(COND, BODY) => COND ~> whileTest(COND, BODY)
  rule boolVal(true)  ~> whileTest(COND, BODY)
    => exec(BODY) ~> While(COND, BODY)
  rule boolVal(false) ~> whileTest(_, _) => .K

  rule Call(Name(F), ARG) => ARG ~> invoke(F)
  rule <k> V:Value ~> invoke(F)
        => exec(BODY) ~> implicitReturn ~> restoreEnv(RHO) ... </k>
       <functions> ... F |-> function(P, BODY) ... </functions>
       <env> RHO => P |-> V </env>

  rule Return(E) => E ~> makeReturn
  rule V:Value ~> makeReturn => returnScan(V)
  rule returnScan(V) ~> implicitReturn => V
  rule returnScan(V) ~> _:KItem => returnScan(V) [owise]
  rule implicitReturn => none
  rule <k> V:Value ~> restoreEnv(RHO) => V ... </k>
       <env> _ => RHO </env>
endmodule
