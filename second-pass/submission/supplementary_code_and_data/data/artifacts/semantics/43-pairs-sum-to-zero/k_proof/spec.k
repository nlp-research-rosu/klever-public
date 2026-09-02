requires "verification.k"

module PAIRS-SUMMARY-SPEC
  imports PAIRS-VERIFICATION

  claim [bounded-empty]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(.ValSeq), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [bounded-one]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(vCons(A:Int, .ValSeq)), .Exprs))
      => pairsSpec(vCons(A, .ValSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(seenAfter(vCons(A, .ValSeq), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [bounded-two]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(vCons(A:Int, vCons(B:Int, .ValSeq))), .Exprs))
      => pairsSpec(vCons(A, vCons(B, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           seenAfter(vCons(A, vCons(B, .ValSeq)), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Inductive summary of the reference semantics' list-membership machine.
  claim [membership-summary]:
    <k>
      #memberAcc(V:Int, list(intValues(INPUT:IntSeq)))
      ~> CONT:K
      =>
      memberIS(V, INPUT)
      ~> CONT
    </k>

  // Loop invariant. REM is the unprocessed suffix and SEEN is exactly the
  // prefix accumulated in heap object H.
  claim [loop-summary]:
    <k>
      #loop(list(intValues(REM:IntSeq)),
            Name("value"), pairLoopBody)
      ~> (Return(Bool(false)) .Stmts)
      ~> #endcall
      =>
      scanIS(REM, SEEN)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1))
        1 |-> scope(
          ( "l" |-> list(intValues(ORIGINAL:IntSeq))
            "seen" |-> ref(H:Int)
            "value" |-> OLD:Int ),
          parent(0)) )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1)) )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      (H |-> list(intValues(SEEN:IntSeq)) HEAP:Map)
      =>
      (H |-> list(intValues(seenAfterIS(REM, SEEN))) HEAP)
    </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule

module PAIRS-MAIN-SPEC
  imports PAIRS-VERIFICATION-LEMMAS

  // Main theorem: INPUT ranges over IntSeq, an inductive representation of
  // every finite integer list.
  claim [all-integer-lists]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(intValues(INPUT:IntSeq)), .Exprs))
      =>
      pairsIS(INPUT)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(intValues(seenAfterIS(INPUT, .IntSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
