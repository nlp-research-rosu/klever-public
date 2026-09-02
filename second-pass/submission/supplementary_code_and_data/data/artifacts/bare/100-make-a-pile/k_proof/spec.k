requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [invariant-initialization]:
    goal(proof(evalStmts(
      Assign(Name("result"), ListExpr(.Exprs))
      Assign(Name("i"), BinOp("-", Name("n"), Int(1))),
      "n" |-> VInt(N))))
  =>
    goal(proof(Normal(
      "i" |-> VInt(N -Int 1)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, N)))))
    requires N >Int 0

  claim [invariant-preservation]:
    goal(proof(evalStmts(
      Assign(Name("result"),
        BinOp("+",
          ListExpr(BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))),
          Name("result")))
      Assign(Name("i"), BinOp("-", Name("i"), Int(1))),
      "i" |-> VInt(I)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, I +Int 1)))))
  =>
    goal(proof(Normal(
      "i" |-> VInt(I -Int 1)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, I)))))
    requires N >Int 0 andBool I >=Int 0 andBool I <Int N

  claim [invariant-exit]:
    goal(proof(evalStmts(
      Return(Name("result")),
      "i" |-> VInt(-1)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, 0)))))
  =>
    goal(proof(Returned(
      "i" |-> VInt(-1)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, 0)),
      VList(pileFrom(N, 0)))))
    requires N >Int 0

  // The invariant says that result is precisely the already-built suffix.
  claim [loop-invariant]:
    goal(proof(evalLoop(
      Compare(Name("i"), CmpOp(">=", Int(0))),
      Assign(Name("result"),
        BinOp("+",
          ListExpr(BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))),
          Name("result")))
      Assign(Name("i"), BinOp("-", Name("i"), Int(1))),
      Return(Name("result")),
      "i" |-> VInt(I)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, I +Int 1)))))
  =>
    goal(proof(Returned(
      "i" |-> VInt(-1)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, 0)),
      VList(pileFrom(N, 0)))))
    requires N >Int 0 andBool I >=Int -1 andBool I <Int N

  // The translated source program returns all n terms N, N+2, ..., N+2(n-1).
  claim [functional-correctness]:
    goal(proof(evalEntry(
      Module(
        FuncDef("make_a_pile", Params("n"),
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("i"), BinOp("-", Name("n"), Int(1)))
          While(Compare(Name("i"), CmpOp(">=", Int(0))),
            Assign(Name("result"),
              BinOp("+",
                ListExpr(BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))),
                Name("result")))
            Assign(Name("i"), BinOp("-", Name("i"), Int(1))))
          Return(Name("result")))),
      N)))
  =>
    goal(proof(Returned(
      "i" |-> VInt(-1)
      "n" |-> VInt(N)
      "result" |-> VList(pileFrom(N, 0)),
      VList(pileFrom(N, 0)))))
    requires N >Int 0
endmodule
