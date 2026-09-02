requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the satisfying concrete input [] returns [], not ["E"].
  claim [false-empty-result]:
    <k> runGrades(.ValSeq) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map
      => 0 |-> list(vCons(letter("E"), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>

endmodule
