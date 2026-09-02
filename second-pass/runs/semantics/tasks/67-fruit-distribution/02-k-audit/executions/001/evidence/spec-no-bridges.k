requires "verification-no-bridges.k"

module SPEC-NOBRIDGES
  imports VERIFICATION-NOBRIDGES

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           str(fruitSentenceCodes(A, B)), N, .Exprs)
      => N -Int A -Int B
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
    requires A >=Int 0
     andBool B >=Int 0
     andBool A +Int B <=Int N
endmodule
