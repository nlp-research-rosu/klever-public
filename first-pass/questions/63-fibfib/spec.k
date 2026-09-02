// spec.k — the reachability claims kprove discharges. On the UNIFIED semantics.
//
//   kompile verification.k --backend haskell \
//     --main-module FIBFIB-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FIBFIB-SPEC

requires "verification.k"

module FIBFIB-SPEC
  imports FIBFIB-VERIFICATION

  // ---- Loop invariant (the circularity) — induction on the count (HI - I) -----
  // Running `for _ in range(...)` with body `a, b, c = b, c, a + b + c` over a symbolic
  // rangeObj(I, HI, 1) slides the 3-window exactly (HI - I) times, leaving
  //   a := winA(HI-I, A,B,C),  b := winB(HI-I, A,B,C),  c := winC(HI-I, A,B,C).
  // kprove splits I into >=HI (base: empty range, window unchanged, winX(K<=0,…)=X) and
  // <HI (step: bind _:=I, run `a,b,c=b,c,(a+b)+c` -> [B,C,(A+B)+C], recurse on I+1; the
  // winX step rules match the slid window).  Body has no return, so the loop runs to
  // completion and the window lands in <scopes>; the <k> ends in `.K`.  (cf. 55-fib.)
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("_"),
        Assign(TupleExpr(Name("a"), Name("b"), Name("c")),
               TupleExpr(Name("b"), Name("c"),
                 BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Int ]
                            [ "a" <- A:Int ] [ "b" <- B:Int ] [ "c" <- C:Int ]
                            [ "_" <- _:Val ], P:Parent)
               => scope(.Map [ "n" <- NV ]
                            [ "a" <- winA(HI -Int I, A, B, C) ]
                            [ "b" <- winB(HI -Int I, A, B, C) ]
                            [ "c" <- winC(HI -Int I, A, B, C) ]
                            [ "_" <- ?_:Val ], P) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = fibfib(N)` (for N >= 0), the root scope's result = fibfibOf(N) =
  // winA(N, 0, 0, 1) — the N-th fibfib number (range(N) slides the seed [0,0,1] N times,
  // returning the first component).  Domain: N >= 0.
  claim
    <k>
      FuncDef("fibfib", Params("n"),
        Assign(TupleExpr(Name("a"), Name("b"), Name("c")), TupleExpr(Int(0), Int(0), Int(1)))
        For(Name("_"), Call(Name("range"), Name("n")),
          Assign(TupleExpr(Name("a"), Name("b"), Name("c")),
                 TupleExpr(Name("b"), Name("c"),
                   BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")))))
        Return(Name("a")))
      Assign(Name("result"), Call(Name("fibfib"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fibfib" <- ?_:Val ] [ "result" <- fibfibOf(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
