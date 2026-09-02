requires "verification.k"

module FALSE-PROGRAM-CLAIMS
  imports SPLIT-WORDS-VERIFICATION

  // Real input "".  The program returns integer 0, but proofPath=1 forces the
  // false first branch and proves an allocated empty list.
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

  // Real input " ".  The program takes its first branch and returns [], but
  // proofPath=2 discards it and forces the false comma branch, proving [" "].
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

  // Real input ",".  The program returns ["", ""], but proofPath=3 discards
  // the true comma branch and proves the final integer result 0.
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
