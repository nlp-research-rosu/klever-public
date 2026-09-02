requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  // Loop invariant/circularity. The function frame and return continuation are
  // included so an early Return(false) and normal Return(true) are both proved.
  claim
    <k> #loop(list(intsToVals(IS:IntSeq)),
              Name("number"),
              belowThresholdLoopBody)
         ~> (Return(Bool(true)) .Stmts)
         ~> #endcall
      => belowThresholdSpec(IS, T)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      1 |-> scope(
        "l"      |-> list(intsToVals(_ORIGINAL:IntSeq))
        "number" |-> _OLD:Int
        "t"      |-> T:Int,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> BUILTINS:Scope
      =>
      0  |-> scope(.Map, parent(-1))
      -1 |-> BUILTINS
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(loop-invariant)]

endmodule

module SPEC
  imports VERIFICATION

  // End-to-end entry-point claim, composed with the independently proved
  // loop-invariant rule in VERIFICATION.
  claim
    <k> #belowThresholdCall(IS:IntSeq, T:Int)
      => belowThresholdSpec(IS, T)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(entry-point)]
endmodule
