requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  // Satisfying entry state for IS = [1, -2, 0], with the formal expected
  // result substituted directly as [2, -1, 1].
  claim [ground-entry]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(
           Name("incr_list"),
           list(intVals(iCons(1, iCons(-2, iCons(0, .IntSeq))))))
      ~> #observeResult
      =>
      list(vCons(2, vCons(-1, vCons(1, .ValSeq))))
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
