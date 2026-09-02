requires "/tmp/audit-work/reconstruction/verification.k"

module SPEC-GROUND-WITNESS
  imports VERIFICATION

  // Satisfying instance of SPEC.int-int: compare_one(1, 2) must yield 2.
  claim [one-two]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), 1, 2)
      => 2 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
