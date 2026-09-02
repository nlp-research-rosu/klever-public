// spec.k — sort_array on the UNIFIED semantics. Loop invariant (rev-branched loop-index sort
// reconstruction, rev carried abstractly) + entry (computes the parity flag via the isInt echo,
// case-splits on it). See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module SORT-ARRAY-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SORT-ARRAY-SPEC

requires "verification.k"

module SORT-ARRAY-SPEC
  imports SORT-ARRAY-VERIFICATION

  // ---- Loop invariant — over rangeObj(I, N, 1) the loop leaves res := sortArrFold(REV, I, N,
  // SS, RACC).  s = list(SS) FRESH (only indexed); rev = REV carried abstractly (the If(rev)
  // body case-splits, matching sortArrFold's true/false rules); array/n loop-constant.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Name("rev"),
          Assign(Name("res"), BinOp("+", Name("res"), ListExpr(Subscript(Name("s"), BinOp("-", BinOp("-", Name("n"), Int(1)), Name("i")))))),
          Assign(Name("res"), BinOp("+", Name("res"), ListExpr(Subscript(Name("s"), Name("i")))))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "sort_array" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "array" <- AV:Val ] [ "n" <- N:Int ] [ "rev" <- REV:Bool ]
                              [ "s" <- ref(HN1_1:Int) ] [ "res" <- ref(HN1_0:Int) ] [ "i" <- _:Val ], parent(0))
               => scope(.Map [ "array" <- AV ] [ "n" <- N ] [ "rev" <- REV ]
                              [ "s" <- ref(HN1_1) ] [ "res" <- ref(?HN1_0B:Int) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <heap> (HN1_0 |-> list(RACC:ValSeq)) (HN1_1 |-> list(SS:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(sortArrFold(REV, I, N, SS, RACC))) (HN1_1 |-> list(SS)) ?FRESH1:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLC2:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool N ==Int vsLen(SS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool 0 <=Int HN1_1 andBool HN1_1 <Int HLC1
     andBool notBool (HN1_0 ==Int HN1_1)
     andBool notBool (HN1_0 in_keys(HRST1))
     andBool notBool (HN1_1 in_keys(HRST1)) andBool keysBelow(HRST1, HLC1)
    ensures 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLC2 andBool HLC1 <=Int ?HLC2
     andBool notBool (?HN1_0B ==Int HN1_1)
     andBool keysBelow(?FRESH1, ?HLC2)
     andBool notBool (?HN1_0B in_keys(?FRESH1)) andBool notBool (?HN1_0B in_keys(HRST1))
     andBool notBool (HN1_1 in_keys(?FRESH1))
    [all-path]

  // ---- Entry claim — after `result = sort_array(list(VS))`, result == sortArrRes(VS). The
  // n==0 guard is skipped (domain vsLen(VS) >= 1); rev is computed via the echo; the loop-inv
  // applies with REV := sortArrRev(VS), SS := sortVS(VS), N := vsLen(VS).
  claim
    <k>
      FuncDef("sort_array", Params("array"),
        Assign(Name("n"), Call(Name("len"), Name("array")))
        If(Compare(Name("n"), CmpOp("==", Int(0))), Return(ListExpr(.Exprs)), .Stmts)
        Assign(Name("rev"),
          Compare(BinOp("%", BinOp("+", Subscript(Name("array"), Int(0)), Subscript(Name("array"), UnaryOp("-", Int(1)))), Int(2)),
            CmpOp("==", Int(0))))
        Assign(Name("s"), Call(Name("sorted"), Name("array")))
        Assign(Name("res"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          If(Name("rev"),
            Assign(Name("res"), BinOp("+", Name("res"), ListExpr(Subscript(Name("s"), BinOp("-", BinOp("-", Name("n"), Int(1)), Name("i")))))),
            Assign(Name("res"), BinOp("+", Name("res"), ListExpr(Subscript(Name("s"), Name("i")))))))
        Return(Name("res")))
      Assign(Name("result"), Call(Name("sort_array"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sort_array" <- ?_:Val ] [ "result" <- ref(?RR:Int) ], parent(-1))
    </scopes>
    <heap> .Map
        => (?RR |-> list(sortArrFold(sortArrRev(VS), 0, vsLen(VS), sortVS(VS), .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool vsLen(VS) >=Int 1
    [all-path]
endmodule
