requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports NEXT-SMALLEST-WITH-LOOP-LEMMA

  // Fresh false mutation: claim that every input returns None.  The existing
  // entry precondition is satisfiable by INPUT = [1, 2], for which both Python
  // implementations and nsScan return 2.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("next_smallest"),
              (list(intVals(INPUT:Ints)), .Exprs))
    =>
      noneV
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
