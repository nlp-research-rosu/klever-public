requires "verification.k"

module COMPARE-SPEC
  imports COMPARE-VERIFICATION

  // ---- Loop invariant (circularity) — $acc grows by valSeqConcat(R, compareVS(...)) over the zip.
  claim
    <k>
      #loop(zipObj(S1:ValSeq, S2:ValSeq), TupleExpr(Name("x"), Name("y")),
        If(BoolOp("and", Bool(true)),
           Assign(Name("$acc"), BinOp("+", Name("$acc"),
             ListExpr(Call(Name("abs"), BinOp("-", Name("x"), Name("y")))))),
           .Stmts))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      ... -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare" <- _:Val ], parent(-1))
      1 |-> scope(.Map [ "game" <- _:Val ] [ "guess" <- _:Val ], parent(0))
      2 |-> (
        scope(.Map [ "$acc" <- ref(HN1_0:Int) ] [ "x" <- _:Val ] [ "y" <- _:Val ], parent(1)) =>
        scope(.Map [ "$acc" <- ref(?HN1_0B:Int) ] [ "x" <- ?_:Val ] [ "y" <- ?_:Val ], parent(1))
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(S1) andBool allInt(S2)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    ensures ?RO ==K valSeqConcat(R, compareVS(intListOf(S1), intListOf(S2)))
    [all-path]

  // ---- Entry claim — result = compare(list(VS1), list(VS2)) == compareVS over the zip.
  // Two frames: compare (scope 1) + the comprehension closure (scope 2); nextLoc 1 => 3.
  claim
    <k>
      FuncDef("compare", Params("game", "guess"),
        Return(
          ListComp(Call(Name("abs"), BinOp("-", Name("x"), Name("y"))),
            CompFor(
              TupleExpr(Name("x"), Name("y")),
              Call(Name("zip"), Name("game"), Name("guess")),
              Bool(true)))))
      Assign(Name("result"), Call(Name("compare"), list(VS1:ValSeq), list(VS2:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare" <- ?_:Val ] [ "result" <- ref(?HN2_e:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_e |-> list(compareVS(intListOf(VS1), intListOf(VS2)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS1) andBool allInt(VS2)
    [all-path]
endmodule
