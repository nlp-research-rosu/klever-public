// spec.k — is_prime reachability claims on the UNIFIED semantics (src/).
// The divisor scan `for k in range(2, n-1)` is a range For loop over rangeObj(2, N-1, 1)
// with a Bool accumulator `prime`. See ./PROOF.md; range-For template: ../139-special-factorial.
//
//   kompile verification.k --backend haskell \
//     --main-module IS-PRIME-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module IS-PRIME-SPEC

requires "verification.k"

module IS-PRIME-SPEC
  imports IS-PRIME-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(I, HI, 1) from prime = P the divisor
  // scan leaves prime := primeAcc(N, I, HI, P). Induction on the range: #iterNext splits
  // I<HI (bind k:=I, run `if n%k==0: prime=False`, recurse on (I+1,HI)) vs I>=HI (done, P).
  // `k` is pre-bound so the scope shape is stable whether or not the range is empty.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("k"),
        If(Compare(BinOp("%", Name("n"), Name("k")), CmpOp("==", Int(0))),
           Assign(Name("prime"), Bool(false)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- N:Int ] [ "prime" <- P:Bool ] [ "k" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- N ] [ "prime" <- primeAcc(N, I, HI, P) ] [ "k" <- ?_:Val ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — after `result = is_prime(N)`, result == primeAcc(N, 2, N-1, N>=2):
  // N is prime iff N>=2 and no divisor in [2, N-1). Total over all N (empty range for N<=3
  // gives the seed N>=2, correct for N<2 -> false and N in {2,3} -> true).
  claim
    <k>
      FuncDef("is_prime", Params("n"),
        Assign(Name("prime"), Compare(Name("n"), CmpOp(">=", Int(2))))
        Assign(Name("k"), Int(0))
        For(Name("k"), Call(Name("range"), (Int(2), BinOp("-", Name("n"), Int(1)))),
          If(Compare(BinOp("%", Name("n"), Name("k")), CmpOp("==", Int(0))),
             Assign(Name("prime"), Bool(false)),
             .Stmts))
        Return(Name("prime")))
      Assign(Name("result"), Call(Name("is_prime"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_prime" <- ?_:Val ]
                       [ "result" <- primeAcc(N, 2, N -Int 1, N >=Int 2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
