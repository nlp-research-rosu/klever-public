requires "verification-no-bridges.k"

module FALSE-PROGRAM-CLAIMS-NO-BRIDGES
  imports SPLIT-WORDS-NO-BRIDGES

  claim [empty-forced-whitespace]:
    <k> Call(solutionClosure, str(.IntSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("$proofPath" |-> 1, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [space-forced-comma]:
    <k>
      Call(solutionClosure, str(iCons(32, .IntSeq)))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("$proofPath" |-> 2, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(str(iCons(32, .IntSeq)), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [comma-forced-count]:
    <k>
      Call(solutionClosure, str(iCons(44, .IntSeq)))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("$proofPath" |-> 3, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
