module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef(" String "," Params "," Stmts ")"
                | "If(" Expr "," Stmts "," Stmts ")"
                | "Return(" Expr ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params(" Strings ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Expr ::= "Int(" Int ")"
                | "Name(" String ")"
                | "BinOp(" String "," Expr "," Expr ")"
                | "Compare(" Expr "," CmpOps ")"
                | "ListExpr(" Exprs ")"
                | "Call(" Expr "," Exprs ")"
  syntax CmpOp ::= "CmpOp(" String "," Expr ")"
endmodule

module TRI-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  syntax IntSeq ::= "nil"
                  | "cons" "(" Int "," IntSeq ")"

  syntax Value ::= "IVal" "(" Int ")"
                 | "BVal" "(" Bool ")"
                 | "LVal" "(" IntSeq ")"

  syntax Result ::= "returned" "(" Value ")"
                  | "fellThrough"

  configuration <k> run($PGM:Program, $N:Int) </k>

  syntax KItem ::= "run" "(" Program "," Int ")"
                 | evalCall ( Program , String , Int )
                 | findCall ( Stmts , String , Int , Program )
                 | exec ( Stmts , Int , Program )
                 | "doReturn"
                 | choose ( Stmts , Stmts , Stmts , Int , Program )
                 | afterBranch ( Stmts , Int , Program )
                 | evalExpr ( Expr , Int , Program )
                 | binLeft ( String , Expr , Int , Program )
                 | binRight ( String , Value )
                 | cmpLeft ( Expr , Int , Program )
                 | cmpRight ( Int )
                 | "singleton"
                 | callArg ( String , Program )
                 | "callDone"
  syntax Value ::= bin ( String , Value , Value ) [function]
  syntax IntSeq ::= append ( IntSeq , IntSeq ) [function]

  rule <k> run(P, N) => evalCall(P, "tri", N) ... </k>

  rule <k> evalCall(Module(DEFS), F, N)
        => findCall(DEFS, F, N, Module(DEFS)) ... </k>

  rule <k> findCall(FuncDef(F, Params(_X), BODY) _REST, F, N, P)
        => exec(BODY, N, P) ... </k>
  rule <k> findCall(FuncDef(G, Params(_X), _BODY) REST, F, N, P)
        => findCall(REST, F, N, P) ... </k>
    requires G =/=String F

  rule <k> exec(.Stmts, _N, _P) => fellThrough ... </k>
  rule <k> exec(Return(E) _REST, N, P)
        => evalExpr(E, N, P) ~> doReturn ... </k>
  rule <k> V:Value ~> doReturn => returned(V) ... </k>

  rule <k> exec(If(C, THEN, ELSE) REST, N, P)
        => evalExpr(C, N, P) ~> choose(THEN, ELSE, REST, N, P) ... </k>
  rule <k> BVal(true) ~> choose(THEN, _ELSE, REST, N, P)
        => exec(THEN, N, P) ~> afterBranch(REST, N, P) ... </k>
  rule <k> BVal(false) ~> choose(_THEN, ELSE, REST, N, P)
        => exec(ELSE, N, P) ~> afterBranch(REST, N, P) ... </k>
  rule <k> returned(V) ~> afterBranch(_REST, _N, _P)
        => returned(V) ... </k>
  rule <k> fellThrough ~> afterBranch(REST, N, P)
        => exec(REST, N, P) ... </k>

  rule <k> evalExpr(Int(I), _N, _P) => IVal(I) ... </k>
  rule <k> evalExpr(Name("n"), N, _P) => IVal(N) ... </k>
  rule <k> evalExpr(BinOp(OP, L, R), N, P)
        => evalExpr(L, N, P) ~> binLeft(OP, R, N, P) ... </k>
  rule <k> V:Value ~> binLeft(OP, R, N, P)
        => evalExpr(R, N, P) ~> binRight(OP, V) ... </k>
  rule <k> W:Value ~> binRight(OP, V)
        => bin(OP, V, W) ... </k>

  rule <k> evalExpr(Compare(L, CmpOp("==", R)), N, P)
        => evalExpr(L, N, P) ~> cmpLeft(R, N, P) ... </k>
  rule <k> IVal(A) ~> cmpLeft(R, N, P)
        => evalExpr(R, N, P) ~> cmpRight(A) ... </k>
  rule <k> IVal(B) ~> cmpRight(A) => BVal(true) ... </k>
    requires A ==Int B
  rule <k> IVal(B) ~> cmpRight(A) => BVal(false) ... </k>
    requires A =/=Int B

  rule <k> evalExpr(ListExpr(E), N, P)
        => evalExpr(E, N, P) ~> singleton ... </k>
  rule <k> IVal(I) ~> singleton => LVal(cons(I, nil)) ... </k>

  rule <k> evalExpr(Call(Name(F), ARG), N, P)
        => evalExpr(ARG, N, P) ~> callArg(F, P) ... </k>
  rule <k> IVal(A) ~> callArg(F, P)
        => evalCall(P, F, A) ~> callDone ... </k>
  rule <k> returned(V) ~> callDone => V ... </k>

  rule bin("+", IVal(A), IVal(B)) => IVal(A +Int B)
  rule bin("-", IVal(A), IVal(B)) => IVal(A -Int B)
  rule bin("*", IVal(A), IVal(B)) => IVal(A *Int B)
  rule bin("%", IVal(A), IVal(B)) => IVal(A %Int B)
  rule bin("//", IVal(A), IVal(B)) => IVal(A /Int B)
  rule bin("+", LVal(XS), LVal(YS)) => LVal(append(XS, YS))

  rule append(nil, YS) => YS
  rule append(cons(X, XS), YS) => cons(X, append(XS, YS))
endmodule
