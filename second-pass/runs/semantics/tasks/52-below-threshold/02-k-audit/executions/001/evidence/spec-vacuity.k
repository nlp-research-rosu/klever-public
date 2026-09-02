requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: require the function to return the Boolean opposite of
  // its mathematical result.  The empty-list witness satisfies the entry state,
  // returns true, and makes this destination false.
  claim
    <k>
      #belowThresholdCall(IS:IntSeq, T:Int)
      => notBool belowThresholdSpec(IS, T)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(false-opposite-result)]
endmodule
