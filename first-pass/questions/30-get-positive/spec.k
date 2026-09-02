requires "verification.k"

module GET-POSITIVE-SPEC
  imports GET-POSITIVE-VERIFICATION

  // ---- Loop invariant (circularity) — $acc grows by valSeqConcat(R, filterPos(intListOf(VS))).
  // The guard is compGuard's BoolOp("and", e > 0) (a single filter wrapped in and).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e"),
        If(BoolOp("and", Compare(Name("e"), CmpOp(">", Int(0)))),
           Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("e")))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "e" <- _:Val ], P:Parent) =>
        scope(.Map [ "$acc" <- ref(?AN2:Int) ] [ "e" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLM:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
     andBool 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K valSeqConcat(R, filterPos(intListOf(VS)))
    [all-path]

  // ---- Entry claim — result = get_positive(list(VS)) == filterPos(intListOf(VS)).
  // Two nested calls: get_positive (scope 1), then the comprehension closure
  // (scope 2), so nextLoc runs 1 => 3.
  claim
    <k>
      FuncDef("get_positive", Params("l"),
        Return(
          ListComp(Name("e"),
            CompFor(Name("e"), Name("l"),
              Compare(Name("e"), CmpOp(">", Int(0)))))))
      Assign(Name("result"), Call(Name("get_positive"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "get_positive" <- ?_:Val ] [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(filterPos(intListOf(VS)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
