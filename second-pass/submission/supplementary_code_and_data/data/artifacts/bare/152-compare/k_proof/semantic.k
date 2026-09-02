requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")" [symbol(Module)]

  syntax Stmts ::= List{Stmt, ""} [symbol(stmts)]
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Return" "(" Expr ")"                         [symbol(Return)]
                | "Assign" "(" Expr "," Expr ")"               [symbol(Assign)]
                | "If" "(" Expr "," Stmts "," Stmts ")"        [symbol(If)]

  syntax Params ::= "Params" "(" Strings ")" [symbol(Params)]
  syntax Strings ::= List{String, ","} [symbol(strings)]

  syntax Expr ::= "Name" "(" String ")"                         [symbol(Name)]
                | "Int" "(" Int ")"                             [symbol(IntExpr)]
                | "ListExpr" "(" Exprs ")"                      [symbol(ListExpr)]
                | "BinOp" "(" String "," Expr "," Expr ")"     [symbol(BinOp)]
                | "UnaryOp" "(" String "," Expr ")"             [symbol(UnaryOp)]
                | "Compare" "(" Expr "," CmpOps ")"             [symbol(Compare)]
                | "Subscript" "(" Expr "," Index ")"            [symbol(Subscript)]
                | "Call" "(" Expr "," Exprs ")"                 [symbol(Call)]

  syntax Exprs ::= List{Expr, ","} [symbol(exprs)]
  syntax CmpOps ::= List{CmpOp, ","} [symbol(cmpOps)]
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")" [symbol(Slice)]
  syntax Bound ::= Expr | "NoBound" [symbol(NoBound)]
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  syntax Value ::= "VInt" "(" Int ")"     [symbol(VInt)]
                 | "VBool" "(" Bool ")"   [symbol(VBool)]
                 | "VList" "(" Values ")" [symbol(VList)]
  syntax Values ::= "VNil"                            [symbol(VNil)]
                  | "VCons" "(" Value "," Values ")" [symbol(VCons)]

  syntax Env ::= "EmptyEnv"                           [symbol(EmptyEnv)]
               | "Bind" "(" String "," Value "," Env ")" [symbol(Bind)]
  syntax Outcome ::= "Ongoing" "(" Env ")"           [symbol(Ongoing)]
                   | "Returned" "(" Value ")"        [symbol(Returned)]

  syntax KItem ::= execute(Pgm, Value, Value) [symbol(execute)]
                 | invokeK(Pgm, Value, Value) [symbol(invokeK)]
                 | execK(Stmts, Env, Pgm) [symbol(execK)]
                 | evalK(Expr, Env, Pgm) [symbol(evalK)]
                 | evalExprsK(Exprs, Env, Pgm) [symbol(evalExprsK)]
                 | "makeReturned" [symbol(makeReturned)]
                 | "extractReturned" [symbol(extractReturned)]
                 | assignK(String, Stmts, Env, Pgm) [symbol(assignK)]
                 | ifK(Stmts, Stmts, Stmts, Env, Pgm) [symbol(ifK)]
                 | continueK(Stmts, Pgm) [symbol(continueK)]
                 | listHeadK(Exprs, Env, Pgm) [symbol(listHeadK)]
                 | listTailK(Value) [symbol(listTailK)]
                 | binLeftK(String, Expr, Env, Pgm) [symbol(binLeftK)]
                 | binRightK(String, Value) [symbol(binRightK)]
                 | unaryK(String) [symbol(unaryK)]
                 | compareLeftK(String, Expr, Env, Pgm) [symbol(compareLeftK)]
                 | compareRightK(String, Value) [symbol(compareRightK)]
                 | subscriptK(Index) [symbol(subscriptK)]
                 | callArgK(Expr, Env, Pgm) [symbol(callArgK)]
                 | callInvokeK(Value, Pgm) [symbol(callInvokeK)]

  syntax Value ::= lookupEnv(String, Env) [function, symbol(lookupEnv)]
                 | lookupAt(Values, Int) [function, symbol(lookupAt)]
                 | indexValue(Value, Index) [function, symbol(indexValue)]
                 | headValue(Values) [function, total, symbol(headValue)]
  syntax Values ::= dropValues(Values, Int) [function, symbol(dropValues)]
                  | concatValues(Values, Values) [function, symbol(concatValues)]
                  | tailValues(Values) [function, total, symbol(tailValues)]
  syntax Bool ::= isEmptyValues(Values) [function, total, symbol(isEmptyValues)]
  syntax Int ::= valueAsInt(Value) [function, total, symbol(valueAsInt)]

  configuration <k> execute($PGM:Pgm, $GAME:Value, $GUESS:Value) </k>

  rule execute(P, GAME, GUESS) => invokeK(P, GAME, GUESS)
  rule invokeK(
         Module(FuncDef("compare", Params("game", "guess"), BODY)),
         GAME, GUESS)
    => execK(
         BODY,
         Bind("game", GAME, Bind("guess", GUESS, EmptyEnv)),
         Module(FuncDef("compare", Params("game", "guess"), BODY)))
       ~> extractReturned

  rule execK(.Stmts, ENV, _) => Ongoing(ENV)
  rule execK(Return(E) _REST, ENV, P) => evalK(E, ENV, P) ~> makeReturned
  rule execK(Assign(Name(X), E) REST, ENV, P)
    => evalK(E, ENV, P) ~> assignK(X, REST, ENV, P)
  rule execK(If(COND, THEN, ELSE) REST, ENV, P)
    => evalK(COND, ENV, P) ~> ifK(THEN, ELSE, REST, ENV, P)

  rule V:Value ~> makeReturned => Returned(V)
  rule Returned(V) ~> extractReturned => V
  rule V:Value ~> assignK(X, REST, ENV, P)
    => execK(REST, Bind(X, V, ENV), P)
  rule VBool(B) ~> ifK(THEN, _, REST, ENV, P)
    => execK(THEN, ENV, P) ~> continueK(REST, P)
    requires B
  rule VBool(B) ~> ifK(_, ELSE, REST, ENV, P)
    => execK(ELSE, ENV, P) ~> continueK(REST, P)
    requires notBool B
  rule Ongoing(ENV) ~> continueK(REST, P) => execK(REST, ENV, P)
  rule Returned(V) ~> continueK(_, _) => Returned(V)

  rule evalK(Name(X), ENV, _) => lookupEnv(X, ENV)
  rule evalK(Int(I), _, _) => VInt(I)
  rule evalK(ListExpr(ES), ENV, P) => evalExprsK(ES, ENV, P)
  rule evalExprsK(.Exprs, _, _) => VList(VNil)
  rule evalExprsK(E, ES, ENV, P)
    => evalK(E, ENV, P) ~> listHeadK(ES, ENV, P)
  rule V:Value ~> listHeadK(ES, ENV, P)
    => evalExprsK(ES, ENV, P) ~> listTailK(V)
  rule VList(VS) ~> listTailK(V) => VList(VCons(V, VS))

  rule evalK(BinOp(OP, L, R), ENV, P)
    => evalK(L, ENV, P) ~> binLeftK(OP, R, ENV, P)
  rule V:Value ~> binLeftK(OP, R, ENV, P)
    => evalK(R, ENV, P) ~> binRightK(OP, V)
  rule V2:Value ~> binRightK("-", V1:Value)
    => VInt(valueAsInt(V1) -Int valueAsInt(V2))
  rule VList(RS) ~> binRightK("+", VList(LS))
    => VList(concatValues(LS, RS))

  rule evalK(UnaryOp(OP, E), ENV, P) => evalK(E, ENV, P) ~> unaryK(OP)
  rule VInt(I) ~> unaryK("-") => VInt(0 -Int I)

  rule evalK(Compare(L, CmpOp(OP, R)), ENV, P)
    => evalK(L, ENV, P) ~> compareLeftK(OP, R, ENV, P)
  rule V:Value ~> compareLeftK(OP, R, ENV, P)
    => evalK(R, ENV, P) ~> compareRightK(OP, V)
  rule VList(VNil) ~> compareRightK("==", VList(VS))
    => VBool(isEmptyValues(VS))
  rule VInt(J) ~> compareRightK("<", VInt(I)) => VBool(I <Int J)

  rule evalK(Subscript(E, IDX), ENV, P) => evalK(E, ENV, P) ~> subscriptK(IDX)
  rule V:Value ~> subscriptK(IDX) => indexValue(V, IDX)
  rule indexValue(VList(VS), Int(N)) => lookupAt(VS, N)
    requires N >=Int 0
  rule indexValue(VList(VS), Slice(Int(N), NoBound, NoBound))
    => VList(dropValues(VS, N))
    requires N >=Int 0

  rule evalK(Call(Name("compare"), GAME, GUESS), ENV, P)
    => evalK(GAME, ENV, P) ~> callArgK(GUESS, ENV, P)
  rule GAME:Value ~> callArgK(GUESS, ENV, P)
    => evalK(GUESS, ENV, P) ~> callInvokeK(GAME, P)
  rule GUESS:Value ~> callInvokeK(GAME, P) => execute(P, GAME, GUESS)

  rule lookupEnv(X, Bind(X, V, _)) => V
  rule lookupEnv(X, Bind(Y, _, ENV)) => lookupEnv(X, ENV)
    requires X =/=String Y

  rule isEmptyValues(VNil) => true
  rule isEmptyValues(VCons(_, _)) => false
  rule headValue(VNil) => VInt(0)
  rule headValue(VCons(V, _)) => V
  rule tailValues(VNil) => VNil
  rule tailValues(VCons(_, VS)) => VS
  rule valueAsInt(VInt(I)) => I
  rule valueAsInt(VBool(_)) => 0
  rule valueAsInt(VList(_)) => 0
  rule lookupAt(VS, 0) => headValue(VS)
  rule lookupAt(VS, N) => lookupAt(tailValues(VS), N -Int 1)
    requires N >Int 0
  rule dropValues(VS, 0) => VS
  rule dropValues(VS, N) => dropValues(tailValues(VS), N -Int 1)
    requires N >Int 0
  rule concatValues(VNil, VS) => VS
  rule concatValues(VCons(V, VS), WS) => VCons(V, concatValues(VS, WS))
endmodule
