requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

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

  // Deliberately false: the real result does not acquire an extra leading 0.
  // The empty input is a satisfying witness: [] is not [0].
  claim [false-incr-list]:
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
    ensures ?RESULT ==K vCons(0, incrVals(IS))
    [depends(incr-loop)]
endmodule
