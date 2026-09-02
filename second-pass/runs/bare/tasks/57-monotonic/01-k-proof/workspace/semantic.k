module SEMANTIC-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Bool" "(" Bool ")"
                | "BoolOp" "(" String "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "KwArg" "(" String "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // Values used by this task: booleans and finite lists of mathematical ints.
  syntax IntList ::= "nil"
                   | "cons" "(" Int "," IntList ")"
  syntax Val ::= "boolVal" "(" Bool ")"
               | "listVal" "(" IntList ")"
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  configuration <k> #run($PGM:Pgm, $ARG:Val) </k>

  // A small, compositional evaluator for the translated subset used in
  // solution.mpy. Function definitions remain AST data until invoked.
  syntax Fun ::= "function" "(" Params "," Stmts ")"
  syntax Env ::= "env" "(" String "," Val ")"

  syntax Fun ::= #findFunction(String, Stmts) [function]
  rule #findFunction(F, FuncDef(F, P, BODY) _REST)
    => function(P, BODY)
  rule #findFunction(F, FuncDef(G, _P, _BODY) REST)
    => #findFunction(F, REST)
    requires F =/=String G

  syntax KItem ::= #run(Pgm, Val)

  syntax Val ::= #apply(String, Val, Stmts) [function]
               | #applyFunction(Fun, Val, Stmts) [function]
               | #exec(Stmts, Env, Stmts) [function]
               | #eval(Expr, Env, Stmts) [function]
               | #equals(Val, Val) [function]
               | #boolOr(Val, Val) [function]

  rule #run(Module(FUNS), ARG)
    => #apply("monotonic", ARG, FUNS)

  rule #apply(F, ARG, FUNS)
    => #applyFunction(#findFunction(F, FUNS), ARG, FUNS)
  rule #applyFunction(function(Params(P), BODY), ARG, FUNS)
    => #exec(BODY, env(P, ARG), FUNS)

  rule #exec(Return(E) _REST, ENV, FUNS)
    => #eval(E, ENV, FUNS)

  rule #eval(Name(N), env(N, V), _FUNS) => V
  rule #eval(Bool(B), _ENV, _FUNS) => boolVal(B)

  // Both operands in this task are pure and total. Evaluating them eagerly is
  // observationally identical to Python's short-circuiting `or` here.
  rule #eval(BoolOp("or", E1, E2), ENV, FUNS)
    => #boolOr(#eval(E1, ENV, FUNS), #eval(E2, ENV, FUNS))
  rule #boolOr(boolVal(B1), boolVal(B2))
    => boolVal(B1 orBool B2)

  rule #eval(Compare(E1, CmpOp("==", E2)), ENV, FUNS)
    => #equals(#eval(E1, ENV, FUNS), #eval(E2, ENV, FUNS))
  rule #equals(listVal(L1), listVal(L2))
    => boolVal(#eqIntLists(L1, L2))

  // The two sorted call shapes appearing in solution.mpy.
  rule #eval(Call(Name("sorted"), E), ENV, FUNS)
    => listVal(#sortInts(#asIntList(#eval(E, ENV, FUNS))))
  rule #eval(
          Call(Name("sorted"), E, KwArg("reverse", Bool(true))),
          ENV,
          FUNS)
    => listVal(#reverseInts(#sortInts(#asIntList(#eval(E, ENV, FUNS)))))

  syntax IntList ::= #asIntList(Val) [function]
  rule #asIntList(listVal(L)) => L

  // Insertion sort gives `sorted` an executable, independently stated
  // meaning rather than treating it as an oracle.
  syntax IntList ::= #sortInts(IntList) [function]
                   | #insertInt(Int, IntList) [function]
  rule #sortInts(nil) => nil
  rule #sortInts(cons(I, L)) => #insertInt(I, #sortInts(L))

  rule #insertInt(I, nil) => cons(I, nil)
  rule #insertInt(I, cons(J, L)) => cons(I, cons(J, L))
    requires I <=Int J
  rule #insertInt(I, cons(J, L)) => cons(J, #insertInt(I, L))
    requires I >Int J

  syntax IntList ::= #reverseInts(IntList) [function]
                   | #appendInts(IntList, IntList) [function]
  rule #reverseInts(nil) => nil
  rule #reverseInts(cons(I, L))
    => #appendInts(#reverseInts(L), cons(I, nil))
  rule #appendInts(nil, L2) => L2
  rule #appendInts(cons(I, L1), L2)
    => cons(I, #appendInts(L1, L2))

  syntax Bool ::= #eqIntLists(IntList, IntList) [function]
  rule #eqIntLists(nil, nil) => true
  rule #eqIntLists(nil, cons(_I, _L)) => false
  rule #eqIntLists(cons(_I, _L), nil) => false
  rule #eqIntLists(cons(I, L1), cons(J, L2))
    => (I ==Int J) andBool #eqIntLists(L1, L2)
endmodule
