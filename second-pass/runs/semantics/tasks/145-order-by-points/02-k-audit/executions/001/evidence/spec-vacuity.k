requires "verification.k"

module ORDER-BY-POINTS-SPEC-VACUITY
  imports ORDER-BY-POINTS-VERIFICATION

  // Deliberately false for the satisfying input VS = vCons(1, .ValSeq):
  // the real program returns [1], not [].
  claim [false-empty-result]:
    <k> #runOrderByPoints(list(VS:ValSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
