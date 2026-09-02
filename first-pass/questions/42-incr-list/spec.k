requires "verification.k"

module INCR-LIST-SPEC
  imports INCR-LIST-VERIFICATION

  // ---- Loop invariant (circularity) — $acc grows by valSeqConcat(R, incrVS(intListOf(VS))).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e"),
        If(BoolOp("and", Bool(true)),
           Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(BinOp("+", Name("e"), Int(1))))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(HN1_0:Int) ] [ "e" <- _:Val ], P:Parent) =>
        scope(.Map [ "$acc" <- ref(?HN1_0B:Int) ] [ "e" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    ensures ?RO ==K valSeqConcat(R, incrVS(intListOf(VS)))
    [all-path]

  // ---- Entry claim — result = incr_list(list(VS)) == incrVS(intListOf(VS)).
  claim
    <k>
      FuncDef("incr_list", Params("l"),
        Return(
          ListComp(BinOp("+", Name("e"), Int(1)),
            CompFor(Name("e"), Name("l"), Bool(true)))))
      Assign(Name("result"), Call(Name("incr_list"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "incr_list" <- ?_:Val ] [ "result" <- ref(?HN2_e:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_e |-> list(incrVS(intListOf(VS)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
