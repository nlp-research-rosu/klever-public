requires "audit-variants.k"

module OPPOSITE-INT-SPEC
  imports OPPOSITE-INT

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           str(fruitSentenceCodes(5, 6)), 19, .Exprs)
      => 6
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
