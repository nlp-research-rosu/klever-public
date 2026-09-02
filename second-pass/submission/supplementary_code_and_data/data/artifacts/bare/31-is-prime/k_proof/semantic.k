module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= Module(Stmts)

  // The translator represents statement blocks by juxtaposition.
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= FuncDef(String, Params, Stmts)
                | Return(Expr)
                | If(Expr, Stmts, Stmts)

  syntax Params ::= Params(Ids)
  syntax Ids ::= List{String, ","}

  syntax Expr ::= Int(Int)
                | Bool(Bool)
                | Name(String)
                | BinOp(String, Expr, Expr)
                | Compare(Expr, CmpOp)
                | Call(Expr, Exprs)
  syntax CmpOp ::= CmpOp(String, Expr)
  syntax Exprs ::= List{Expr, ","}
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports MAP
  imports INT
  imports BOOL

  syntax Function ::= function(Params, Stmts)

  syntax KItem ::= #invoke(String, Exprs)
                 | #branch(Expr, Stmts, Stmts)
                 | #finish(Expr)

  syntax Expr ::= #eval(Expr, Map) [function]
                | #lookup(String, Map) [function]
                | #bin(String, Expr, Expr) [function]
                | #cmp(String, Expr, Expr) [function]
  syntax Exprs ::= #evalArgs(Exprs, Map) [function]
  syntax Map ::= #bind(Params, Exprs) [function]

  configuration
    <py>
      <k> $PGM:Program ~> #invoke("is_prime", Int($N:Int)) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> Bool(false) </result>
    </py>

  rule <k> Module(SS) => SS ... </k>

  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> FuncDef(F, P, B) => .K ... </k>
       <functions> FS => FS [ F <- function(P, B) ] </functions>

  rule <k> #invoke(F, VS) => B ... </k>
       <functions> ... F |-> function(P, B) ... </functions>
       <env> _ => #bind(P, VS) </env>

  rule <k> If(E, THEN, ELSE) => #branch(#eval(E, RHO), THEN, ELSE) ... </k>
       <env> RHO </env>
  rule <k> #branch(Bool(true),  THEN, _) => THEN ... </k>
  rule <k> #branch(Bool(false), _, ELSE) => ELSE ... </k>

  // Calls in solution.py are tail calls.  Return discards the rest of the
  // current block, exactly as Python does.
  rule <k> Return(Call(Name(F), ES)) ~> _ => #invoke(F, #evalArgs(ES, RHO)) </k>
       <env> RHO </env> [priority(40)]
  rule <k> Return(E) ~> _ => #finish(#eval(E, RHO)) </k>
       <env> RHO </env>
  rule <k> #finish(V) => .K </k>
       <result> _ => V </result>

  rule #lookup(X, (X |-> V:Expr) _REST) => V

  rule #eval(Int(I),    _)   => Int(I)
  rule #eval(Bool(B),   _)   => Bool(B)
  rule #eval(Name(X),   RHO) => #lookup(X, RHO)
  rule #eval(BinOp(OP, L, R), RHO)
    => #bin(OP, #eval(L, RHO), #eval(R, RHO))
  rule #eval(Compare(L, CmpOp(OP, R)), RHO)
    => #cmp(OP, #eval(L, RHO), #eval(R, RHO))

  rule #bin("+", Int(I), Int(J)) => Int(I +Int J)
  rule #bin("*", Int(I), Int(J)) => Int(I *Int J)
  rule #bin("%", Int(I), Int(J)) => Int(I %Int J)
    requires J =/=Int 0

  rule #cmp("<",  Int(I), Int(J)) => Bool(I <Int J)
  rule #cmp(">",  Int(I), Int(J)) => Bool(I >Int J)
  rule #cmp("==", Int(I), Int(J)) => Bool(I ==Int J)

  rule #evalArgs((E:Expr), RHO) => #eval(E, RHO)
  rule #evalArgs((E1:Expr, E2:Expr), RHO)
    => (#eval(E1, RHO), #eval(E2, RHO))

  rule #bind(Params(X:String), V:Expr) => X |-> V
  rule #bind(Params(X:String, Y:String), (V1:Expr, V2:Expr))
    => X |-> V1 Y |-> V2
endmodule
