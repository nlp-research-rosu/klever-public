requires "audit-native-verification.k"

module AUDIT-NATIVE-ENTRY-SPEC
  imports AUDIT-NATIVE-WITH-LOOP-LEMMA

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("next_smallest"),
              (list(nativeIntVals(INPUT:Ints)), .Exprs))
    =>
      nsScan(INPUT, 0, 0, 0)
    </k>
    <env> 0 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    =>
      ?FINAL_ENTRY_SCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
