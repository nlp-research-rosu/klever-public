requires "verification.k"

module SPEC-LEN-BRIDGE-OPPOSITE
  imports VERIFICATION

  // The ordinary mathematical/Python result for a two-element list is 2.
  // This must get stuck because the proof-local bridge has already returned 1.
  claim [abstract-list-should-have-len-two]:
    <k>
      Call(Name("len"), list(intVals(iCons(10, iCons(20, .IntSeq)))))
      =>
      2
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
