requires "verification-no-bridge.k"

module BRIDGE-CONNECTION-SPEC
  imports MONOTONIC-VERIFICATION-NO-BRIDGE

  claim [ascending-connection]:
    <k>
      Compare(list(VS:ValSeq), CmpOp("==", list(sortVS(VS))))
      => nondecreasing(VS)
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

  claim [descending-connection]:
    <k>
      Compare(
        list(VS:ValSeq),
        CmpOp("==", list(revVSAcc(sortVS(VS), .ValSeq)))
      )
      => nonincreasing(VS)
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
