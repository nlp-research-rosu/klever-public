module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports MAP

  // The constructor grammar emitted by py2mpy.py.  This task uses a deliberately
  // small, explicit subset; unsupported Python constructs cannot silently run.
  syntax Program ::= "Module" "(" Stmts ")" [symbol]

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol]
                | "Return" "(" Expr ")"                         [symbol]
                | "If" "(" Expr "," Stmts "," Stmts ")"       [symbol]

  syntax Params ::= "Params" "(" Strings ")" [symbol]
  syntax Strings ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Name" "(" String ")"                         [symbol]
                | "Int" "(" Int ")"                             [symbol]
                | "Str" "(" String ")"                          [symbol]
                | "ListExpr" "(" Exprs ")"                      [symbol]
                | "BinOp" "(" String "," Expr "," Expr ")"    [symbol]
                | "BoolOp" "(" String "," Exprs ")"            [symbol]
                | "Compare" "(" Expr "," CmpOps ")"            [symbol]
                | "Call" "(" Expr "," Exprs ")"                [symbol]
                | "Subscript" "(" Expr "," Index ")"           [symbol]
                | "ValueExpr" "(" Value ")"                     [symbol]
                | "ListComp" "(" Expr "," CompFors ")"          [symbol]
                | "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" [symbol]
                | "TupleExpr" "(" Exprs ")"                     [symbol]
                | "KwArg" "(" String "," Expr ")"              [symbol]
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"             [symbol]
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"  [symbol]
  syntax Bound ::= Expr | "NoBound" [symbol]
  syntax CompFors ::= List{CompFor, ""}
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")" [symbol]
  syntax CellVars ::= "CellVars" "(" Strings ")" [symbol]
  syntax FreeVars ::= "FreeVars" "(" Strings ")" [symbol]

  syntax Words ::= List{String, ","}
  syntax Value ::= "VInt" "(" Int ")"       [symbol]
                 | "VStr" "(" String ")"    [symbol]
                 | "VBool" "(" Bool ")"     [symbol]
                 | "VList" "(" Words ")"    [symbol]
                 | "VNone"                    [symbol]
  syntax Values ::= List{Value, ","}

  syntax Run ::= "Run" "(" Program "," Expr ")" [symbol]
  syntax Result ::= "Result" "(" Value ")" [symbol]
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports MAP

  configuration <k> $PGM:Run </k>

  syntax Value ::= evalExpr ( Expr , Map , Program ) [function]
  syntax Values ::= evalExprs ( Exprs , Map , Program ) [function]
  syntax Value ::= evalBinOp ( String , Value , Value ) [function]
                 | evalCompare ( String , Value , Value ) [function]
                 | evalBoolOp ( String , Values ) [function]
                 | evalSubscript ( Value , Index , Map , Program ) [function]
                 | callFunction ( Function , Values , Program ) [function]
                 | returnedValue ( ExecResult ) [function]
                 | makeList ( Values ) [function]
  syntax Int ::= valueLength ( Value ) [function]
  syntax Words ::= valueWords ( Value ) [function]
                 | filterEven ( Words ) [function]
                 | filterEvenDecision ( Bool , String , Words ) [function]
                 | sortByKey ( Words ) [function]
                 | insertBySemanticKey ( String , Words ) [function]
                 | insertBySemanticDecision ( Bool , String , String , Words ) [function]
  syntax Bool ::= semanticKeyLess ( String , String ) [function]

  syntax Function ::= "Function" "(" Params "," Stmts ")" [symbol]
                    | findFunction ( String , Stmts ) [function]
  syntax Stmts ::= programStmts ( Program ) [function]
  syntax Map ::= bindParams ( Params , Values ) [function]

  syntax ExecResult ::= "Normal" [symbol]
                      | "Returned" "(" Value ")" [symbol]
                      | execStmts ( Stmts , Map , Program ) [function]
                      | continueWith ( ExecResult , Stmts , Map , Program ) [function]
                      | chooseBranch ( Value , Stmts , Stmts , Stmts , Map , Program ) [function]

  rule <k> Run(P, E) => Result(evalExpr(E, .Map, P)) </k>

  rule programStmts(Module(SS)) => SS

  rule findFunction(F, FuncDef(F, PS, BODY) REST)
    => Function(PS, BODY)
  rule findFunction(F, FuncDef(G, PS, BODY) REST)
    => findFunction(F, REST)
    requires F =/=String G

  rule bindParams(Params(.Strings), .Values) => .Map
  rule bindParams(Params(X, XS), V, VS)
    => (X |-> V) bindParams(Params(XS), VS)

  rule evalExpr(ValueExpr(V), ENV, P) => V
  rule evalExpr(Int(I), ENV, P) => VInt(I)
  rule evalExpr(Str(S), ENV, P) => VStr(S)
  rule evalExpr(Name(X), ENV, P) => {ENV[X]}:>Value

  rule evalExprs(.Exprs, ENV, P) => .Values
  rule evalExprs(E, ENV, P) => evalExpr(E, ENV, P)
  rule evalExprs(E, ES, ENV, P)
    => evalExpr(E, ENV, P), evalExprs(ES, ENV, P)

  rule evalExpr(ListExpr(ES), ENV, P)
    => makeList(evalExprs(ES, ENV, P))
  rule makeList(.Values) => VList(.Words)
  rule makeList(VStr(S)) => VList(S)
  rule makeList(VStr(S), VS)
    => prependWord(S, makeList(VS))

  syntax Value ::= prependWord ( String , Value ) [function]
  rule prependWord(S, VList(WS)) => VList(S, WS)

  rule evalExpr(BinOp(OP, L, R), ENV, P)
    => evalBinOp(OP, evalExpr(L, ENV, P), evalExpr(R, ENV, P))
  rule evalBinOp("%", VInt(I), VInt(J)) => VInt(I %Int J)
  rule evalBinOp("+", VList(LS), VList(RS)) => VList(LS, RS)

  rule evalExpr(Compare(L, CmpOp(OP, R)), ENV, P)
    => evalCompare(OP, evalExpr(L, ENV, P), evalExpr(R, ENV, P))
  rule evalCompare("==", VInt(I), VInt(J)) => VBool(I ==Int J)
  rule evalCompare("<", VInt(I), VInt(J)) => VBool(I <Int J)
  rule evalCompare("<", VStr(S), VStr(T)) => VBool(S <String T)

  rule evalExpr(BoolOp(OP, ES), ENV, P)
    => evalBoolOp(OP, evalExprs(ES, ENV, P))
  rule evalBoolOp("and", VBool(B1), VBool(B2))
    => VBool(B1 andBool B2)

  rule evalExpr(Call(Name("len"), E), ENV, P)
    => VInt(valueLength(evalExpr(E, ENV, P)))

  // Denotation of the exact comprehension emitted for
  //   [word for word in lst if len(word) % 2 == 0]
  // The binder names are matched, not hard-coded.
  rule evalExpr(
         ListComp(Name(X),
           CompFor(Name(X), Name(L),
             Compare(
               BinOp("%", Call(Name("len"), Name(X)), Int(2)),
               CmpOp("==", Int(0))))),
         ENV,
         P)
    => VList(filterEven(valueWords({ENV[L]}:>Value)))

  // Denotation of sorted(..., key=lambda word: (len(word), word)).
  rule evalExpr(
         Call(Name("sorted"), E,
           KwArg("key",
             Lambda(Params(X), CellVars(.Strings), FreeVars(.Strings),
               TupleExpr(Call(Name("len"), Name(X)), Name(X))))),
         ENV,
         P)
    => VList(sortByKey(valueWords(evalExpr(E, ENV, P))))

  rule evalExpr(Call(Name(F), ES), ENV, P)
    => callFunction(
         findFunction(F, programStmts(P)),
         evalExprs(ES, ENV, P),
         P)
    requires F =/=String "len" andBool F =/=String "sorted"
  rule callFunction(Function(PS, BODY), VS, P)
    => returnedValue(execStmts(BODY, bindParams(PS, VS), P))
  rule returnedValue(Returned(V)) => V

  rule valueLength(VStr(S)) => lengthString(S)
  rule valueLength(VList(.Words)) => 0
  rule valueLength(VList(S, SS)) => 1 +Int valueLength(VList(SS))

  rule valueWords(VList(WS)) => WS

  rule filterEven(.Words) => .Words
  rule filterEven(S, SS)
    => filterEvenDecision(lengthString(S) %Int 2 ==Int 0, S, filterEven(SS))
  rule filterEvenDecision(B, S, SS) => S, SS
    requires B
  rule filterEvenDecision(B, S, SS) => SS
    requires notBool B

  rule sortByKey(.Words) => .Words
  rule sortByKey(S, SS) => insertBySemanticKey(S, sortByKey(SS))
  rule insertBySemanticKey(S, .Words) => S
  rule insertBySemanticKey(S, T, TS)
    => insertBySemanticDecision(semanticKeyLess(S, T), S, T, TS)
  rule semanticKeyLess(S, T)
    => (lengthString(S) <Int lengthString(T))
       orBool ((lengthString(S) ==Int lengthString(T)) andBool (S <String T))
  rule insertBySemanticDecision(B, S, T, TS) => S, T, TS
    requires B
  rule insertBySemanticDecision(B, S, T, TS)
    => T, insertBySemanticKey(S, TS)
    requires notBool B

  rule evalExpr(Subscript(E, IX), ENV, P)
    => evalSubscript(evalExpr(E, ENV, P), IX, ENV, P)
  rule evalSubscript(VList(S, SS), Int(0), ENV, P) => VStr(S)
  rule evalSubscript(VList(S, SS), Slice(Int(1), NoBound, NoBound), ENV, P)
    => VList(SS)

  rule execStmts(.Stmts, ENV, P) => Normal
  rule execStmts(Return(E) REST, ENV, P)
    => Returned(evalExpr(E, ENV, P))
  rule execStmts(If(COND, THEN, ELSE) REST, ENV, P)
    => chooseBranch(evalExpr(COND, ENV, P), THEN, ELSE, REST, ENV, P)

  rule chooseBranch(VBool(B), THEN, ELSE, REST, ENV, P)
    => continueWith(execStmts(THEN, ENV, P), REST, ENV, P)
    requires B
  rule chooseBranch(VBool(B), THEN, ELSE, REST, ENV, P)
    => continueWith(execStmts(ELSE, ENV, P), REST, ENV, P)
    requires notBool B
  rule continueWith(Returned(V), REST, ENV, P) => Returned(V)
  rule continueWith(Normal, REST, ENV, P) => execStmts(REST, ENV, P)
endmodule
