requires "verification.k"

module WITNESS-SPEC
  imports VERIFICATION

  // Satisfying entry state with a true contract result.
  claim [entry-true-000]:
    <k>
      Call(Name("triples_sum_to_zero"), (ref(0), .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
        0  |-> scope(solutionBindings(), parent(-1))
        -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(iCons(0, iCons(0, iCons(0, .IntSeq))))
       0 |-> list(intVals(iCons(0, iCons(0, iCons(0, .IntSeq)))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Satisfying entry state at the short-list boundary, with a false result.
  claim [entry-false-12]:
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
      -1 |-> intSeqGhost(iCons(1, iCons(2, .IntSeq)))
       0 |-> list(intVals(iCons(1, iCons(2, .IntSeq))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
