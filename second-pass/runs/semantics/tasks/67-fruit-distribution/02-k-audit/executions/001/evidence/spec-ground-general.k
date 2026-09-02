requires "verification.k"

module SPEC-GROUND-GENERAL
  imports VERIFICATION

  // Satisfying witness for the general precondition:
  // A=5, B=6, N=19; 5>=0, 6>=0, and 5+6<=19.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           str(fruitSentenceCodes(5, 6)), 19, .Exprs)
      => 8
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINAL_HEAP:Map </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
