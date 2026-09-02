module MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  // Concrete syntax emitted by the fixed py2mpy.py transliterator.  This is
  // intentionally a small Python subset, but the nodes keep their AST shape.
  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Strings  ::= List{String, ","}
  syntax Params   ::= "Params" "(" Strings ")"
  syntax CellVars ::= "CellVars" "(" Strings ")"
  syntax FreeVars ::= "FreeVars" "(" Strings ")"

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "ListComp" "(" Expr "," CompFors ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CompFors ::= List{CompFor, ""}
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
endmodule

module MPY
  imports MPY-SYNTAX

  // Runtime values.  Ints is the semantic representation of a Python list of
  // integers; unlike the source-level AST, it can also be symbolic in claims.
  syntax Ints ::= List{Int, ","}
  syntax PyVal ::= "intValue" "(" Int ")"
                 | "boolValue" "(" Bool ")"
                 | "listValue" "(" Ints ")"

  syntax Env ::= "emptyEnv"
               | "bind" "(" String "," PyVal "," Env ")"

  syntax Function ::= "noFunction"
                    | "closure" "(" String "," Stmts ")"

  configuration
    <py>
      <k> $PGM:Pgm </k>
      <input> $INPUT:PyVal </input>
      <function> noFunction </function>
      <env> emptyEnv </env>
      <output> listValue(.Ints) </output>
    </py>

  // Module loading registers the entry point.  Imports have no dynamic effect
  // in this subset because annotations are erased by the supplied translator.
  syntax KItem ::= "execModule" "(" Stmts ")" | "startEntry"
  rule <k> Module(SS) => execModule(SS) </k>
  rule <k> execModule(.Stmts) => startEntry </k>
  rule <k> execModule(S SS) => S ~> execModule(SS) </k>
  rule <k> ImportFrom(_, _) => .K ...</k>

  rule <k> FuncDef("remove_duplicates", Params(P), BODY) => .K ...</k>
       <function> noFunction => closure(P, BODY) </function>
  rule <k> FuncDef("remove_duplicates", Params(P), _, _, BODY) => .K ...</k>
       <function> noFunction => closure(P, BODY) </function>

  syntax KItem ::= "execFunction" "(" Stmts ")"
  rule <k> startEntry => execFunction(BODY) </k>
       <input> ARG </input>
       <function> closure(P, BODY) </function>
       <env> _ => bind(P, ARG, emptyEnv) </env>

  // Returning a comprehension starts an explicit transition system.  Keeping
  // iteration in <k> (rather than hiding it in a meta-level evaluator) lets
  // kprove symbolically split an arbitrary list into empty/cons cases.
  syntax KItem ::= "walkComp" "(" Ints "," String "," Expr "," Expr "," Env ")"
                 | "emitComputed" "(" Bool "," Int ")"
  rule <k> execFunction(Return(ListComp(E, CompFor(Name(X), ITER, PRED))) _REST)
         => walkComp(asInts(eval(ITER, ENV)), X, E, PRED, ENV) </k>
       <env> ENV </env>

  rule <k> walkComp(.Ints, _, _, _, _) => .K ...</k>
  rule <k> walkComp((I, IS), X, E, PRED, ENV)
         => (walkComp(IS, X, E, PRED, ENV)
             ~> emitComputed(asBool(eval(PRED, bind(X, intValue(I), ENV))),
                             asInt(eval(E, bind(X, intValue(I), ENV))))) ...</k>
  rule <k> emitComputed(B, I) => .K ...</k>
       <output> listValue(IS) => listValue(ifCons(B, I, IS)) </output>

  syntax Ints ::= "ifCons" "(" Bool "," Int "," Ints ")" [function]
  rule ifCons(true, I, IS) => I, IS
  rule ifCons(false, _, IS) => IS

  // Pure expression evaluator for the constructs used by solution.mpy.
  syntax PyVal ::= "eval" "(" Expr "," Env ")" [function]
  rule eval(Int(I), _) => intValue(I)
  rule eval(Name(X), bind(X, V, _)) => V
  rule eval(Name(X), bind(Y, _, ENV)) => eval(Name(X), ENV)
    requires X =/=String Y

  rule eval(Call(Attribute(E, "count"), A), ENV)
    => intValue(count(asInt(eval(A, ENV)), asInts(eval(E, ENV))))

  rule eval(Compare(L, CmpOp("==", R)), ENV)
    => boolValue(asInt(eval(L, ENV)) ==Int asInt(eval(R, ENV)))

  rule eval(ListComp(E, CompFor(Name(X), ITER, PRED)), ENV)
    => collect(asInts(eval(ITER, ENV)), X, E, PRED, ENV)

  syntax Int ::= "asInt" "(" PyVal ")" [function]
  syntax Ints ::= "asInts" "(" PyVal ")" [function]
  syntax Bool ::= "asBool" "(" PyVal ")" [function]
  rule asInt(intValue(I)) => I
  rule asInts(listValue(IS)) => IS
  rule asBool(boolValue(B)) => B

  // Python list.count for integer lists.
  syntax Int ::= "count" "(" Int "," Ints ")" [function]
  // Concrete execution unfolds count normally.  During symbolic proof the
  // call remains an abstract, shared mathematical observation of ORIGINAL;
  // this avoids needlessly enumerating every possible shape of ORIGINAL.
  rule count(_, .Ints) => 0 [concrete]
  rule count(I, (I, IS)) => 1 +Int count(I, IS) [concrete]
  rule count(I, (J, IS)) => count(I, IS)
    requires I =/=Int J [concrete]

  // A one-generator list comprehension.  The generator variable is pushed in
  // front of the captured environment, matching Python lexical shadowing.
  syntax PyVal ::= "collect" "(" Ints "," String "," Expr "," Expr "," Env ")" [function]
  rule collect(.Ints, _, _, _, _) => listValue(.Ints)
  rule collect((I, IS), X, E, PRED, ENV)
    => prependIf(
         asBool(eval(PRED, bind(X, intValue(I), ENV))),
         asInt(eval(E, bind(X, intValue(I), ENV))),
         collect(IS, X, E, PRED, ENV))

  syntax PyVal ::= "prependIf" "(" Bool "," Int "," PyVal ")" [function]
  rule prependIf(true, I, listValue(IS)) => listValue(I, IS)
  rule prependIf(false, _, listValue(IS)) => listValue(IS)
endmodule
