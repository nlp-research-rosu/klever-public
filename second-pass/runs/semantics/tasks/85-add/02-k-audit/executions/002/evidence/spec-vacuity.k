requires "/tmp/audit-work/85-add/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the real result for [4, 2, 6, 7] is 2, while this
  // destination requires 3.  The full entry configuration is satisfiable.
  claim [false-result]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("add"),
           (list(intVals(
             iCons(4, iCons(2, iCons(6, iCons(7, .IntSeq))))
           )), .Exprs))
      =>
      3
    </k>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <env> 0 </env>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
