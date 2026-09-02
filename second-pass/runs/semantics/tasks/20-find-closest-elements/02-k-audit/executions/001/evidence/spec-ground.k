requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  claim [two-elements-swapped]:
    <k>
      #applyK(
        toCall(closureVal(("numbers", .ParamNames), findClosestBody, 0)),
        (list(vCons(2.0, vCons(1.0, .ValSeq))), .Vals))
      => tuple(vCons(1.0, vCons(2.0, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [documented-example]:
    <k>
      #applyK(
        toCall(closureVal(("numbers", .ParamNames), findClosestBody, 0)),
        (list(vCons(1.0,
              vCons(2.0,
              vCons(3.0,
              vCons(4.0,
              vCons(5.0,
              vCons(2.2, .ValSeq))))))), .Vals))
      => tuple(vCons(2.0, vCons(2.2, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
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
