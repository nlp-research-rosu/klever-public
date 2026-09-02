requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "BoolOp" "(" String "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Subscript" "(" Expr "," Index ")"

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Val ::= "intVal" "(" Int ")"
               | "boolVal" "(" Bool ")"
               | "listVal" "(" Vals ")"
  syntax Vals ::= List{Val, ","}

  syntax Def ::= "def" "(" Params "," Stmts ")"

  syntax Map ::= collectDefs(Stmts) [function]
  rule collectDefs(.Stmts) => .Map
  rule collectDefs(FuncDef(F, P, B) REST)
    => (F |-> def(P, B)) collectDefs(REST)

  syntax Def ::= getDef(Map, String) [function]
  rule getDef((F |-> D:Def) _REST, F) => D

  syntax Val ::= lookupEnv(Map, String) [function]
  rule lookupEnv((X |-> V:Val) _REST, X) => V

  syntax Map ::= bind(Params, Vals) [function]
  rule bind(Params(.Strings), .Vals) => .Map
  rule bind(Params(X, XS), V, VS)
    => (X |-> V) bind(Params(XS), VS)

  syntax Int ::= valLength(Vals) [function]
               | intHead(Vals) [function]
  syntax Vals ::= intTail(Vals) [function]
  rule valLength(.Vals) => 0
  rule valLength(_V, VS) => 1 +Int valLength(VS)
  rule intHead(intVal(N), _VS) => N
  rule intTail(intVal(_N), VS) => VS

  syntax Stmts ::= appendStmts(Stmts, Stmts) [function]
  rule appendStmts(.Stmts, SS) => SS
  rule appendStmts(S:Stmt REST, SS) => S appendStmts(REST, SS)

  syntax Result ::= "noResult" | "result" "(" Val ")"
  syntax KItem ::= "init" "(" Pgm "," Val ")"
                 | "invokeProgram" "(" Pgm "," Val ")"
                 | "invoke" "(" String "," Vals "," Map ")"
                 | "invokeDef" "(" Def "," Vals "," Map ")"
                 | "execStmts" "(" Stmts "," Map "," Map ")"
                 | "eval" "(" Expr "," Map "," Map ")"
                 | "evalArgs" "(" Exprs "," Map "," Map ")"
                 | "argsDone" "(" Vals ")"
                 | "returnIf" "(" Stmts "," Stmts "," Stmts "," Map "," Map ")"
                 | "binLeft" "(" String "," Expr "," Map "," Map ")"
                 | "binRight" "(" String "," Val ")"
                 | "compareLeft" "(" String "," Expr "," Map "," Map ")"
                 | "compareRight" "(" String "," Val ")"
                 | "andLeft" "(" Expr "," Map "," Map ")"
                 | "andRight" "(" Bool ")"
                 | "argsRest" "(" Exprs "," Map "," Map ")"
                 | "prependArg" "(" Val ")"
                 | "callWith" "(" String "," Map ")"
                 | "subscriptWith" "(" Index ")"
                 | "finish"

  configuration
    <mpy>
      <k> init($PGM:Pgm, $ARGS:Val) </k>
      <result> noResult </result>
    </mpy>

  rule <k> init(P, A) => invokeProgram(P, A) ~> finish ... </k>
  rule <k> invokeProgram(Module(SS), L:Val)
          => invoke("skjkasdkd", L, collectDefs(SS))
       ... </k>

  rule <k> invoke(F, ARGS, DEFS)
          => invokeDef(getDef(DEFS, F), ARGS, DEFS)
       ... </k>
  rule <k> invokeDef(def(PARAMS, BODY), ARGS, DEFS)
          => execStmts(BODY, bind(PARAMS, ARGS), DEFS)
       ... </k>

  rule <k> execStmts(Return(E) _REST, ENV, DEFS)
          => eval(E, ENV, DEFS)
       ... </k>
  rule <k> execStmts(If(COND, THEN, ELSE) REST, ENV, DEFS)
          => eval(COND, ENV, DEFS)
             ~> returnIf(THEN, ELSE, REST, ENV, DEFS)
       ... </k>
  rule <k> boolVal(B) ~> returnIf(THEN, _ELSE, REST, ENV, DEFS)
          => execStmts(appendStmts(THEN, REST), ENV, DEFS)
       ... </k>
    requires B
  rule <k> boolVal(B) ~> returnIf(_THEN, ELSE, REST, ENV, DEFS)
          => execStmts(appendStmts(ELSE, REST), ENV, DEFS)
       ... </k>
    requires notBool B

  rule <k> eval(Int(I), _ENV, _DEFS) => intVal(I) ... </k>
  rule <k> eval(Bool(B), _ENV, _DEFS) => boolVal(B) ... </k>
  rule <k> eval(Name(X), ENV, _DEFS) => lookupEnv(ENV, X) ... </k>

  rule <k> eval(BinOp(OP, E1, E2), ENV, DEFS)
          => eval(E1, ENV, DEFS) ~> binLeft(OP, E2, ENV, DEFS)
       ... </k>
  rule <k> V:Val ~> binLeft(OP, E2, ENV, DEFS)
          => eval(E2, ENV, DEFS) ~> binRight(OP, V)
       ... </k>
  rule <k> intVal(J) ~> binRight("+", intVal(I)) => intVal(I +Int J) ... </k>
  rule <k> intVal(J) ~> binRight("*", intVal(I)) => intVal(I *Int J) ... </k>
  rule <k> intVal(J) ~> binRight("%", intVal(I)) => intVal(I %Int J) ... </k>
    requires J =/=Int 0
  rule <k> intVal(J) ~> binRight("//", intVal(I)) => intVal(I /Int J) ... </k>
    requires J =/=Int 0

  rule <k> eval(Compare(E1, CmpOp(OP, E2)), ENV, DEFS)
          => eval(E1, ENV, DEFS) ~> compareLeft(OP, E2, ENV, DEFS)
       ... </k>
  rule <k> V:Val ~> compareLeft(OP, E2, ENV, DEFS)
          => eval(E2, ENV, DEFS) ~> compareRight(OP, V)
       ... </k>
  rule <k> intVal(J) ~> compareRight("<", intVal(I))
          => boolVal(I <Int J)
       ... </k>
  rule <k> intVal(J) ~> compareRight(">", intVal(I))
          => boolVal(I >Int J)
       ... </k>
  rule <k> intVal(J) ~> compareRight("==", intVal(I))
          => boolVal(I ==Int J)
       ... </k>

  rule <k> eval(BoolOp("and", E1, E2), ENV, DEFS)
          => eval(E1, ENV, DEFS) ~> andLeft(E2, ENV, DEFS)
       ... </k>
  rule <k> boolVal(B1) ~> andLeft(E2, ENV, DEFS)
          => eval(E2, ENV, DEFS) ~> andRight(B1)
       ... </k>
  rule <k> boolVal(B2) ~> andRight(B1) => boolVal(B1 andBool B2) ... </k>

  rule <k> eval(Call(Name(F), ES), ENV, DEFS)
          => evalArgs(ES, ENV, DEFS) ~> callWith(F, DEFS)
       ... </k>
  rule <k> evalArgs(.Exprs, _ENV, _DEFS) => argsDone(.Vals) ... </k>
  rule <k> evalArgs(E, ES, ENV, DEFS)
          => eval(E, ENV, DEFS) ~> argsRest(ES, ENV, DEFS)
       ... </k>
  rule <k> V:Val ~> argsRest(ES, ENV, DEFS)
          => evalArgs(ES, ENV, DEFS) ~> prependArg(V)
       ... </k>
  rule <k> argsDone(VS) ~> prependArg(V) => argsDone(V, VS) ... </k>
  rule <k> argsDone(listVal(VS)) ~> callWith("len", _DEFS)
          => intVal(valLength(VS))
       ... </k>
  rule <k> argsDone(VS) ~> callWith(F, DEFS) => invoke(F, VS, DEFS) ... </k>
    requires F =/=String "len"

  rule <k> eval(Subscript(E, INDEX), ENV, DEFS)
          => eval(E, ENV, DEFS) ~> subscriptWith(INDEX)
       ... </k>
  rule <k> listVal(VS) ~> subscriptWith(Int(0))
          => intVal(intHead(VS)) ...
       </k>
    requires valLength(VS) =/=Int 0
  rule <k> listVal(VS)
            ~> subscriptWith(Slice(Int(1), NoBound, NoBound))
          => listVal(intTail(VS))
       ... </k>
    requires valLength(VS) =/=Int 0

  rule <k> V:Val ~> finish => .K ... </k>
       <result> noResult => result(V) </result>
endmodule
