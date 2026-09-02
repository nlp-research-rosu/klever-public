// spec.k — the reachability claims kprove discharges. On the UNIFIED semantics.
//
//   kompile verification.k --backend haskell \
//     --main-module FIB4-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FIB4-SPEC

requires "verification.k"

module FIB4-SPEC
  imports FIB4-VERIFICATION

  // ---- Loop invariant (the circularity) — induction on the count (HI - I) -----
  // Running the sliding window loop `for _ in range(...)` with body
  //   a, b, c, d = b, c, d, a + b + c + d
  // over symbolic bounds slides the 4-window (a,b,c,d) exactly (HI - I) times,
  // leaving a := fibA(HI-I, A,B,C,D), … d := fibD(HI-I, A,B,C,D) (n constant; the
  // loop var `_` ends bound to some index -> ?_).  kprove splits I into >=HI (base:
  // empty range, window unchanged, fibX(K<=0,…)=X) and <HI (step: bind _:=I, run the
  // tuple-unpack -> [B,C,D,((A+B)+C)+D], recurse on I+1; the fibX step rules match the
  // slid window).  Body has no return, so the loop runs to completion and the window
  // lands in <scopes>; the <k> ends in `.K`.  (cf. 24-largest-divisor / 60-sum-to-n.)
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("_"),
        Assign(TupleExpr(Name("a"), Name("b"), Name("c"), Name("d")),
               TupleExpr(Name("b"), Name("c"), Name("d"),
                 BinOp("+", BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")), Name("d")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Int ]
                            [ "a" <- A:Int ] [ "b" <- B:Int ] [ "c" <- C:Int ] [ "d" <- D:Int ]
                            [ "_" <- _:Val ], P:Parent)
               => scope(.Map [ "n" <- NV ]
                            [ "a" <- fibA(HI -Int I, A, B, C, D) ]
                            [ "b" <- fibB(HI -Int I, A, B, C, D) ]
                            [ "c" <- fibC(HI -Int I, A, B, C, D) ]
                            [ "d" <- fibD(HI -Int I, A, B, C, D) ]
                            [ "_" <- ?_:Val ], P) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = fib4(N)`, the root scope's result = fib4Of(N):
  //   N<4  -> 2 if N==2 else 0  (the early-return [0,0,2,0][N]);
  //   N>=4 -> fibD(N-3, 0,0,2,0) = the N-th fib4 number (the loop slides N-3 times
  //           from the seed [0,0,2,0], since range(4, N+1) runs N-3 times).
  // Domain: N >= 0 (the fib4 index domain).
  claim
    <k>
      FuncDef("fib4", Params("n"),
        If(Compare(Name("n"), CmpOp("<", Int(4))),
          Return(IfExp(Compare(Name("n"), CmpOp("==", Int(2))), Int(2), Int(0))),
          .Stmts)
        Assign(TupleExpr(Name("a"), Name("b"), Name("c"), Name("d")),
               TupleExpr(Int(0), Int(0), Int(2), Int(0)))
        For(Name("_"), Call(Name("range"), (Int(4), BinOp("+", Name("n"), Int(1)))),
          Assign(TupleExpr(Name("a"), Name("b"), Name("c"), Name("d")),
                 TupleExpr(Name("b"), Name("c"), Name("d"),
                   BinOp("+", BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")), Name("d")))))
        Return(Name("d")))
      Assign(Name("result"), Call(Name("fib4"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fib4" <- ?_:Val ] [ "result" <- fib4Of(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
