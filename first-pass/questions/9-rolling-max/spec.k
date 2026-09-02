requires "verification.k"

module ROLLING-MAX-SPEC
  imports ROLLING-MAX-VERIFICATION

  // ---- Loop invariant (circularity) — 3-state fold. From (result=list(R), m=M,
  // first=F) the loop leaves result := list(valSeqConcat(R, rollAcc(VS, M, F))).
  // Induction on VS; `if first` / inner `if n>m` line up with rollAcc.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("n"),
        If(Name("first"),
          Assign(Name("m"), Name("n"))
          Assign(Name("first"), Bool(false)),
          If(Compare(Name("n"), CmpOp(">", Name("m"))),
            Assign(Name("m"), Name("n")),
            .Stmts))
        Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("m")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "numbers" <- NV:Val ] [ "result" <- ref(HNA:Int) ]
                   [ "m" <- M:Val ] [ "first" <- F:Bool ] [ "n" <- _:Val ], P:Parent) =>
        scope(.Map [ "numbers" <- NV ] [ "result" <- ref(?HNB:Int) ]
                   [ "m" <- ?_:Val ] [ "first" <- ?_:Bool ] [ "n" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HNA |-> list(R:ValSeq)) HRSTA:Map
        => (?HNB |-> list(?RVS:ValSeq)) ?_:Map </heap>
    <heapLoc> HLCA:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool isInt(M)
     andBool 0 <=Int HNA andBool HNA <Int HLCA andBool keysBelow(HRSTA, HLCA)
    ensures ?RVS ==K valSeqConcat(R, rollAcc(intListOf(VS), M, F))
    [all-path]

  // ---- Entry claim — result = rolling_max(list(VS)) == rollAcc(intListOf(VS), 0, true).
  // (The m=0 seed is irrelevant — `first` overrides it on the first element.)
  claim
    <k>
      FuncDef("rolling_max", Params("numbers"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("m"), Int(0))
        Assign(Name("first"), Bool(true))
        Assign(Name("n"), Int(0))
        For(Name("n"), Name("numbers"),
          If(Name("first"),
            Assign(Name("m"), Name("n"))
            Assign(Name("first"), Bool(false)),
            If(Compare(Name("n"), CmpOp(">", Name("m"))),
              Assign(Name("m"), Name("n")),
              .Stmts))
          Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("m")))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("rolling_max"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "rolling_max" <- ?_:Val ] [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(rollAcc(intListOf(VS), 0, true))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
