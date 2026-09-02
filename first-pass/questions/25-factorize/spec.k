// spec.k — factorize on the UNIFIED semantics (src/). Trial-division while invariant + entry. See
// ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module FACTORIZE-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FACTORIZE-SPEC

requires "verification.k"

module FACTORIZE-SPEC
  imports FACTORIZE-VERIFICATION

  // ---- Loop invariant — trial-division factor list. From (fact=list(ACC), n=NV, i=IV) the loop leaves
  // fact := list(factorList(NV, IV, ACC)); n/i havoc'd. The body's If splits on `n%i==0` (divide vs.
  // increment), matching factorList's two non-base rules; `fact = fact + [i]` = valSeqConcat. Scope:
  // {fact, n, i}.
  claim
    <k>
      #while(Compare(Name("i"), CmpOp("<=", Name("n"))),
        If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
          Assign(Name("fact"), BinOp("+", Name("fact"), ListExpr(Name("i"))))
          Assign(Name("n"), BinOp("//", Name("n"), Name("i"))),
          Assign(Name("i"), BinOp("+", Name("i"), Int(1)))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "factorize" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "fact" <- ref(HN1_0:Int) ] [ "n" <- NV:Int ] [ "i" <- IV:Int ], parent(0)) =>
        scope(.Map [ "fact" <- ref(?HN1_0B:Int) ] [ "n" <- ?_:Val ] [ "i" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <heap> (HN1_0 |-> list(ACC:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(factorList(NV, IV, ACC))) ?FRESH1:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLC2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires IV >=Int 2 andBool NV >=Int 0
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    ensures 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLC2 andBool HLC1 <=Int ?HLC2
     andBool keysBelow(?FRESH1, ?HLC2)
     andBool notBool (?HN1_0B in_keys(?FRESH1))
     andBool notBool (?HN1_0B in_keys(HRST1))
    [all-path]

  // ---- Entry — result = factorize(N) == factorizeRes(N) = list(factorList(N, 2, .)): the ascending
  // prime factorization of N. Domain N >= 0 (the trial-division list is total for any N >= 0).
  claim
    <k>
      FuncDef("factorize", Params("n"),
        Assign(Name("fact"), ListExpr(.Exprs))
        Assign(Name("i"), Int(2))
        While(Compare(Name("i"), CmpOp("<=", Name("n"))),
          If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("fact"), BinOp("+", Name("fact"), ListExpr(Name("i"))))
            Assign(Name("n"), BinOp("//", Name("n"), Name("i"))),
            Assign(Name("i"), BinOp("+", Name("i"), Int(1)))))
        Return(Name("fact")))
      Assign(Name("result"), Call(Name("factorize"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "factorize" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(factorList(N, 2, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
