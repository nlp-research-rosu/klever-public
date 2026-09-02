module MPY-SYNTAX
  imports STRING-SYNTAX
  imports INT-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" String ")"
                  | "Params" "(" String "," String "," String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Subscript" "(" Expr "," Index ")"
                | "Call" "(" Expr "," Expr ")"
                | "Call" "(" Expr "," Expr "," Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr
                 | "Slice" "(" Expr "," "NoBound" "," "NoBound" ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports DOMAINS

  syntax StrVals ::= "vals" "(" String ")"
                   | "vals" "(" String "," String "," String ")"

  syntax Function ::= "fun" "(" Params "," Stmts ")"
  syntax Function ::= findFun ( String , Stmts ) [function]
  syntax Map ::= bindParams ( Params , StrVals ) [function, total]
  syntax Stmts ::= appendStmts ( Stmts , Stmts ) [function]

  rule findFun(N, FuncDef(N, P, B) _REST) => fun(P, B)
  rule findFun(N, FuncDef(M, _, _) REST) => findFun(N, REST)
    requires N =/=String M

  rule bindParams(Params(P), vals(V)) => P |-> V
  rule bindParams(Params(P1, P2, P3), vals(V1, V2, V3)) =>
    (P1 |-> V1) (P2 |-> V2) (P3 |-> V3)

  rule appendStmts(.Stmts, SECOND) => SECOND
  rule appendStmts(S:Stmt REST, SECOND) => S appendStmts(REST, SECOND)

  syntax KItem ::= run ( Pgm , String )
                 | invoke ( String , StrVals )
                 | invokeFound ( Function , StrVals )
                 | exec ( Stmts )
                 | eval ( Expr )
                 | val ( String )
                 | boolVal ( Bool )
                 | restore ( Map )
                 | "returnValue"
                 | ifKont ( Stmts , Stmts , Stmts )
                 | plusLeft ( Expr )
                 | plusRight ( String )
                 | indexKont ( Int )
                 | sliceKont ( Int )
                 | compareLeft ( String , Expr )
                 | compareRight ( String , String )
                 | callOne ( String )
                 | callSecond ( String , Expr , Expr )
                 | callThird ( String , String , Expr )
                 | callInvoke ( String , String , String )

  configuration
    <python>
      <k> run($PGM, $INPUT) </k>
      <functions> .Stmts </functions>
      <env> .Map </env>
      <result> "" </result>
    </python>

  rule <k> run(Module(FS), INPUT) => invoke("anti_shuffle", vals(INPUT)) </k>
       <functions> _ => FS </functions>

  rule <k> invoke(N, VS) => invokeFound(findFun(N, FS), VS) ... </k>
       <functions> FS </functions>
  rule <k> invokeFound(fun(P, B), VS) => exec(B) ~> restore(OLD) ... </k>
       <env> OLD => bindParams(P, VS) </env>
  rule <k> val(V) ~> restore(OLD) => val(V) ... </k>
       <env> _ => OLD </env>

  rule <k> exec(Return(E) _REST) => eval(E) ~> returnValue ... </k>
  rule <k> val(V) ~> returnValue => val(V) ... </k>
  rule <k> exec(If(C, THEN, ELSE) REST) =>
             eval(C) ~> ifKont(THEN, ELSE, REST) ...
       </k>
  rule <k> boolVal(B) ~> ifKont(THEN, _, REST) =>
             exec(appendStmts(THEN, REST)) ...
       </k>
    requires B
  rule <k> boolVal(B) ~> ifKont(_, ELSE, REST) =>
             exec(appendStmts(ELSE, REST)) ...
       </k>
    requires notBool B

  rule <k> eval(Str(S)) => val(S) ... </k>
  rule <k> eval(Name(N)) => val(V) ... </k>
       <env> (N |-> V:String) _ </env>

  rule <k> eval(BinOp("+", L, R)) => eval(L) ~> plusLeft(R) ... </k>
  rule <k> val(L) ~> plusLeft(R) => eval(R) ~> plusRight(L) ... </k>
  rule <k> val(R) ~> plusRight(L) => val(L +String R) ... </k>

  rule <k> eval(Subscript(E, Int(I))) => eval(E) ~> indexKont(I) ... </k>
  rule <k> val(S) ~> indexKont(I) => val(substrString(S, I, I +Int 1)) ... </k>
  rule <k> eval(Subscript(E, Slice(Int(I), NoBound, NoBound))) =>
             eval(E) ~> sliceKont(I) ...
       </k>
  rule <k> val(S) ~> sliceKont(I) =>
             val(substrString(S, I, lengthString(S))) ...
       </k>

  rule <k> eval(Compare(L, CmpOp(OP, R))) =>
             eval(L) ~> compareLeft(OP, R) ...
       </k>
  rule <k> val(L) ~> compareLeft(OP, R) =>
             eval(R) ~> compareRight(OP, L) ...
       </k>
  rule <k> val(R) ~> compareRight("==", L) => boolVal(L ==String R) ... </k>
  rule <k> val(R) ~> compareRight("<=", L) => boolVal(L <=String R) ... </k>

  rule <k> eval(Call(Name(N), A)) => eval(A) ~> callOne(N) ... </k>
  rule <k> val(A) ~> callOne(N) => invoke(N, vals(A)) ... </k>
  rule <k> eval(Call(Name(N), A1, A2, A3)) =>
             eval(A1) ~> callSecond(N, A2, A3) ...
       </k>
  rule <k> val(A1) ~> callSecond(N, A2, A3) =>
             eval(A2) ~> callThird(N, A1, A3) ...
       </k>
  rule <k> val(A2) ~> callThird(N, A1, A3) =>
             eval(A3) ~> callInvoke(N, A1, A2) ...
       </k>
  rule <k> val(A3) ~> callInvoke(N, A1, A2) =>
             invoke(N, vals(A1, A2, A3)) ...
       </k>

  rule <k> val(V) => .K </k>
       <result> _ => V </result>
endmodule
