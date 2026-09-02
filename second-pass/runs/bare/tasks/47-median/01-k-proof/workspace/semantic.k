requires "verification.k"

module MEDIAN-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The source language is the constructor language emitted by py2mpy.py.
  // This grammar intentionally covers every constructor used by solution.mpy.
  syntax Module ::= "Module" "(" Stmts ")" [symbol(moduleNode)]

  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                  [symbol(funcDefNode)]
                | "Assign" "(" Expr "," Expr ")" [symbol(assignNode)]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol(ifNode)]
                | "Return" "(" Expr ")" [symbol(returnNode)]

  syntax Params ::= "Params" "(" String ")" [symbol(oneParamNode)]

  syntax Expr ::= "Name" "(" String ")" [symbol(nameNode)]
                | "Int" "(" Int ")" [symbol(intNode)]
                | "Call" "(" Expr "," Expr ")" [symbol(callNode)]
                | "BinOp" "(" String "," Expr "," Expr ")"
                  [symbol(binOpNode)]
                | "Subscript" "(" Expr "," Expr ")"
                  [symbol(subscriptNode)]

  // Constructor notation used to supply integer lists to krun and kprove.
  syntax Ints ::= "nil" [symbol(nilInts)]
                | "cons" "(" Int "," Ints ")" [symbol(consInts)]
endmodule

module MEDIAN-SEMANTICS
  imports MEDIAN-SYNTAX
  imports INT
  imports STRING

  syntax Val ::= intVal(Int)
               | floatVal(Int, Int)
               | listVal(Ints)

  syntax Env ::= ".Env"
               | bind(String, Val, Env)

  syntax ExecResult ::= next(Env) | returned(Val)
  syntax ResultSlot ::= "noResult" | Val

  syntax Val ::= lookup(String, Env) [function]
  rule lookup(X, bind(X, V, _)) => V
  rule lookup(X, bind(Y, _, REST)) => lookup(X, REST)
    requires X =/=String Y

  syntax Val ::= evalExpr(Expr, Env) [function]
  rule evalExpr(Int(I), _) => intVal(I)
  rule evalExpr(Name(X), ENV) => lookup(X, ENV)
  rule evalExpr(Call(Name("sorted"), E), ENV)
    => sortVal(evalExpr(E, ENV))
  rule evalExpr(Call(Name("len"), E), ENV)
    => lenVal(evalExpr(E, ENV))
  rule evalExpr(Subscript(E1, E2), ENV)
    => subscriptVal(evalExpr(E1, ENV), evalExpr(E2, ENV))
  rule evalExpr(BinOp(OP, E1, E2), ENV)
    => binopVal(OP, evalExpr(E1, ENV), evalExpr(E2, ENV))

  syntax Val ::= sortVal(Val) [function]
               | lenVal(Val) [function]
               | subscriptVal(Val, Val) [function]
               | binopVal(String, Val, Val) [function]
               | ifVal(Val, Val, Val) [function]

  rule sortVal(listVal(IS)) => listVal(sortInts(IS))
  rule lenVal(listVal(IS)) => intVal(lenInts(IS))
  rule subscriptVal(listVal(IS), intVal(N)) => intVal(nthInt(IS, N))

  rule binopVal("+", intVal(I), intVal(J)) => intVal(I +Int J)
  rule binopVal("//", intVal(I), intVal(J)) => intVal(I /Int J)
  rule binopVal("%", intVal(I), intVal(J)) => intVal(I %Int J)
  // floatVal(N,D) is an exact model of a Python floating division N / D.
  rule binopVal("/", intVal(I), intVal(J)) => floatVal(I, J)

  rule ifVal(intVal(0), _, ELSE) => ELSE
  rule ifVal(intVal(I), THEN, _) => THEN requires I =/=Int 0

  syntax Int ::= lenInts(Ints) [function, total]
               | nthInt(Ints, Int) [function, total]
  syntax Ints ::= sortInts(Ints) [function, total]
                | insertInt(Int, Ints) [function, total]

  rule lenInts(nil) => 0
  rule lenInts(cons(_, REST)) => 1 +Int lenInts(REST)

  rule nthInt(cons(I, _), 0) => I
  rule nthInt(cons(_, REST), N) => nthInt(REST, N -Int 1)
    requires N >Int 0

  // A deterministic insertion sort supplies Python sorted() for integer lists.
  rule sortInts(nil) => nil
  rule sortInts(cons(I, REST)) => insertInt(I, sortInts(REST))
  rule insertInt(I, nil) => cons(I, nil)
  rule insertInt(I, cons(J, REST)) => cons(I, cons(J, REST))
    requires I <=Int J
  rule insertInt(I, cons(J, REST)) => cons(J, insertInt(I, REST))
    requires I >Int J

  syntax ExecResult ::= evalBody(Stmts, Env) [function]
                      | continueWith(ExecResult, Stmts) [function]
                      | chooseBody(Val, Stmts, Stmts, Stmts, Env) [function]

  rule evalBody(.Stmts, ENV) => next(ENV)
  rule evalBody(Assign(Name(X), E) REST, ENV)
    => evalBody(REST, bind(X, evalExpr(E, ENV), ENV))
  rule evalBody(Return(E) _REST, ENV) => returned(evalExpr(E, ENV))

  // This rule is the ordinary semantics of an if whose two arms return.
  // Keeping it as one equation also leaves a useful symbolic ifVal term when
  // the list length is symbolic.
  rule evalBody(
         If(COND,
           Return(THEN) .Stmts,
           Return(ELSE) .Stmts)
         _REST,
         ENV)
    => returned(ifVal(evalExpr(COND, ENV),
                      evalExpr(THEN, ENV),
                      evalExpr(ELSE, ENV)))

  // General statement-level if semantics (not needed only by this solution).
  rule evalBody(If(COND, THEN, ELSE) REST, ENV)
    => chooseBody(evalExpr(COND, ENV), THEN, ELSE, REST, ENV)
  rule chooseBody(intVal(0), _, ELSE, REST, ENV)
    => continueWith(evalBody(ELSE, ENV), REST)
  rule chooseBody(intVal(I), THEN, _, REST, ENV)
    => continueWith(evalBody(THEN, ENV), REST)
    requires I =/=Int 0
  rule continueWith(returned(V), _) => returned(V)
  rule continueWith(next(ENV), REST) => evalBody(REST, ENV)

  configuration
    <median>
      <k> $PGM:Module </k>
      <input> $INPUT:Ints </input>
      <result> noResult </result>
    </median>

  rule <k> Module(FuncDef("median", Params("l"), BODY) .Stmts)
           => evalBody(BODY, bind("l", listVal(IS), .Env))
       </k>
       <input> IS </input>

  rule <k> returned(V) => .K </k>
       <result> noResult => V </result>
endmodule

module SEMANTIC
  imports MEDIAN-VERIFICATION
endmodule
