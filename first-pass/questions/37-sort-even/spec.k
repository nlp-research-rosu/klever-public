// spec.k — sort_even on the UNIFIED semantics (src/). Gather even-index invariant + interleave-build
// invariant (indexing the trusted sorted list, Q70 fresh-sorted pattern) + entry. See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module SORT-EVEN-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SORT-EVEN-SPEC

requires "verification.k"

module SORT-EVEN-SPEC
  imports SORT-EVEN-VERIFICATION

  // ---- GATHER loop invariant — `for k in range(0,n): if k%2==0: evens += [l[k]]`.
  claim
    <k>
      #loop(rangeObj(K:Int, N:Int, 1), Name("k"),
        If(Compare(BinOp("%", Name("k"), Int(2)), CmpOp("==", Int(0))),
          Assign(Name("evens"), BinOp("+", Name("evens"), ListExpr(Subscript(Name("l"), Name("k"))))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "sort_even" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "l" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "evens" <- ref(HN1_0:Int) ]
                              [ "se" <- SV:Val ] [ "ans" <- AV:Val ] [ "k" <- _:Val ] [ "i" <- IV:Val ], parent(0))
               => scope(.Map [ "l" <- list(VS) ] [ "n" <- N ] [ "evens" <- ref(?HN1_0B:Int) ]
                              [ "se" <- SV ] [ "ans" <- AV ] [ "k" <- ?_:Val ] [ "i" <- IV ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <heap> (HN1_0 |-> list(TACC:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(strideFold(K, N, VS, TACC))) ?FRESHG:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLCG:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires K >=Int 0
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    ensures 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLCG andBool HLC1 <=Int ?HLCG
     andBool keysBelow(?FRESHG, ?HLCG)
     andBool notBool (?HN1_0B in_keys(?FRESHG))
     andBool notBool (?HN1_0B in_keys(HRST1))
    [all-path]

  // ---- BUILD loop invariant — `for i in range(0,n): if i%2==0: ans += [se[i//2]] else: ans += [l[i]]`.
  // se = list(ST) FRESH (only indexed).
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
          Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Subscript(Name("se"), BinOp("//", Name("i"), Int(2)))))),
          Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Subscript(Name("l"), Name("i")))))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "sort_even" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "l" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "evens" <- THV:Val ]
                              [ "se" <- ref(HN2_1:Int) ] [ "ans" <- ref(HN2_0:Int) ] [ "k" <- KV:Val ] [ "i" <- _:Val ], parent(0))
               => scope(.Map [ "l" <- list(VS) ] [ "n" <- N ] [ "evens" <- THV ]
                              [ "se" <- ref(?HN2_1B:Int) ] [ "ans" <- ref(?HN2_0B:Int) ] [ "k" <- KV ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <heap> (HN2_0 |-> list(AACC:ValSeq)) (HN2_1 |-> list(ST:ValSeq)) HRST2:Map
        => (?HN2_0B |-> list(buildFold(I, N, VS, ST, AACC))) (?HN2_1B |-> list(ST)) ?FRESHB:Map HRST2 </heap>
    <heapLoc> HLC2:Int => ?HLCB:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0
     andBool 0 <=Int HN2_0 andBool HN2_0 <Int HLC2 andBool 0 <=Int HN2_1 andBool HN2_1 <Int HLC2 andBool keysBelow(HRST2, HLC2)
     andBool notBool (HN2_0 ==Int HN2_1)
     andBool notBool (HN2_0 in_keys(HRST2))
     andBool notBool (HN2_1 in_keys(HRST2))
    ensures 0 <=Int ?HN2_0B andBool ?HN2_0B <Int ?HLCB andBool HLC2 <=Int ?HLCB
     andBool 0 <=Int ?HN2_1B andBool ?HN2_1B <Int ?HLCB
     andBool notBool (?HN2_0B ==Int ?HN2_1B)
     andBool keysBelow(?FRESHB, ?HLCB)
     andBool notBool (?HN2_0B in_keys(?FRESHB)) andBool notBool (?HN2_0B in_keys(HRST2))
     andBool notBool (?HN2_1B in_keys(?FRESHB)) andBool notBool (?HN2_1B in_keys(HRST2))
    [all-path]

  // ---- Entry claim — result = sort_even(list(VS)) == list(buildFold(0, len, VS, sortVS(stride), .)),
  // stride = strideFold(0, len, VS, .ValSeq).
  claim
    <k>
      FuncDef("sort_even", Params("l"),
        Assign(Name("n"), Call(Name("len"), Name("l")))
        Assign(Name("evens"), ListExpr(.Exprs))
        Assign(Name("se"), ListExpr(.Exprs))
        Assign(Name("ans"), ListExpr(.Exprs))
        Assign(Name("k"), Int(0))
        Assign(Name("i"), Int(0))
        For(Name("k"), Call(Name("range"), (Int(0), Name("n"))),
          If(Compare(BinOp("%", Name("k"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("evens"), BinOp("+", Name("evens"), ListExpr(Subscript(Name("l"), Name("k"))))),
            .Stmts))
        Assign(Name("se"), Call(Name("sorted"), Name("evens")))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Subscript(Name("se"), BinOp("//", Name("i"), Int(2)))))),
            Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Subscript(Name("l"), Name("i")))))))
        Return(Name("ans")))
      Assign(Name("result"), Call(Name("sort_even"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sort_even" <- ?_:Val ]
                       [ "result" <- ref(?HN3_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN3_0 |-> list(buildFold(0, vsLen(VS), VS, sortVS(strideFold(0, vsLen(VS), VS, .ValSeq)), .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
