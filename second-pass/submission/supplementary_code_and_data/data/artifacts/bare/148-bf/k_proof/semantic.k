module MPY-SYNTAX
  imports DOMAINS

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Names ")"
  syntax Names ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "TupleExpr" "(" Exprs ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Exprs ::= List{Expr, ","}
endmodule

module MPY
  imports MPY-SYNTAX

  syntax KItem ::= "invokeBF" "(" String "," String ")"
                 | "execStmt" "(" Stmt ")"
  syntax Result ::= "noResult"
                  | "tupleValue" "(" StringValues ")"
  syntax StringValues ::= List{String, ","}

  configuration
    <bf>
      <k> $PGM:Program ~> invokeBF($PLANET1:String, $PLANET2:String) </k>
      <planet1> "" </planet1>
      <planet2> "" </planet2>
      <result> noResult </result>
    </bf>

  rule <k> Module(FuncDef("bf", Params("planet1", "planet2"), BODY))
             ~> invokeBF(P1, P2)
          => BODY
       ... </k>
       <planet1> "" => P1 </planet1>
       <planet2> "" => P2 </planet2>

  rule <k> (S:Stmt REST:Stmts) => execStmt(S) ~> REST ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> execStmt(
             If(Compare(Name("planet1"), CmpOp("==", Str(S))), THEN, _ELSE))
          => THEN
       ... </k>
       <planet1> P1 </planet1>
    requires P1 ==String S

  rule <k> execStmt(
             If(Compare(Name("planet1"), CmpOp("==", Str(S))), _THEN, ELSE))
          => ELSE
       ... </k>
       <planet1> P1 </planet1>
    requires P1 =/=String S

  rule <k> execStmt(
             If(Compare(Name("planet2"), CmpOp("==", Str(S))), THEN, _ELSE))
          => THEN
       ... </k>
       <planet2> P2 </planet2>
    requires P2 ==String S

  rule <k> execStmt(
             If(Compare(Name("planet2"), CmpOp("==", Str(S))), _THEN, ELSE))
          => ELSE
       ... </k>
       <planet2> P2 </planet2>
    requires P2 =/=String S

  rule <k> execStmt(Return(TupleExpr(.Exprs))) ~> _REST => .K </k>
       <result> noResult => tupleValue(.StringValues) </result>

  rule <k> execStmt(Return(TupleExpr(Str(S1)))) ~> _REST => .K </k>
       <result> noResult => tupleValue(S1) </result>

  rule <k> execStmt(Return(TupleExpr(Str(S1), Str(S2)))) ~> _REST => .K </k>
       <result> noResult => tupleValue(S1, S2) </result>

  rule <k> execStmt(Return(TupleExpr(Str(S1), Str(S2), Str(S3))))
          ~> _REST
          => .K
       </k>
       <result> noResult => tupleValue(S1, S2, S3) </result>

  rule <k> execStmt(
             Return(TupleExpr(Str(S1), Str(S2), Str(S3), Str(S4))))
          ~> _REST
          => .K
       </k>
       <result> noResult => tupleValue(S1, S2, S3, S4) </result>

  rule <k> execStmt(
             Return(
               TupleExpr(Str(S1), Str(S2), Str(S3), Str(S4), Str(S5))))
          ~> _REST
          => .K
       </k>
       <result> noResult => tupleValue(S1, S2, S3, S4, S5) </result>

  rule <k> execStmt(
             Return(
               TupleExpr(
                 Str(S1), Str(S2), Str(S3), Str(S4), Str(S5), Str(S6))))
          ~> _REST
          => .K
       </k>
       <result> noResult => tupleValue(S1, S2, S3, S4, S5, S6) </result>
endmodule
