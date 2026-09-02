requires "verification.k"

module SPEC-GROUND-WITNESS
  imports VERIFICATION

  claim [empty]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("incr_list"), list(intVals(.IntSeq)))
      ~> #observeResult
      => list(.ValSeq)
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

  claim [two-elements]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(
           Name("incr_list"),
           list(intVals(iCons(2, iCons(-1, .IntSeq)))))
      ~> #observeResult
      => list(vCons(3, vCons(0, .ValSeq)))
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
