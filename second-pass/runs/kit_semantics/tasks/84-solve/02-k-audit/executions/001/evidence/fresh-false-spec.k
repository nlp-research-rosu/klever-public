requires "verification.k"

module FRESH-FALSE-SPEC
  imports VERIFICATION

  // N=147 satisfies the source domain. The real result is "1100", not "111".
  claim [wrong-ground-result]:
    <k>
      #loadAll(solutionModule) ~> Call(Name("solve"), 147)
      =>
      str(iCons(49, iCons(49, iCons(49, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
