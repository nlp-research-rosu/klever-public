// spec.k — the reachability claims kprove discharges. On the UNIFIED semantics.
//
//   kompile verification.k --backend haskell \
//     --main-module FIB-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FIB-SPEC

requires "verification.k"

module FIB-SPEC
  imports FIB-VERIFICATION

  // ---- Loop invariant (the circularity) — induction on the count (HI - I) -----
  // Running `for _ in range(...)` with body `a, b = b, a + b` over a symbolic
  // rangeObj(I, HI, 1) slides the 2-window exactly (HI - I) times, leaving
  //   a := winA(HI-I, A, B),  b := winB(HI-I, A, B).
  // kprove splits I into >=HI (base: empty range, window unchanged, winX(K<=0,…)=X)
  // and <HI (step: bind _:=I, run `a,b=b,a+b` -> [B, A+B], recurse on I+1; the winX
  // step rules match the slid window).  Body has no return, so the loop runs to
  // completion and the window lands in <scopes>; the <k> ends in `.K`.  (cf. 46-fib4.)
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("_"),
        Assign(TupleExpr(Name("a"), Name("b")),
               TupleExpr(Name("b"), BinOp("+", Name("a"), Name("b")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Int ] [ "a" <- A:Int ] [ "b" <- B:Int ]
                            [ "_" <- _:Val ], P:Parent)
               => scope(.Map [ "n" <- NV ]
                            [ "a" <- winA(HI -Int I, A, B) ]
                            [ "b" <- winB(HI -Int I, A, B) ]
                            [ "_" <- ?_:Val ], P) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = fib(N)` (for N >= 0), the root scope's result = fibOf(N) =
  // winA(N, 0, 1) — the N-th Fibonacci number (range(N) slides the seed [0,1] N times,
  // returning the first component).  Domain: N >= 0 (the fib index domain; range(N) is
  // empty for N <= 0, giving fib(0) = 0).
  claim
    <k>
      FuncDef("fib", Params("n"),
        Assign(TupleExpr(Name("a"), Name("b")), TupleExpr(Int(0), Int(1)))
        For(Name("_"), Call(Name("range"), Name("n")),
          Assign(TupleExpr(Name("a"), Name("b")),
                 TupleExpr(Name("b"), BinOp("+", Name("a"), Name("b")))))
        Return(Name("a")))
      Assign(Name("result"), Call(Name("fib"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fib" <- ?_:Val ] [ "result" <- fibOf(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
