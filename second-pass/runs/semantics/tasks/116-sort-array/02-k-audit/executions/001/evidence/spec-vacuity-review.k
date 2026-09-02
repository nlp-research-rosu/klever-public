requires "/tmp/audit-work/rebuild/verification.k"

module REVIEW-SPEC-VACUITY
  imports SORT-ARRAY-VERIFICATION

  // Deliberately false: execution performs two allocations and returns the
  // outer keyed-sort object at ref(1), not the inner decimal-sort object ref(0).
  // VS=.ValSeq is a concrete satisfying witness for the unchanged precondition.
  claim
    <k> Call(sortArrayClosure, list(VS)) => ref(0) </k>
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
      1 |-> list(sortArraySpec(VS))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNonNegativeInts(VS)
endmodule
