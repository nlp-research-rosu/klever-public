requires "verification.k"

module SPEC-VACUITY-CONTENT
  imports SORT-ARRAY-VERIFICATION

  // Deliberately false: keep the returned outer ref but require it to contain
  // only the decimal pre-sort, omitting the keyed popcount sort.
  claim
    <k>
      Call(sortArrayClosure, list(VS))
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(VS))
      1 |-> list(sortVS(VS))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNonNegativeInts(VS)
endmodule
