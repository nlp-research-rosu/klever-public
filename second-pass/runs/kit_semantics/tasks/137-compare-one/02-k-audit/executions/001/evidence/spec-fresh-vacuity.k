requires "/tmp/audit-work/reconstruction/verification.k"

module SPEC-FRESH-VACUITY
  imports VERIFICATION

  // Deliberately false result constraint. The unchanged real program returns
  // 2 for (1,2), so a destination value of 1 must be rejected.
  claim [wrong-one-two]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), 1, 2)
      => 1 </k>
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
