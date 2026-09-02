requires "verification-no-bridge.k"

module FIXED-EQUAL-LISTS-SPEC
  imports MONOTONIC-VERIFICATION-NO-BRIDGE

  claim [equal-singletons]:
    <k>
      Compare(
        list(vCons(1, .ValSeq)),
        CmpOp("==", list(vCons(1, .ValSeq)))
      )
      => true
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
endmodule
