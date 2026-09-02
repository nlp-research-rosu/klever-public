requires "verification.k"

module MONOTONIC-SPEC-FALSE-MUTATION
  imports MONOTONIC-VERIFICATION

  // False mutation of entry claim 1.  The empty list satisfies
  // nondecreasing(.ValSeq), and both Python implementations return true.
  // This mutation instead demands false.
  claim [mutated-nondecreasing-result]:
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
