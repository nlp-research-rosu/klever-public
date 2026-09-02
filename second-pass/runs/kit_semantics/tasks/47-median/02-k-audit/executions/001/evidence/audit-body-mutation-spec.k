requires "audit-verification-mutant.k"

module AUDIT-BODY-MUTATION-SPEC
  imports AUDIT-VERIFICATION-MUTANT

  claim [changed-body-rejected]:
    <k>
      Call(
        Name("median"),
        list(vCons(3, vCons(1, vCons(2, .ValSeq)))))
      =>
      2
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> auditSolutionClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(vCons(3, vCons(1, vCons(2, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
