requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "ListExpr" "(" ")"
                | "ListExpr" "(" Expr "," Expr ")"
                | "Call" "(" Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Subscript" "(" Expr "," Index ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports MAP
  imports STRING

  // Python integer-list values.  A dedicated algebraic list keeps the
  // semantics and its proofs independent of K's collection representation.
  syntax PList ::= "nil"
                 | "cons" "(" Int "," PList ")"

  syntax PVal ::= "pInt" "(" Int ")"
                | "pBool" "(" Bool ")"
                | "pList" "(" PList ")"

  syntax Outcome ::= "pending"
                   | "normal" "(" Map ")"
                   | "returned" "(" PVal ")"
  syntax Outcome ::= PVal

  configuration
    <python>
      <program> $PGM:Module </program>
      <input> $INPUT:PList </input>
      <entry> $ENTRY:String </entry>
      <result> pending </result>
    </python>

  rule <program> PGM </program>
       <input> INPUT </input>
       <entry> ENTRY </entry>
       <result> pending => invoke(ENTRY, pList(INPUT), PGM) </result>

  // Function lookup and big-step statement execution.
  syntax PVal ::= "invoke" "(" String "," PVal "," Module ")" [function]
  rule invoke(F, V, Module(DEFS)) => invokeFind(F, V, DEFS, Module(DEFS))

  syntax PVal ::= "invokeFind" "(" String "," PVal "," Stmts "," Module ")" [function]
  rule invokeFind(F, V,
      FuncDef(F, Params(P), BODY) _REST, ALL)
    => returnedValue(exec(BODY, P |-> V, ALL))
  rule invokeFind(F, V,
      FuncDef(G, Params(_P), _BODY) REST, ALL)
    => invokeFind(F, V, REST, ALL)
    requires F =/=String G

  syntax PVal ::= "returnedValue" "(" Outcome ")" [function]
  rule returnedValue(returned(V)) => V

  syntax Outcome ::= "exec" "(" Stmts "," Map "," Module ")" [function]
  rule exec(.Stmts, ENV, _DEFS) => normal(ENV)
  rule exec(S REST, ENV, DEFS) => continue(execStmt(S, ENV, DEFS), REST, DEFS)

  syntax Outcome ::= "continue" "(" Outcome "," Stmts "," Module ")" [function]
  rule continue(returned(V), _REST, _DEFS) => returned(V)
  rule continue(normal(ENV), REST, DEFS) => exec(REST, ENV, DEFS)

  syntax Outcome ::= "execStmt" "(" Stmt "," Map "," Module ")" [function]
  rule execStmt(Assign(Name(X), E), ENV, DEFS)
    => normal(ENV [ X <- eval(E, ENV, DEFS) ])
  rule execStmt(Return(E), ENV, DEFS) => returned(eval(E, ENV, DEFS))
  rule execStmt(If(COND, THEN, ELSE), ENV, DEFS)
    => branch(eval(COND, ENV, DEFS), THEN, ELSE, ENV, DEFS)

  syntax Outcome ::= "branch" "(" PVal "," Stmts "," Stmts "," Map "," Module ")" [function]
  rule branch(pBool(true),  THEN, _ELSE, ENV, DEFS) => exec(THEN, ENV, DEFS)
  rule branch(pBool(false), _THEN, ELSE, ENV, DEFS) => exec(ELSE, ENV, DEFS)

  // Pure expression evaluation for the AST forms emitted by solution.py.
  syntax PVal ::= "eval" "(" Expr "," Map "," Module ")" [function]
  rule eval(Name(X), ENV, _DEFS) => {ENV[X]}:>PVal
  rule eval(Int(I), _ENV, _DEFS) => pInt(I)
  rule eval(ListExpr(), _ENV, _DEFS) => pList(nil)
  rule eval(ListExpr(E1, E2), ENV, DEFS)
    => makePair(eval(E1, ENV, DEFS), eval(E2, ENV, DEFS))
  rule eval(Call(Name(F), ARG), ENV, DEFS)
    => apply(F, eval(ARG, ENV, DEFS), DEFS)
  rule eval(Compare(LEFT, CmpOp("==", RIGHT)), ENV, DEFS)
    => equal(eval(LEFT, ENV, DEFS), eval(RIGHT, ENV, DEFS))
  rule eval(BinOp("+", LEFT, RIGHT), ENV, DEFS)
    => plus(eval(LEFT, ENV, DEFS), eval(RIGHT, ENV, DEFS))
  rule eval(UnaryOp("-", E), ENV, DEFS) => negate(eval(E, ENV, DEFS))
  rule eval(Subscript(BASE, IDX), ENV, DEFS)
    => index(eval(BASE, ENV, DEFS), IDX, ENV, DEFS)

  syntax PVal ::= "makePair" "(" PVal "," PVal ")" [function]
  rule makePair(pInt(I), pInt(J)) => pList(cons(I, cons(J, nil)))

  syntax PVal ::= "apply" "(" String "," PVal "," Module ")" [function]
  rule apply("len", pList(L), _DEFS) => pInt(length(L))
  rule apply("sorted", pList(L), _DEFS) => pList(sortInts(L))
  rule apply(F, V, DEFS) => invoke(F, V, DEFS)
    requires F =/=String "len" andBool F =/=String "sorted"

  syntax PVal ::= "equal" "(" PVal "," PVal ")" [function]
  rule equal(pInt(I), pInt(J)) => pBool(I ==Int J)

  syntax PVal ::= "plus" "(" PVal "," PVal ")" [function]
  rule plus(pList(L1), pList(L2)) => pList(append(L1, L2))

  syntax PVal ::= "negate" "(" PVal ")" [function]
  rule negate(pInt(I)) => pInt(0 -Int I)

  syntax PVal ::= "index" "(" PVal "," Index "," Map "," Module ")" [function]
  rule index(pList(L), Int(I), _ENV, _DEFS) => pInt(nth(L, I))
  rule index(pList(L), UnaryOp("-", Int(I)), _ENV, _DEFS)
    => pInt(nth(L, length(L) -Int I))
  rule index(pList(L), Slice(Int(1), UnaryOp("-", Int(1)), NoBound), _ENV, _DEFS)
    => pList(interior(L))

  // Mathematical operations needed by the source-language builtins.
  syntax Int ::= "length" "(" PList ")" [function]
  rule length(nil) => 0
  rule length(cons(_I, L)) => 1 +Int length(L)

  syntax Int ::= "nth" "(" PList "," Int ")" [function]
  rule nth(cons(I, _L), 0) => I
  rule nth(cons(_I, L), N) => nth(L, N -Int 1) requires N >Int 0

  syntax PList ::= "append" "(" PList "," PList ")" [function]
  rule append(nil, L2) => L2
  rule append(cons(I, L1), L2) => cons(I, append(L1, L2))

  syntax PList ::= "dropLast" "(" PList ")" [function]
  rule dropLast(nil) => nil
  rule dropLast(cons(_I, nil)) => nil
  rule dropLast(cons(I, cons(J, L))) => cons(I, dropLast(cons(J, L)))

  syntax PList ::= "interior" "(" PList ")" [function]
  rule interior(nil) => nil
  rule interior(cons(_I, L)) => dropLast(L)

  syntax PList ::= "sortInts" "(" PList ")" [function]
  rule sortInts(nil) => nil
  rule sortInts(cons(I, L)) => insertInt(I, sortInts(L))

  syntax PList ::= "insertInt" "(" Int "," PList ")" [function]
  rule insertInt(I, nil) => cons(I, nil)
  rule insertInt(I, cons(J, L)) => cons(I, cons(J, L)) requires I <=Int J
  rule insertInt(I, cons(J, L)) => cons(J, insertInt(I, L)) requires I >Int J
endmodule
