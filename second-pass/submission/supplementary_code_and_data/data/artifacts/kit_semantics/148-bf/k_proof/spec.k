requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [bf-correct]:
    <k> #loadAll(bfModule) ~> bfCall(P1:IntSeq, P2:IntSeq)
        => tuple(betweenPlanets(P1, P2)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"), bfBody, 0),
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
