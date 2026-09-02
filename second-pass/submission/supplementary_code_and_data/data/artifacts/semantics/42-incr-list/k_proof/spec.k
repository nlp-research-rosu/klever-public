requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive loop invariant. The accumulator object stays at the same heap
  // location and gains exactly the incremented form of the remaining input.
  claim [incr-loop]:
    <k>
      #loop(list(intVals(IS:IntSeq)), Name("x"), incrLoopBody)
      ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(("l" |-> _INPUT:Val)
                   ("result" |-> ref(H:Int))
                   ("x" |-> (_OLD_X:Val => ?_FINAL_X:Val)),
                   _PAR:Parent)
       _REST_SCOPES:Map)
    </scopes>
    <heap>
      H |-> list(
        PREFIX:ValSeq
        => valSeqConcat(PREFIX, incrVals(IS)))
      _REST_HEAP:Map
    </heap>

  // End-to-end contract for the exact solution.mpy constructor tree.
  claim [incr-list]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("incr_list"), list(intVals(IS:IntSeq)))
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
    ensures ?RESULT ==K incrVals(IS)
    [depends(incr-loop)]
endmodule
