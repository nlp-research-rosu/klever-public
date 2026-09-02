requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= Module(Stmts)
  syntax Stmt ::= FuncDef(String, Params, Stmts)
                | Return(Expr)
  syntax Stmts ::= List{Stmt, ""}

  syntax Params ::= Params(Strings)
  syntax Strings ::= List{String, ","}

  syntax Expr ::= Int(Int)
                | Name(String)
                | ListExpr(Exprs)
                | Call(Expr, Exprs)
  syntax Exprs ::= List{Expr, ","}
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports LIST

  syntax Val ::= VInt(Int)
               | VList(List)
               | VSet(List)

  // Function application and expression evaluation for the source subset used
  // by solution.py. VSet is an abstract set value: its list representation is
  // observable only through sorted(), which canonicalizes it.
  syntax Val ::= apply(Program, Val) [function]
  rule apply(Module(FuncDef(_F, Params(X), Return(E))), V)
    => eval(E, X, V)

  syntax Val ::= eval(Expr, String, Val) [function]
  rule eval(Int(I), _, _) => VInt(I)
  rule eval(Name(X), X, V) => V
  rule eval(ListExpr(ES), X, V) => VList(evalExprs(ES, X, V))
  rule eval(Call(Name("set"), E), X, V) => makeSet(eval(E, X, V))
  rule eval(Call(Name("sorted"), E), X, V) => sortSet(eval(E, X, V))

  syntax List ::= evalExprs(Exprs, String, Val) [function]
  rule evalExprs(.Exprs, _, _) => .List
  rule evalExprs(E:Expr, X, V) => ListItem(eval(E, X, V))
  rule evalExprs((E:Expr, ES:Exprs), X, V)
    => ListItem(eval(E, X, V)) evalExprs(ES, X, V)

  syntax Val ::= makeSet(Val) [function]
               | sortSet(Val) [function]
  rule makeSet(VList(L)) => VSet(dedupInts(L))
  rule sortSet(VSet(L)) => VList(sortInts(L))

  syntax List ::= dedupInts(List) [function]
  rule dedupInts(.List) => .List
  rule dedupInts(ListItem(VInt(I)) REST)
    => ListItem(VInt(I)) dedupInts(removeInt(I, REST))

  syntax List ::= removeInt(Int, List) [function]
  rule removeInt(_, .List) => .List
  rule removeInt(I, ListItem(VInt(I)) REST) => removeInt(I, REST)
  rule removeInt(I, ListItem(VInt(J)) REST)
    => ListItem(VInt(J)) removeInt(I, REST)
    requires I =/=Int J

  syntax List ::= sortInts(List) [function]
  rule sortInts(.List) => .List
  rule sortInts(ListItem(VInt(I)) REST)
    => insertInt(I, sortInts(REST))

  syntax List ::= insertInt(Int, List) [function]
  rule insertInt(I, .List) => ListItem(VInt(I))
  rule insertInt(I, ListItem(VInt(J)) REST)
    => ListItem(VInt(I)) ListItem(VInt(J)) REST
    requires I <=Int J
  rule insertInt(I, ListItem(VInt(J)) REST)
    => ListItem(VInt(J)) insertInt(I, REST)
    requires I >Int J

  syntax Val ::= run(Program, Expr) [function]
  rule run(P, ARG) => apply(P, eval(ARG, "", VList(.List)))

  configuration <k> run($PGM:Program, $ARGS:Expr) </k>
endmodule
