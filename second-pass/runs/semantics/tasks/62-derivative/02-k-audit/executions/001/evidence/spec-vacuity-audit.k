requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation of entry-empty: the satisfying input xs=[] really
  // returns [], but this postcondition requires a one-element result [1].
  claim
    <k>
      Call(Name("derivative"), list(asValSeq(.IntVals)))
      => ref(?RESULT:Int)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("derivative" |-> derivativeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ?RESULT |-> list(vCons(1, .ValSeq))
      ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    [label(false-empty-result)]
endmodule
