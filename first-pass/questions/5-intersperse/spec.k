requires "verification.k"

module INTERSPERSE-SPEC
  imports INTERSPERSE-VERIFICATION

  // ---- Loop invariant (circularity) — dual-state fold. From (result=list(R),
  // first=F) the loop leaves result := list(valSeqConcat(R, interAcc(VS, D, F))).
  // Induction on VS; the body flips `first` to false after the 1st element.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("n"),
        If(Name("first"),
          Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("n"))))
          Assign(Name("first"), Bool(false)),
          Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("delimeter"), Name("n"))))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "numbers" <- NV:Val ] [ "delimeter" <- D:Int ]
                   [ "result" <- ref(HNA:Int) ] [ "first" <- F:Bool ] [ "n" <- _:Val ], P:Parent) =>
        scope(.Map [ "numbers" <- NV ] [ "delimeter" <- D ]
                   [ "result" <- ref(?HNB:Int) ]
                   [ "first" <- ?_:Bool ] [ "n" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HNA |-> list(R:ValSeq)) HRSTA:Map
        => (?HNB |-> list(?RVS:ValSeq)) ?_:Map </heap>
    <heapLoc> HLCA:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HNA andBool HNA <Int HLCA andBool keysBelow(HRSTA, HLCA)
    ensures ?RVS ==K valSeqConcat(R, interAcc(VS, D, F))
    [all-path]

  // ---- Entry claim — result = intersperse(list(VS), D) == interAcc(VS, D, true).
  claim
    <k>
      FuncDef("intersperse", Params("numbers", "delimeter"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("first"), Bool(true))
        Assign(Name("n"), Int(0))
        For(Name("n"), Name("numbers"),
          If(Name("first"),
            Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("n"))))
            Assign(Name("first"), Bool(false)),
            Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("delimeter"), Name("n"))))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("intersperse"), list(VS:ValSeq) , D:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "intersperse" <- ?_:Val ] [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(interAcc(VS, D, true))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
