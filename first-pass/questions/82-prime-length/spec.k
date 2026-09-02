// spec.k — prime_length reachability claims on the UNIFIED semantics (src/). is_prime (reused
// from #31) applied to the symbolic string length isLen(CS). See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module PRIME-LENGTH-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module PRIME-LENGTH-SPEC

requires "verification.k"

module PRIME-LENGTH-SPEC
  imports PRIME-LENGTH-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(I, HI, 1) from prime = P the divisor
  // scan on l leaves prime := primeAcc(L, I, HI, P). `i` pre-bound for a stable scope.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("l"), Name("i")), CmpOp("==", Int(0))),
           Assign(Name("prime"), Bool(false)),
           .Stmts))
    => .K ... </k>
    <env> EL:Int </env>
    <scopes>
      ... EL |-> ( scope(.Map [ "string" <- SV:Val ] [ "l" <- L:Int ] [ "prime" <- P:Bool ] [ "i" <- _:Val ], PR:Parent)
                => scope(.Map [ "string" <- SV ] [ "l" <- L ] [ "prime" <- primeAcc(L, I, HI, P) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — after `result = prime_length(str(CS))`, result == primeAcc(isLen(CS),
  // 2, isLen(CS), isLen(CS)>=2): the string's length is prime. len(str(CS)) = isLen(CS).
  claim
    <k>
      FuncDef("prime_length", Params("string"),
        Assign(Name("l"), Call(Name("len"), Name("string")))
        Assign(Name("prime"), Compare(Name("l"), CmpOp(">=", Int(2))))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(2), Name("l"))),
          If(Compare(BinOp("%", Name("l"), Name("i")), CmpOp("==", Int(0))),
             Assign(Name("prime"), Bool(false)),
             .Stmts))
        Return(Name("prime")))
      Assign(Name("result"), Call(Name("prime_length"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "prime_length" <- ?_:Val ]
                       [ "result" <- primeAcc(isLen(CS), 2, isLen(CS), isLen(CS) >=Int 2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
