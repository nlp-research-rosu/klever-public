// spec.k — x_or_y reachability claims on the UNIFIED semantics (src/). Divisor scan (reused
// from #31 is_prime) over range(2, n) + a prime? x : y select. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module X-OR-Y-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module X-OR-Y-SPEC

requires "verification.k"

module X-OR-Y-SPEC
  imports X-OR-Y-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(I, HI, 1) from prime = P the divisor
  // scan leaves prime := primeAcc(N, I, HI, P). `k` pre-bound for a stable scope.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("k"),
        If(Compare(BinOp("%", Name("n"), Name("k")), CmpOp("==", Int(0))),
           Assign(Name("prime"), Bool(false)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- N:Int ] [ "x" <- XV:Val ] [ "y" <- YV:Val ]
                             [ "prime" <- P:Bool ] [ "k" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- N ] [ "x" <- XV ] [ "y" <- YV ]
                             [ "prime" <- primeAcc(N, I, HI, P) ] [ "k" <- ?_:Val ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — after `result = x_or_y(N, X, Y)`, result == sel(primeAcc(N, 2, N,
  // N!=1), X, Y): X if N is prime (n!=1 and no divisor in [2,N)), else Y.
  claim
    <k>
      FuncDef("x_or_y", Params("n", "x", "y"),
        Assign(Name("prime"), Compare(Name("n"), CmpOp("!=", Int(1))))
        Assign(Name("k"), Int(0))
        For(Name("k"), Call(Name("range"), (Int(2), Name("n"))),
          If(Compare(BinOp("%", Name("n"), Name("k")), CmpOp("==", Int(0))),
             Assign(Name("prime"), Bool(false)),
             .Stmts))
        If(Name("prime"),
          Assign(Name("ans"), Name("x")),
          Assign(Name("ans"), Name("y")))
        Return(Name("ans")))
      Assign(Name("result"), Call(Name("x_or_y"), Int(N:Int), Int(X:Int), Int(Y:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "x_or_y" <- ?_:Val ]
                       [ "result" <- sel(primeAcc(N, 2, N, N =/=Int 1), X, Y) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
