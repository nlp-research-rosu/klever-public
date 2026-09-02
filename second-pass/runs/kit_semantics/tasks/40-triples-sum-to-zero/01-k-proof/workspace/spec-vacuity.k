requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false for [0, 0, 0]: the real result is true.
  claim [false-result]:
    <k>
      Call(
        Name("triples_sum_to_zero"),
        (ref(0), .Exprs))
      => false
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
endmodule
