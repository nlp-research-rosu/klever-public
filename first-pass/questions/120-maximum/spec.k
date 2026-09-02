// spec.k — maximum on the UNIFIED semantics (trusted sorted, mpy-sort.k). The sorted
// list s = list(SS) is a FRESH variable in the loop invariant (only INDEXED via total
// valSeqAt, never iterated); the entry instantiates SS := sortVS(ARR). See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module MAXIMUM-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module MAXIMUM-SPEC

requires "verification.k"

module MAXIMUM-SPEC
  imports MAXIMUM-VERIFICATION

  // ---- Loop invariant — over rangeObj(J, K, 1) from res = list(RACC) the loop leaves
  // res := list(maxFold(J, K, N, SS, RACC)). s = list(SS) FRESH (only indexed); `arr` is
  // generic (AV). Carries <stack> _STK:List so it folds a loop inside the function frame.
  claim
    <k>
      #loop(rangeObj(J:Int, K:Int, 1), Name("j"),
        Assign(Name("res"), BinOp("+", Name("res"),
          ListExpr(Subscript(Name("s"), BinOp("+", BinOp("-", Name("n"), Name("k")), Name("j")))))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "maximum" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "arr" <- AV:Val ] [ "k" <- K:Int ] [ "n" <- N:Int ] [ "s" <- ref(HN1_1:Int) ]
                             [ "res" <- ref(HN1_0:Int) ] [ "j" <- _:Val ], parent(0))
               => scope(.Map [ "arr" <- AV ] [ "k" <- K ] [ "n" <- N ] [ "s" <- ref(?HN1_1B:Int) ]
                             [ "res" <- ref(?HN1_0B:Int) ] [ "j" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <heap> (HN1_0 |-> list(RACC:ValSeq)) (HN1_1 |-> list(SS:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(maxFold(J, K, N, SS, RACC))) (?HN1_1B |-> list(SS)) ?FRESH1:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLCB:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires J >=Int 0 andBool N ==Int vsLen(SS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool 0 <=Int HN1_1 andBool HN1_1 <Int HLC1 andBool keysBelow(HRST1, HLC1)
     andBool notBool (HN1_0 ==Int HN1_1)
     andBool notBool (HN1_0 in_keys(HRST1))
     andBool notBool (HN1_1 in_keys(HRST1))
    ensures 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLCB andBool HLC1 <=Int ?HLCB
     andBool 0 <=Int ?HN1_1B andBool ?HN1_1B <Int ?HLCB
     andBool notBool (?HN1_0B ==Int ?HN1_1B)
     andBool keysBelow(?FRESH1, ?HLCB)
     andBool notBool (?HN1_0B in_keys(?FRESH1)) andBool notBool (?HN1_0B in_keys(HRST1))
     andBool notBool (?HN1_1B in_keys(?FRESH1)) andBool notBool (?HN1_1B in_keys(HRST1))
    [all-path]

  // ---- Entry claim — after `result = maximum(list(ARR), K)`, result == maximumRes(ARR, K)
  // = list(maxFold(0, K, vsLen(ARR), sortVS(ARR), .ValSeq)). The loop-inv applies with
  // SS := sortVS(ARR), N := vsLen(ARR). Domain 0 <= K <= len(arr) (the problem's stated range);
  // K = 0 leaves range(0,0) empty so res stays [] (maxFold base case J >= K).
  claim
    <k>
      FuncDef("maximum", Params("arr", "k"),
        Assign(Name("n"), Call(Name("len"), Name("arr")))
        Assign(Name("s"), Call(Name("sorted"), Name("arr")))
        Assign(Name("res"), ListExpr(.Exprs))
        Assign(Name("j"), Int(0))
        For(Name("j"), Call(Name("range"), (Int(0), Name("k"))),
          Assign(Name("res"), BinOp("+", Name("res"),
            ListExpr(Subscript(Name("s"), BinOp("+", BinOp("-", Name("n"), Name("k")), Name("j")))))))
        Return(Name("res")))
      Assign(Name("result"), Call(Name("maximum"), list(ARR:ValSeq), Int(K:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "maximum" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(maxFold(0, K, vsLen(ARR), sortVS(ARR), .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int K andBool K <=Int vsLen(ARR)
    [all-path]
endmodule
