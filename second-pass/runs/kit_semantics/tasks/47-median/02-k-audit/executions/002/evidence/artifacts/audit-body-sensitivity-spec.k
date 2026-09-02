requires "audit-verification-mutated.k"

module AUDIT-BODY-SENSITIVITY-SPEC
  imports AUDIT-VERIFICATION-MUTATED

  // The original body returns 5 here; the executed mutant body returns 0.
  claim [audit-mutated-body-rejected]:
    <k>
      Call(
        Name("median"),
        list(vCons(9, vCons(1, vCons(5, .ValSeq)))))
      =>
      5
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosureMutated, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(vCons(9, vCons(1, vCons(5, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
