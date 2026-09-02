// spec.k — strange_sort_list on the UNIFIED semantics (trusted sorted, mpy-sort.k). The sorted
// list s = list(SS) is a FRESH variable in the loop invariant (only INDEXED via total valSeqAt,
// never iterated); the entry instantiates SS := sortVS(LST). See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module STRANGE-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module STRANGE-SPEC

requires "verification.k"

module STRANGE-SPEC
  imports STRANGE-VERIFICATION

  // ---- Loop invariant — over rangeObj(I, N, 1) from res = list(RACC) the loop leaves res :=
  // list(reconFoldV(I, N, SS, RACC)). s = list(SS) FRESH (only indexed); `lst` is generic (LV,
  // unused in the loop). `requires I >=Int 0` so the // lemma collapses i//2.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
          Assign(Name("res"), BinOp("+", Name("res"), ListExpr(Subscript(Name("s"), BinOp("//", Name("i"), Int(2)))))),
          Assign(Name("res"), BinOp("+", Name("res"),
            ListExpr(Subscript(Name("s"), BinOp("-", BinOp("-", Name("n"), Int(1)), BinOp("//", Name("i"), Int(2)))))))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "strange_sort_list" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "lst" <- LV:Val ] [ "n" <- N:Int ] [ "s" <- ref(HN1_1:Int) ]
                             [ "res" <- ref(HN1_0:Int) ] [ "i" <- _:Val ], parent(0))
               => scope(.Map [ "lst" <- LV ] [ "n" <- N ] [ "s" <- ref(?HN1_1B:Int) ]
                             [ "res" <- ref(?HN1_0B:Int) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <heap> (HN1_0 |-> list(RACC:ValSeq)) (HN1_1 |-> list(SS:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(reconFoldV(I, N, SS, RACC))) (?HN1_1B |-> list(SS)) ?FRESH1:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLCB:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool N ==Int vsLen(SS)
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

  // ---- Entry claim — after `result = strange_sort_list(list(LST))`, result == strangeRes(LST) =
  // list(reconFoldV(0, vsLen(LST), sortVS(LST), .ValSeq)). The loop-inv applies with SS :=
  // sortVS(LST), N := vsLen(LST).
  claim
    <k>
      FuncDef("strange_sort_list", Params("lst"),
        Assign(Name("n"), Call(Name("len"), Name("lst")))
        Assign(Name("s"), Call(Name("sorted"), Name("lst")))
        Assign(Name("res"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("res"), BinOp("+", Name("res"), ListExpr(Subscript(Name("s"), BinOp("//", Name("i"), Int(2)))))),
            Assign(Name("res"), BinOp("+", Name("res"),
              ListExpr(Subscript(Name("s"), BinOp("-", BinOp("-", Name("n"), Int(1)), BinOp("//", Name("i"), Int(2)))))))))
        Return(Name("res")))
      Assign(Name("result"), Call(Name("strange_sort_list"), list(LST:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "strange_sort_list" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(reconFoldV(0, vsLen(LST), sortVS(LST), .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
