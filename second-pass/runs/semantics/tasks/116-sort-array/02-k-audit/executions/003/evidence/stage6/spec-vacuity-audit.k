requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports SORT-ARRAY-VERIFICATION

  // Deliberately false: the executed function returns the outer allocation
  // at ref(1), not the inner decimal-sort allocation at ref(0).
  claim
    <k>
      Call(sortArrayClosure, list(VS))
      =>
      ref(0)
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
      1 |-> list(sortArraySpec(VS))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNonNegativeInts(VS)
endmodule
