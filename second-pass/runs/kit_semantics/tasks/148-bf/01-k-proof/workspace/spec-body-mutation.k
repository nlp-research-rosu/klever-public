requires "verification-mutant.k"

module SPEC-BODY-MUTATION
  imports MUTATION

  // The original contract requires ("Venus",) for this witness.
  claim [changed-body-rejected]:
    <k> #loadAll(mutantModule)
         ~> bfCall(strToCodes("Mercury"), strToCodes("Earth"))
        => tuple(betweenPlanets(strToCodes("Mercury"),
                               strToCodes("Earth"))) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"),
                                               mutantBody, 0),
                    parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
