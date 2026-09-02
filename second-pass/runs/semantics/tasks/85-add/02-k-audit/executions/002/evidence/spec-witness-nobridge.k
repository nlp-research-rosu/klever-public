requires "/audit-output/evidence/verification-nobridge.k"

module SPEC-WITNESS-NOBRIDGE
  imports VERIFICATION-NOBRIDGE

  claim [entry-empty]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("add"), (list(intVals(.IntSeq)), .Exprs))
      =>
      0
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

  claim [entry-normal]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("add"),
           (list(intVals(
             iCons(4, iCons(2, iCons(6, iCons(7, .IntSeq))))
           )), .Exprs))
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
