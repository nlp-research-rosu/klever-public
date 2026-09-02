// spec.k — tri on the UNIFIED semantics (src/). Range-loop list-build invariant + entry. See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module TRI-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module TRI-SPEC

requires "verification.k"

module TRI-SPEC
  imports TRI-VERIFICATION

  // ---- Loop invariant — over rangeObj(I, HI, 1) from my_tri = list(ACC) the loop appends each term,
  // sliding the pair (a,b). Leaves my_tri := list(triFold(I, HI, A, B, ACC)); a/b/c/i havoc'd. The body's
  // If splits on `i%2==0` (even/odd), matching triFold's two non-base rules. Scope: {n, my_tri, a, b, c, i}.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
          Assign(Name("c"), BinOp("+", BinOp("//", Name("i"), Int(2)), Int(1))),
          Assign(Name("c"),
            BinOp("+", BinOp("+", Name("b"), Name("a")), BinOp("//", BinOp("+", Name("i"), Int(3)), Int(2)))))
        Assign(Name("my_tri"), BinOp("+", Name("my_tri"), ListExpr(Name("c"))))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("c")))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "tri" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "n" <- NV:Val ] [ "my_tri" <- ref(HN1_0:Int) ] [ "a" <- A:Int ] [ "b" <- B:Int ]
                   [ "c" <- _:Val ] [ "i" <- _:Val ], parent(0)) =>
        scope(.Map [ "n" <- NV ] [ "my_tri" <- ref(?HN1_0B:Int) ] [ "a" <- ?_:Val ]
                   [ "b" <- ?_:Val ] [ "c" <- ?_:Val ] [ "i" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <heap> (HN1_0 |-> list(ACC:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(triFold(I, HI, A, B, ACC))) ?FRESH1:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLC2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
     andBool notBool (HN1_0 in_keys(HRST1))
    ensures 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLC2 andBool HLC1 <=Int ?HLC2
     andBool keysBelow(?FRESH1, ?HLC2)
     andBool notBool (?HN1_0B in_keys(?FRESH1))
     andBool notBool (?HN1_0B in_keys(HRST1))
    [all-path]

  // ---- Entry (n=0) — result = tri(N) == triRes(N): the first N+1 Tribonacci-variant numbers. The `if n==0`
  // splits (base [1] vs the [1,3]+fold), matching triRes's two rules. Domain N >= 0.
  claim
    <k>
      FuncDef("tri", Params("n"),
        If(Compare(Name("n"), CmpOp("==", Int(0))),
          Return(ListExpr(Int(1))),
          .Stmts)
        Assign(Name("my_tri"), ListExpr(Int(1), Int(3)))
        Assign(Name("a"), Int(1))
        Assign(Name("b"), Int(3))
        For(Name("i"), Call(Name("range"), Int(2), BinOp("+", Name("n"), Int(1))),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("c"), BinOp("+", BinOp("//", Name("i"), Int(2)), Int(1))),
            Assign(Name("c"),
              BinOp("+", BinOp("+", Name("b"), Name("a")), BinOp("//", BinOp("+", Name("i"), Int(3)), Int(2)))))
          Assign(Name("my_tri"), BinOp("+", Name("my_tri"), ListExpr(Name("c"))))
          Assign(Name("a"), Name("b"))
          Assign(Name("b"), Name("c")))
        Return(Name("my_tri")))
      Assign(Name("result"), Call(Name("tri"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "tri" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(vCons(1, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0 andBool N ==Int 0
    [all-path]
  // ---- Entry (n>=1) — result = tri(N) == triRes(N): the first N+1 Tribonacci-variant numbers. The `if n==0`
  // splits (base [1] vs the [1,3]+fold), matching triRes's two rules. Domain N >= 0.
  claim
    <k>
      FuncDef("tri", Params("n"),
        If(Compare(Name("n"), CmpOp("==", Int(0))),
          Return(ListExpr(Int(1))),
          .Stmts)
        Assign(Name("my_tri"), ListExpr(Int(1), Int(3)))
        Assign(Name("a"), Int(1))
        Assign(Name("b"), Int(3))
        For(Name("i"), Call(Name("range"), Int(2), BinOp("+", Name("n"), Int(1))),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("c"), BinOp("+", BinOp("//", Name("i"), Int(2)), Int(1))),
            Assign(Name("c"),
              BinOp("+", BinOp("+", Name("b"), Name("a")), BinOp("//", BinOp("+", Name("i"), Int(3)), Int(2)))))
          Assign(Name("my_tri"), BinOp("+", Name("my_tri"), ListExpr(Name("c"))))
          Assign(Name("a"), Name("b"))
          Assign(Name("b"), Name("c")))
        Return(Name("my_tri")))
      Assign(Name("result"), Call(Name("tri"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "tri" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(triFold(2, N +Int 1, 1, 3, vCons(1, vCons(3, .ValSeq))))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0 andBool N >=Int 1
    [all-path]
endmodule
