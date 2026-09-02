requires "verification.k"

module FRESH-FALSE-SPEC
  imports VERIFICATION

  // Fresh false result obligation: [1, -1, 0] has three distinct positions
  // summing to zero, so requiring false must be rejected.
  claim [false-result-1-neg1-0]:
    <k>
      Call(Name("triples_sum_to_zero"), (ref(0), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
        0  |-> scope(solutionBindings(), parent(-1))
        -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(iCons(1, iCons(-1, iCons(0, .IntSeq))))
       0 |-> list(intVals(iCons(1, iCons(-1, iCons(0, .IntSeq)))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
