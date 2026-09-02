// spec.k — unique on the UNIFIED semantics (src/). Order-preserving dedup loop then sorted().
// Membership `x not in out` on the symbolic accumulator is the opaque memberVS (see verification.k);
// the loop folds dedupFold, the entry wraps it in the trusted sortVS. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module UNIQUE-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module UNIQUE-SPEC

requires "verification.k"

module UNIQUE-SPEC
  imports UNIQUE-VERIFICATION

  // ---- Loop invariant (circularity) — the dedup loop over VS from out = list(OUT) leaves
  // out := list(dedupFold(VS, OUT)). The `x not in out` guard is the opaque memberVS(X, OUT);
  // the If case-split matches dedupFold's memberVS / notBool memberVS rules.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("x"), CmpOp("not in", Name("out"))),
           Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("x")))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "l" <- LV:Val ] [ "out" <- ref(HN1_0:Int) ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "l" <- LV ] [ "out" <- ref(?HN1_0B:Int) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(OUT:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(?OO:ValSeq)) ?HRST2:Map </heap>
    <heapLoc> HLC1:Int => ?HLC2:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
     andBool allInt(VS) andBool allInt(OUT)
    ensures ?OO ==K dedupFold(VS, OUT)
     andBool 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLC2
     andBool keysBelow(?HRST2, ?HLC2)
     andBool notBool ?HN1_0B in_keys(?HRST2)
    [all-path]

  // ---- Entry claim — result = sorted(dedup(l)) == list(sortVS(dedupFold(VS, .ValSeq))).
  claim
    <k>
      FuncDef("unique", Params("l"),
        Assign(Name("out"), ListExpr(.Exprs))
        For(Name("x"), Name("l"),
          If(Compare(Name("x"), CmpOp("not in", Name("out"))),
             Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("x")))),
             .Stmts))
        Return(Call(Name("sorted"), Name("out"))))
      Assign(Name("result"), Call(Name("unique"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "unique" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(sortVS(dedupFold(VS, .ValSeq)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
