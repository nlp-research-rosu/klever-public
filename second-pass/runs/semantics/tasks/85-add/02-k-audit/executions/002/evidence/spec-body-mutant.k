requires "/audit-output/evidence/verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim [body-sensitivity]:
    <k>
      #loadAll(mutatedSolutionModule)
      ~> Call(
           Name("add"),
           (list(intVals(iCons(4, iCons(2, .IntSeq)))), .Exprs))
      =>
      2
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
