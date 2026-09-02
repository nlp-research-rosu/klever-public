requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports LIST
  imports MAP

  syntax Program ::= Module
                   | "Run" "(" Module "," "[" Ints "]" ")"

  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Expr" "(" Expr ")"
                | "Return" "(" Expr ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Ints ::= List{Int, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "ListExpr" "(" Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}

  // Runtime values are expressions so they can occupy evaluation positions.
  syntax Val ::= IntVal(Int) | BoolVal(Bool) | ListVal(List) | "NoneVal"
  syntax Expr ::= Val

  syntax Function ::= Function(Params, Stmts)
  syntax Frame ::= Frame(Map)

  syntax KItem ::= Invoke(String, Val)
                 | CallKont(String)
                 | "EndCall"
                 | "Cleanup"
                 | Store(String)
                 | "Discard"
                 | Branch(Stmts, Stmts)
                 | CompareRight(Expr)
                 | GreaterThan(Int)
                 | AppendTo(String)
                 | StartLoop(String, Stmts)
                 | Loop(String, Stmts, List)
                 | Bind(String, Val)

  syntax List ::= intsToList(Ints) [function, total]
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  configuration
    <py>
      <k> $PGM:Program </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <stack> .List </stack>
    </py>

  // The concrete command-line harness supplies a list of machine integers.
  rule intsToList(.Ints) => .List
  rule intsToList(I:Int) => ListItem(I)
  rule intsToList(I:Int, IS:Ints) => ListItem(I) intsToList(IS)

  rule <k> Run(M, [ IS ]) => M ~> Invoke("rolling_max", ListVal(intsToList(IS))) ~> Cleanup ... </k>
  rule <k> Module(SS) => SS ... </k>
  rule <k> S:Stmt SS:Stmts => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>
  rule <k> V:Val ~> .Stmts => V ... </k>

  rule <k> ImportFrom(_, _) => .K ... </k>
  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> FS => FS [ F <- Function(PS, BODY) ] </functions>

  // Calls use a fresh local environment and restore the caller at EndCall.
  rule <k> Call(Name(F), E:Expr, .Exprs) => E ~> CallKont(F) ... </k>
  rule <k> V:Val ~> CallKont(F) => Invoke(F, V) ... </k>
  rule <k> Invoke(F, V) => BODY ~> EndCall ... </k>
       <functions>... F |-> Function(Params(P:String, .Strings), BODY) ...</functions>
       <env> OLD => P |-> V </env>
       <stack> .List => ListItem(Frame(OLD)) </stack>
  rule <k> V:Val ~> EndCall => V ... </k>
       <env> _ => OLD </env>
       <stack> ListItem(Frame(OLD)) => .List </stack>

  rule <k> V:Val ~> Cleanup => V ... </k>
       <functions> _ => .Map </functions>

  // Literals and lookup.
  rule <k> Int(I) => IntVal(I) ... </k>
  rule <k> Bool(B) => BoolVal(B) ... </k>
  rule <k> ListExpr(.Exprs) => ListVal(.List) ... </k>
  rule <k> Name(X) => V ... </k> <env>... X |-> V ...</env>

  // Assignment, return, and expression statements.
  rule <k> Assign(Name(X), E) => E ~> Store(X) ... </k>
  rule <k> V:Val ~> Store(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>
  rule <k> Return(E) => E ... </k>
  rule <k> Expr(E) => E ~> Discard ... </k>
  rule <k> _:Val ~> Discard => .K ... </k>

  // The only comparison needed by the submitted program.
  rule <k> Compare(L, CmpOp(">", R), .CmpOps) => L ~> CompareRight(R) ... </k>
  rule <k> IntVal(I) ~> CompareRight(R) => R ~> GreaterThan(I) ... </k>
  rule <k> IntVal(J) ~> GreaterThan(I) => BoolVal(I >Int J) ... </k>

  // Conditionals evaluate their guard before selecting a statement block.
  rule <k> If(E, THEN, ELSE) => E ~> Branch(THEN, ELSE) ... </k>
  rule <k> BoolVal(true) ~> Branch(THEN, _) => THEN ... </k>
  rule <k> BoolVal(false) ~> Branch(_, ELSE) => ELSE ... </k>

  // list.append mutates the named list and evaluates to None.
  rule <k> Call(Attribute(Name(X), "append"), E:Expr, .Exprs) => E ~> AppendTo(X) ... </k>
  rule <k> IntVal(I) ~> AppendTo(X) => NoneVal ... </k>
       <env>... X |-> ListVal(ITEMS) => X |-> ListVal(ITEMS ListItem(I)) ...</env>

  // A for-loop binds each integer in order and executes its body sequentially.
  rule <k> For(Name(X), E, BODY) => E ~> StartLoop(X, BODY) ... </k>
  rule <k> ListVal(ITEMS) ~> StartLoop(X, BODY) => Loop(X, BODY, ITEMS) ... </k>
  rule <k> Loop(_, _, .List) => .K ... </k>
  rule <k> Loop(X, BODY, ListItem(I) REST) => Bind(X, IntVal(I)) ~> BODY ~> Loop(X, BODY, REST) ... </k>
  rule <k> Bind(X, V) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>
endmodule
