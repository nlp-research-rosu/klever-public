requires "/tmp/audit-work/spec.k"

module REVIEWER-LOOP-BRIDGE-CONTEXT-SPEC
  imports PAIRS-SUMMARY-SPEC

  // Bridge-free connection theorem over the complete domain accepted by the
  // promoted rule. Unlike the candidate's loop-summary, this explicitly
  // quantifies the arbitrary builtins scope, heapLoc, exception, and exit cells
  // that the promoted rewrite frames.
  claim [complete-loop-bridge-domain]:
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
      ( -1 |-> BUILTINS:Scope
        0 |-> scope(.Map, parent(-1))
        1 |-> scope(
          ( "l" |-> list(intValues(ORIGINAL:IntSeq))
            "seen" |-> ref(H:Int)
            "value" |-> OLD:Int ),
          parent(0)) )
      =>
      ( -1 |-> BUILTINS
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
    <exc> EXC:Exc </exc>
    <exit-code> EC:Int </exit-code>
endmodule
