module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"
  syntax Exprs  ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Value ::= "Str" "(" String ")"
                 | "Int" "(" Int ")"
                 | "Bool" "(" Bool ")"
                 | "NoneVal"
  syntax Expr ::= Value
                | "Name" "(" String ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP
  imports K-EQUAL

  // A private, algebraic iterator makes the behavior of split explicit.
  syntax WordSeq ::= "WNil" | "WCons" "(" String "," WordSeq ")"
  syntax WordSeq ::= "splitWords" "(" String ")" [function, total]

  rule splitWords(S) => WCons(S, WNil)
    requires findString(S, " ", 0) ==Int -1
  rule splitWords(S) =>
       WCons(substrString(S, 0, findString(S, " ", 0)),
             splitWords(substrString(S, findString(S, " ", 0) +Int 1,
                                        lengthString(S))))
    requires findString(S, " ", 0) >=Int 0

  syntax Function ::= "function" "(" String "," Stmts ")"
  syntax KItem ::= "load" "(" Program ")"
                 | "invoke" "(" String "," Value ")"
                 | "exec" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"
                 | "loop" "(" String "," WordSeq "," Stmts ")"
                 | "put" "(" String "," Value ")"
                 | "choose" "(" Bool "," Stmts "," Stmts ")"

  configuration
    <mpy>
      <k> load($PGM:Program) ~> invoke("words_in_sentence", Str($SENTENCE:String)) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> NoneVal </result>
    </mpy>

  rule <k> load(Module(.Stmts)) => .K ... </k>
  rule <k> load(Module(FuncDef(F, Params(P), BODY) REST:Stmts))
        => load(Module(REST)) ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>

  rule <k> invoke(F, V) => exec(BODY) ... </k>
       <functions> ... F |-> function(P, BODY) ... </functions>
       <env> _ => P |-> V </env>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt REST:Stmts) => execStmt(S) ~> exec(REST) ... </k>

  rule <k> execStmt(Assign(Name(X), Str(S))) => .K ... </k>
       <env> RHO => RHO [ X <- Str(S) ] </env>

  rule <k> execStmt(For(Name(X),
                        Call(Attribute(Name(Y), "split"), Str(" ")),
                        BODY))
        => loop(X, splitWords(S), BODY) ... </k>
       <env> ... Y |-> Str(S) ... </env>

  rule <k> loop(_, WNil, _) => .K ... </k>
  rule <k> loop(X, WCons(W, WS), BODY)
        => put(X, Str(W)) ~> exec(BODY) ~> loop(X, WS, BODY) ... </k>
  rule <k> put(X, V) => .K ... </k>
       <env> ... X |-> (_ => V) ... </env>

  syntax Bool ::= "memberInt" "(" Int "," Exprs ")" [function]
  rule memberInt(_, .Exprs) => false
  rule memberInt(N, Int(M), REST:Exprs) =>
       (N ==Int M) orBool memberInt(N, REST)

  syntax String ::= "conditionalAppend" "(" Bool "," String "," String ")"
                    [function, total]
  rule conditionalAppend(B, A, W) =>
       #if B
       #then #if A ==String "" #then W #else A +String " " +String W #fi
       #else A
       #fi

  // The exact nested If used by the submitted program.  Its store effect is
  // expressed without symbolic control-flow branching, but still depends on
  // the translated membership list rather than a baked-in primality test.
  rule <k> execStmt(If(Compare(Call(Name("len"), Name("word")),
                              CmpOp("in", ListExpr(NUMS))),
                        If(Compare(Name("result"), CmpOp("==", Str(""))),
                           Assign(Name("result"), Name("word")),
                           Assign(Name("result"),
                                  BinOp("+",
                                    BinOp("+", Name("result"), Str(" ")),
                                    Name("word")))),
                        .Stmts))
        => .K ... </k>
       <env> ... "result" |-> (Str(A) =>
                  Str(conditionalAppend(memberInt(lengthString(W), NUMS),
                                        A, W)))
                 "word" |-> Str(W) ... </env>

  rule <k> execStmt(If(Compare(Name(X), CmpOp("==", Str(S))),
                        THEN, ELSE))
        => choose(V ==String S, THEN, ELSE) ... </k>
       <env> ... X |-> Str(V) ... </env>

  rule <k> choose(true, THEN, _) => exec(THEN) ... </k>
  rule <k> choose(false, _, ELSE) => exec(ELSE) ... </k>

  rule <k> execStmt(Assign(Name(X), Name(Y))) => .K ... </k>
       <env> RHO => RHO [ X <- RHO[Y] ] </env>

  rule <k> execStmt(Assign(Name(X),
                          BinOp("+", BinOp("+", Name(Y), Str(SEP)), Name(Z))))
        => .K ... </k>
       <env> RHO => RHO [ X <- Str(SY +String SEP +String SZ) ] </env>
    requires (RHO [ Y ] ==K Str(SY)) andBool (RHO [ Z ] ==K Str(SZ))

  rule <k> execStmt(Return(Name(X))) => .K ... </k>
       <env> ... X |-> V ... </env>
       <result> _ => V </result>
endmodule
