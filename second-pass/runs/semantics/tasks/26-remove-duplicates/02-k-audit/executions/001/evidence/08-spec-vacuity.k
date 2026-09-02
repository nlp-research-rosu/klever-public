requires "verification.k"

module REMOVE-DUPLICATES-SPEC-VACUITY
  imports REMOVE-DUPLICATES-VERIFICATION

  // Deliberately false: remove_duplicates([]) returns an empty list, not [0].
  claim [entry-empty-false-result]:
    <k>
      Call(#removeDuplicatesClosure, list(.ValSeq), .Exprs)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(0, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
