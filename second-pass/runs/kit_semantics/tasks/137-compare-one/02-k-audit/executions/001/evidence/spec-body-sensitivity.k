requires "/audit-output/evidence/verification-body-mutation.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION-BODY-MUTATION

  // False for the executed mutated term: compare_one(2,1) now returns 1.
  claim [changed-body]:
    <k> #loadAll(mutatedSolutionModule()) ~>
        Call(Name("compare_one"), 2, 1)
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
