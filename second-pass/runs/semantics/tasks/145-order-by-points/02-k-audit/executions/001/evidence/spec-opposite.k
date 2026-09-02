requires "opposite-verification.k"

module ORDER-BY-POINTS-OPPOSITE-SPEC
  imports ORDER-BY-POINTS-OPPOSITE-VERIFICATION

  // False under the task contract: digit sums are 2 and 1, so [11, 1]
  // must become [1, 11]. The identity interpretation proves [11, 1].
  claim [wrong-ground-result]:
    <k>
      #runOrderByPoints(list(vCons(11, vCons(1, .ValSeq))))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(11, vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
