requires "semantic.k"

module VERIFICATION
  imports MPY
  imports K-EQUAL

  // A cell-free big-step presentation of the same semantics.  Keeping the
  // state explicit makes reachability claims independent of cell elaboration.
  syntax Val ::= evalExpr(Expr, Map) [function]
  syntax Val ::= evalBin(String, Val, Val) [function]
  syntax Val ::= evalCmp(String, Val, Val) [function]

  rule evalExpr(Int(I), _) => VInt(I)
  rule evalExpr(Name(X), (X |-> V) _REST) => V
  rule evalExpr(ListExpr(.Exprs), _) => VList(.Vals)
  rule evalExpr(ListExpr(E, .Exprs), ENV)
    => VList(VCons(evalExpr(E, ENV), .Vals))
  rule evalExpr(BinOp(OP, L, R), ENV)
    => evalBin(OP, evalExpr(L, ENV), evalExpr(R, ENV))
  rule evalExpr(Compare(L, CmpOp(OP, R)), ENV)
    => evalCmp(OP, evalExpr(L, ENV), evalExpr(R, ENV))

  rule evalBin("+", VInt(A), VInt(B)) => VInt(A +Int B)
  rule evalBin("-", VInt(A), VInt(B)) => VInt(A -Int B)
  rule evalBin("*", VInt(A), VInt(B)) => VInt(A *Int B)
  rule evalBin("+", VList(XS), VList(YS)) => VList(vAppend(XS, YS))
  rule evalCmp(">=", VInt(A), VInt(B)) => VBool(A >=Int B)

  syntax Outcome ::= "Normal" "(" Map ")"
                   | "Returned" "(" Map "," Val ")"
  syntax Outcome ::= evalStmts(Stmts, Map) [function]
                   | evalLoop(Expr, Stmts, Stmts, Map)
                   | evalEntry(PyModule, Int) [function]
  syntax Proof ::= "proof" "(" Outcome ")" [function]
  syntax Goal ::= "goal" "(" Proof ")"

  rule evalStmts(.Stmts, ENV) => Normal(ENV)
  rule evalStmts(Assign(Name(X), E) REST, ENV)
    => evalStmts(REST, ENV [ X <- evalExpr(E, ENV) ])
  rule evalStmts(Return(E) _REST, ENV)
    => Returned(ENV, evalExpr(E, ENV))
  rule evalStmts(While(COND, BODY) REST, ENV)
    => evalLoop(COND, BODY, REST, ENV)

  // Loop-invariant summary.  Its initialization, preservation, and exit
  // obligations are stated and proved independently in spec.k.
  rule proof(evalLoop(
         Compare(Name("i"), CmpOp(">=", Int(0))),
         Assign(Name("result"),
           BinOp("+",
             ListExpr(BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))),
             Name("result")))
         Assign(Name("i"), BinOp("-", Name("i"), Int(1))),
         Return(Name("result")),
         "i" |-> VInt(I)
         "n" |-> VInt(N)
         "result" |-> VList(ACC)))
    => proof(Returned(
         "i" |-> VInt(-1)
         "n" |-> VInt(N)
         "result" |-> VList(pileFrom(N, 0)),
         VList(pileFrom(N, 0))))
    requires N >Int 0 andBool I >=Int -1 andBool I <Int N
         andBool (ACC ==K pileFrom(N, I +Int 1))
    [simplification]

  rule evalEntry(
         Module(FuncDef(_, Params(P, .Strings), BODY)), N)
    => evalStmts(BODY, P |-> VInt(N))
endmodule
