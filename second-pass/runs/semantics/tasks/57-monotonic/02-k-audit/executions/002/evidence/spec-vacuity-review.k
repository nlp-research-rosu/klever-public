requires "verification.k"

module MONOTONIC-SPEC-VACUITY-REVIEW
  imports MONOTONIC-VERIFICATION

  // Fresh false mutation of claim 1. Witness: VS = [1, 2].
  // Its precondition is true, but the submitted program returns true, not false.
  claim
    <k>
      #loadAll(monotonicProgram)
      ~> Call(Name("monotonic"), list(VS:ValSeq))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires nondecreasing(VS)
endmodule
