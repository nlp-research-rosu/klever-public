requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfiable empty-input state: the program returns [].
  claim [empty-wrongly-returns-e]:
    <k> runGrades(.ValSeq) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(letter("E"), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
endmodule
