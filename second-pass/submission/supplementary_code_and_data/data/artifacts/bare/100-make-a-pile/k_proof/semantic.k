module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax PyModule ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= "FuncDef" "(" String "," "Params" "(" Strings ")" "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Val ::= "VInt" "(" Int ")"
               | "VBool" "(" Bool ")"
               | "VList" "(" Vals ")"
               | "VNone"
  syntax Vals ::= ".Vals"
                | "VCons" "(" Val "," Vals ")"
  syntax Expr ::= Val

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "assignTo" "(" String ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Val ")"
                 | "makeList" "(" Exprs ")"
                 | "listOne"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareApply" "(" String "," Val ")"
                 | "whileGuard" "(" Expr "," Stmts ")"
                 | "finishReturn"

  syntax Vals ::= vAppend(Vals, Vals) [function]
  rule vAppend(.Vals, YS) => YS
  rule vAppend(VCons(V, XS), YS) => VCons(V, vAppend(XS, YS))

  // A mathematical suffix used only to state functional-correctness claims.
  syntax Vals ::= pileFrom(Int, Int) [function]
  rule pileFrom(N, I) => .Vals
    requires I >=Int N
  rule pileFrom(N, I) => VCons(VInt(N +Int (2 *Int I)), pileFrom(N, I +Int 1))
    requires I <Int N

  configuration
    <mpy>
      <k> $PGM:PyModule </k>
      <n> $N:Int </n>
      <env> .Map </env>
      <result> VNone </result>
    </mpy>

  // Loading the module invokes its sole one-argument entry point using <n>.
  rule <k> Module(FuncDef(_, Params(P, .Strings), BODY)) => exec(BODY) </k>
       <n> N </n>
       <env> .Map => P |-> VInt(N) </env>

  rule exec(.Stmts) => .K
  rule exec(S SS) => S ~> exec(SS)

  rule Int(I) => VInt(I)
  rule <k> Name(X) => V ...</k>
       <env>... X |-> V ...</env>

  rule ListExpr(ES) => makeList(ES)
  rule makeList(.Exprs) => VList(.Vals)
  rule makeList(E, .Exprs) => E ~> listOne
  rule V ~> listOne => VList(VCons(V, .Vals))

  rule BinOp(OP, E1, E2) => E1 ~> binLeft(OP, E2)
  rule V1 ~> binLeft(OP, E2) => E2 ~> binRight(OP, V1)
  rule VInt(R) ~> binRight("+", VInt(L)) => VInt(L +Int R)
  rule VInt(R) ~> binRight("-", VInt(L)) => VInt(L -Int R)
  rule VInt(R) ~> binRight("*", VInt(L)) => VInt(L *Int R)
  rule VList(YS) ~> binRight("+", VList(XS)) => VList(vAppend(XS, YS))

  rule Compare(E1, CmpOp(OP, E2)) => E1 ~> compareLeft(OP, E2)
  rule V1 ~> compareLeft(OP, E2) => E2 ~> compareApply(OP, V1)
  rule VInt(B) ~> compareApply(">=", VInt(A)) => VBool(A >=Int B)

  rule Assign(Name(X), E) => E ~> assignTo(X)
  rule <k> V ~> assignTo(X) => .K ...</k>
       <env> ENV => ENV [ X <- V ] </env>

  rule While(COND, BODY) => COND ~> whileGuard(COND, BODY)
  rule VBool(true) ~> whileGuard(COND, BODY)
    => exec(BODY) ~> While(COND, BODY)
  rule VBool(false) ~> whileGuard(_, _) => .K

  rule Return(E) => E ~> finishReturn
  rule <k> V ~> finishReturn ~> _REST => .K </k>
       <result> _ => V </result>
endmodule
