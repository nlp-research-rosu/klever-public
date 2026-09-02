// spec.k — minPath on the UNIFIED semantics (src/). 2x2-restricted: phase 1 unrolls concretely to
// val = min(B,C); phase 2 (alternating build over range(k)) folds via altFrom. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module MIN-PATH-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module MIN-PATH-SPEC

requires "verification.k"

module MIN-PATH-SPEC
  imports MIN-PATH-VERIFICATION

  // ---- Phase-2 invariant (circularity) — over range [I, K) from ans = list(ANS) the alternating
  // build leaves ans := list(altFrom(ANS, I, K, VAL)). Other (phase-1) locals ride in REST:Map.
  claim
    <k>
      #loop(rangeObj(I:Int, K:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
           Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Int(1)))),
           Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Name("val"))))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "minPath" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "grid" <- GV:Val ] [ "k" <- KV:Val ] [ "n" <- NV:Val ]
                   [ "val" <- VAL:Int ] [ "i" <- _:Val ] [ "j" <- JV:Val ]
                   [ "temp" <- TV:Val ] [ "ans" <- ref(HN1_0:Int) ], parent(0)) =>
        scope(.Map [ "grid" <- GV ] [ "k" <- KV ] [ "n" <- NV ]
                   [ "val" <- VAL ] [ "i" <- ?_:Val ] [ "j" <- JV ]
                   [ "temp" <- TV ] [ "ans" <- ref(?HN1_0B:Int) ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <heap> (HN1_0 |-> list(ANS:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(altFrom(ANS, I, K, VAL))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = minPath([[1,B],[C,D]], K) == list(altFrom(.ValSeq, 0, K, min(B,C))).
  // 2x2 grid, 1 at (0,0); B,C,D symbolic ints =/= 1 (only (0,0) triggers the neighbor-min); K >= 0.
  claim
    <k>
      FuncDef("minPath", Params("grid", "k"),
        Assign(Name("n"), Call(Name("len"), Name("grid")))
        Assign(Name("val"), BinOp("+", BinOp("*", Name("n"), Name("n")), Int(1)))
        For(Name("i"), Call(Name("range"), Name("n")),
          For(Name("j"), Call(Name("range"), Name("n")),
            If(Compare(Subscript(Subscript(Name("grid"), Name("i")), Name("j")), CmpOp("==", Int(1))),
              Assign(Name("temp"), ListExpr(.Exprs))
              If(Compare(Name("i"), CmpOp("!=", Int(0))),
                Assign(Name("temp"), BinOp("+", Name("temp"),
                  ListExpr(Subscript(Subscript(Name("grid"), BinOp("-", Name("i"), Int(1))), Name("j"))))),
                .Stmts)
              If(Compare(Name("j"), CmpOp("!=", Int(0))),
                Assign(Name("temp"), BinOp("+", Name("temp"),
                  ListExpr(Subscript(Subscript(Name("grid"), Name("i")), BinOp("-", Name("j"), Int(1)))))),
                .Stmts)
              If(Compare(Name("i"), CmpOp("!=", BinOp("-", Name("n"), Int(1)))),
                Assign(Name("temp"), BinOp("+", Name("temp"),
                  ListExpr(Subscript(Subscript(Name("grid"), BinOp("+", Name("i"), Int(1))), Name("j"))))),
                .Stmts)
              If(Compare(Name("j"), CmpOp("!=", BinOp("-", Name("n"), Int(1)))),
                Assign(Name("temp"), BinOp("+", Name("temp"),
                  ListExpr(Subscript(Subscript(Name("grid"), Name("i")), BinOp("+", Name("j"), Int(1)))))),
                .Stmts)
              Assign(Name("val"), Call(Name("min"), Name("temp"))),
              .Stmts)))
        Assign(Name("ans"), ListExpr(.Exprs))
        For(Name("i"), Call(Name("range"), Name("k")),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
             Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Int(1)))),
             Assign(Name("ans"), BinOp("+", Name("ans"), ListExpr(Name("val"))))))
        Return(Name("ans")))
      Assign(Name("result"),
        Call(Name("minPath"),
          (list(vCons(list(vCons(1, vCons(B:Int, .ValSeq))),
                 vCons(list(vCons(C:Int, vCons(D:Int, .ValSeq))), .ValSeq))),
           K:Int, .Exprs)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "minPath" <- ?_:Val ]
                       [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(altFrom(.ValSeq, 0, K, minInt(C, B)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires B =/=Int 1 andBool C =/=Int 1 andBool D =/=Int 1 andBool K >=Int 0
    [all-path]
endmodule
