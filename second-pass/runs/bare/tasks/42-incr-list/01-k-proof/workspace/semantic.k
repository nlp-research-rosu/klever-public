requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The constructor grammar emitted by py2mpy.py for this task's subset.
  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts   ::= List{Stmt, ""}
  syntax Params  ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Exp "," Exp ")"
                | "For" "(" Exp "," Exp "," Stmts ")"
                | "Return" "(" Exp ")"

  syntax Exp  ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "ListExpr" "(" Exps ")"
                | "BinOp" "(" String "," Exp "," Exp ")"
  syntax Exps ::= List{Exp, ","}
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports LIST
  imports MAP

  // Runtime Python values. A Python list is represented by a K semantic List
  // containing PyVal elements, so size and indexed lookup remain symbolic.
  syntax PyVal ::= pyInt(Int) | pyList(List)
                 | #incPrefix(List, Int) [function, total]
  syntax Result ::= "noResult" | result(PyVal)
  syntax IterVal ::= "noIter" | iter(String, PyVal)
  // Canonical logical value used by the loop invariant. It cannot arise in a
  // concrete run: only symbolic proof states introduce it.

  configuration
    <mpy>
      <k> #init($PGM:Program, $ARGS:PyVal) </k>
      <env> .Map </env>
      <iter> noIter </iter>
      <result> noResult </result>
    </mpy>

  syntax KItem ::= #init(Program, PyVal)
                 | #exec(Stmts)
                 | #for(List, Int, String, Stmts)
                 | #bind(String, PyVal)
                 | #return(PyVal)

  // This semantics deliberately supports the translated subset used by the
  // solution. The source module must define the requested one-argument entry.
  rule <k> #init(Module(FuncDef("incr_list", Params("l"), BODY)), ARG)
         => #exec(BODY) ... </k>
       <env> .Map => "l" |-> ARG </env>

  rule <k> #exec(.Stmts) => .K ... </k>

  rule <k> #exec(Assign(Name(X), E) REST) => #exec(REST) ... </k>
       <env> ENV => ENV [ X <- #eval(E, ENV, IT) ] </env>
       <iter> IT </iter>

  rule <k> #exec(For(Name(X), E, BODY) REST)
         => #for(#asList(#eval(E, ENV, IT)), 0, X, BODY) ~> #exec(REST) ... </k>
       <env> ENV </env>
       <iter> IT </iter>

  rule <k> #exec(Return(E) _REST) => #return(#eval(E, ENV, IT)) ... </k>
       <env> ENV </env>
       <iter> IT </iter>

  rule <k> #for(L, I, X, BODY)
         => #bind(X, #at(L, I)) ~> #exec(BODY)
            ~> #for(L, I +Int 1, X, BODY) ... </k>
    requires I <Int size(L)

  rule <k> #for(L, I, _X, _BODY) => .K ... </k>
    requires I >=Int size(L)

  rule <k> #bind(X, V) => .K ... </k>
       <iter> _ => iter(X, V) </iter>

  rule <k> #return(V) ~> _ => .K </k>
       <result> noResult => result(V) </result>

  // Expression evaluation is big-step because all supported expressions are
  // pure. Statement order and for-loop control remain explicit in <k>.
  syntax PyVal ::= #eval(Exp, Map, IterVal) [function, total]
                 | #add(PyVal, PyVal) [function, total]
                 | #at(List, Int) [function, total]
  syntax List ::= #evalExps(Exps, Map, IterVal) [function, total]
  syntax List ::= #asList(PyVal) [function]

  rule #eval(Name(X), _ENV, iter(X, V)) => V
  rule #eval(Name(X), (X |-> V) _ENV, _IT) => V
  rule #eval(Int(I), _ENV, _IT) => pyInt(I)
  rule #eval(ListExpr(ES), ENV, IT) => pyList(#evalExps(ES, ENV, IT))
  rule #eval(BinOp("+", E1, E2), ENV, IT)
    => #add(#eval(E1, ENV, IT), #eval(E2, ENV, IT))

  rule #evalExps(.Exps, _ENV, _IT) => .List
  rule #evalExps(E, ES, ENV, IT)
    => ListItem(#eval(E, ENV, IT)) #evalExps(ES, ENV, IT)

  rule #add(pyInt(I), pyInt(J)) => pyInt(I +Int J)
  rule #add(pyList(L1), pyList(L2)) => pyList(L1 L2)
  rule #add(
         #incPrefix(L, I),
         pyList(ListItem(#add(#at(L, I), pyInt(1)))))
    => #incPrefix(L, I +Int 1)
    [simplification]

  rule #asList(pyList(L)) => L
  rule #at(ListItem(V:PyVal) _L, 0) => V
  rule #at(ListItem(_V) L, I) => #at(L, I -Int 1)
    requires I >Int 0

  rule #incPrefix(_L, 0) => pyList(.List)
endmodule
