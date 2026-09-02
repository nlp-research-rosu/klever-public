requires "verification-body-mutant.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION-BODY-MUTANT

  // The only program mutation is x + 1 -> x + 2 inside solutionProgram.
  // For input [0], retaining the original expected result [1] is false.
  claim [changed-body-rejects-original-result]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("incr_list"), list(intVals(iCons(0, .IntSeq))))
      ~> #observeResult
      => list(vCons(1, .ValSeq))
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
endmodule
