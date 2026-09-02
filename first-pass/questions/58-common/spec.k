// spec.k — common on the UNIFIED semantics (src/). Single loop over l1 keeping each e1 in l2 not
// already collected, then sorted(). Both memberships are the opaque memberVS (see verification.k);
// the loop folds commonFold, the entry wraps it in the trusted sortVS. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module COMMON-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module COMMON-SPEC

requires "verification.k"

module COMMON-SPEC
  imports COMMON-VERIFICATION

  // ---- Loop invariant (circularity) — the intersect+dedup loop over VS from out = list(OUT)
  // leaves out := list(commonFold(VS, IS2, OUT)). The outer `e1 in l2` is memberVS(X, IS2), the
  // inner `e1 not in out` is notBool memberVS(X, OUT); the nested-If case-split matches commonFold.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e1"),
        If(Compare(Name("e1"), CmpOp("in", Name("l2"))),
           If(Compare(Name("e1"), CmpOp("not in", Name("out"))),
              Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("e1")))),
              .Stmts),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "l1" <- LV1:Val ] [ "l2" <- list(IS2:ValSeq) ] [ "out" <- ref(HN1_0:Int) ] [ "e1" <- _:Val ], P:Parent) =>
        scope(.Map [ "l1" <- LV1 ] [ "l2" <- list(IS2) ] [ "out" <- ref(?HN1_0B:Int) ] [ "e1" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(OUT:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(?OO:ValSeq)) ?HRST2:Map </heap>
    <heapLoc> HLC1:Int => ?HLC2:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
     andBool allInt(VS) andBool allInt(IS2) andBool allInt(OUT)
    ensures ?OO ==K commonFold(VS, IS2, OUT)
     andBool 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLC2
     andBool keysBelow(?HRST2, ?HLC2)
     andBool notBool ?HN1_0B in_keys(?HRST2)
    [all-path]

  // ---- Entry claim — result = sorted(intersect_dedup(l1, l2)) == list(sortVS(commonFold(IS1, IS2, .ValSeq))).
  claim
    <k>
      FuncDef("common", Params("l1", "l2"),
        Assign(Name("out"), ListExpr(.Exprs))
        For(Name("e1"), Name("l1"),
          If(Compare(Name("e1"), CmpOp("in", Name("l2"))),
             If(Compare(Name("e1"), CmpOp("not in", Name("out"))),
                Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("e1")))),
                .Stmts),
             .Stmts))
        Return(Call(Name("sorted"), Name("out"))))
      Assign(Name("result"), Call(Name("common"), list(IS1:ValSeq), list(IS2:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "common" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(sortVS(commonFold(IS1, IS2, .ValSeq)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(IS1) andBool allInt(IS2)
    [all-path]
endmodule
