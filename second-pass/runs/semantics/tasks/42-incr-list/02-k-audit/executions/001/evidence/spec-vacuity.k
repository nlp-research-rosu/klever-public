requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation: on the satisfiable empty-list input, demand [0]
  // even though the executed function returns [].
  claim [incr-list-false-empty]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("incr_list"), list(intVals(.IntSeq)))
      ~> #observeResult
      => list(?RESULT:ValSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?_FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_FINAL_HEAP:Map </heap>
    <heapLoc> 0 => ?_FINAL_HEAP_LOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    ensures ?RESULT ==K vCons(0, .ValSeq)
endmodule
