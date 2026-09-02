requires "verification.k"

module FIBFIB-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")" [symbol(moduleAst)]

  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(funcDefAst)]
                | "Assign" "(" Expr "," Expr ")" [symbol(assignAst)]
                | "While" "(" Expr "," Stmts ")" [symbol(whileAst)]
                | "Return" "(" Expr ")" [symbol(returnAst)]

  syntax Params ::= "Params" "(" Strings ")" [symbol(paramsAst)]
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")" [symbol(nameAst)]
                | "Int" "(" Int ")" [symbol(intAst)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(binOpAst)]
                | "Compare" "(" Expr "," CmpOps ")" [symbol(compareAst)]
                | "TupleExpr" "(" Exprs ")" [symbol(tupleExprAst)]

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(cmpOpAst)]
  syntax CmpOps ::= List{CmpOp, ","}
endmodule

module FIBFIB
  imports FIBFIB-SYNTAX
  imports FIBFIB-VERIFICATION
  imports INT
  imports BOOL
  imports MAP

  syntax KItem ::= "invoke" "(" Int ")"
                 | "finish"
                 | "assignTo" "(" String ")"
                 | "binRhs" "(" String "," Expr ")"
                 | "applyBin" "(" String "," Int ")"
                 | "compareRhs" "(" String "," Expr ")"
                 | "applyCompare" "(" String "," Int ")"
                 | "tupleSecond" "(" String "," String "," String "," Expr "," Expr ")"
                 | "tupleThird" "(" String "," String "," String "," Int "," Expr ")"
                 | "tupleStore" "(" String "," String "," String "," Int "," Int ")"
                 | "whileDecision" "(" Expr "," Stmts ")"
                 | "returnValue"

  syntax KResult ::= Int | Bool

  configuration
    <fibfib>
      <k> $PGM:Pgm ~> invoke($N:Int) </k>
      <env> .Map </env>
      <result> 0 </result>
    </fibfib>

  rule <k> Module(FuncDef("fibfib", Params("n"), BODY)) ~> invoke(N)
        => BODY ~> finish ... </k>
       <env> .Map => "n" |-> N </env>

  rule <k> (S:Stmt REST:Stmts => S ~> REST) ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> Int(I) => I ... </k>
  rule <k> Name(X) => I ... </k>
       <env>... X |-> I ...</env>

  rule <k> BinOp(OP, E1, E2) => E1 ~> binRhs(OP, E2) ... </k>
  rule <k> I:Int ~> binRhs(OP, E2) => E2 ~> applyBin(OP, I) ... </k>
  rule <k> I2:Int ~> applyBin("+", I1) => I1 +Int I2 ... </k>

  rule <k> Compare(E1, CmpOp(OP, E2)) => E1 ~> compareRhs(OP, E2) ... </k>
  rule <k> I1:Int ~> compareRhs(OP, E2) => E2 ~> applyCompare(OP, I1) ... </k>
  rule <k> I2:Int ~> applyCompare("<", I1) => I1 <Int I2 ... </k>

  rule <k> Assign(Name(X), E) => E ~> assignTo(X) ... </k>
  rule <k> I:Int ~> assignTo(X) => .K ... </k>
       <env> M => M [ X <- I ] </env>

  rule <k> Assign(TupleExpr(Name(A), Name(B), Name(C)), TupleExpr(E1, E2, E3))
        => E1 ~> tupleSecond(A, B, C, E2, E3) ... </k>
  rule <k> I1:Int ~> tupleSecond(A, B, C, E2, E3)
        => E2 ~> tupleThird(A, B, C, I1, E3) ... </k>
  rule <k> I2:Int ~> tupleThird(A, B, C, I1, E3)
        => E3 ~> tupleStore(A, B, C, I1, I2) ... </k>
  rule <k> I3:Int ~> tupleStore(A, B, C, I1, I2) => .K ... </k>
       <env> M => M [ A <- I1 ] [ B <- I2 ] [ C <- I3 ] </env>

  rule <k> While(COND, BODY) => COND ~> whileDecision(COND, BODY) ... </k>
  rule <k> true ~> whileDecision(COND, BODY)
        => BODY ~> While(COND, BODY) ... </k>
  rule <k> false ~> whileDecision(_, _) => .K ... </k>

  rule <k> Return(E) => E ~> returnValue ... </k>
  rule <k> I:Int ~> returnValue ~> .Stmts ~> finish => .K </k>
       <result> _ => I </result>
  rule <k> I:Int ~> returnValue ~> finish => .K </k>
       <result> _ => I </result>
endmodule
