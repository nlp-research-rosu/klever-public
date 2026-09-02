requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Auditor mutation: the real result is pileFrom(N, 0), but this claim
  // deliberately drops the first level from the returned value.
  claim [false-functional-off-by-one]:
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
      VList(pileFrom(N, 1)))))
    requires N >Int 0
endmodule
