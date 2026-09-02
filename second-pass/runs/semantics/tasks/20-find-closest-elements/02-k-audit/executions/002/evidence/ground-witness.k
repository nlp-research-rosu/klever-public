requires "/tmp/audit-work/task20/verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  claim [two-ascending]:
    <k>
      #applyK(
        toCall(closureVal(("numbers", .ParamNames), findClosestBody, 0)),
        (list(floatVals(fCons(1.0, fCons(2.0, .FloatSeq)))), .Vals))
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

  claim [two-descending]:
    <k>
      #applyK(
        toCall(closureVal(("numbers", .ParamNames), findClosestBody, 0)),
        (list(floatVals(fCons(2.0, fCons(1.0, .FloatSeq)))), .Vals))
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

  claim [three-elements]:
    <k>
      #applyK(
        toCall(closureVal(("numbers", .ParamNames), findClosestBody, 0)),
        (list(floatVals(
          fCons(9.0, fCons(-2.0, fCons(4.0, .FloatSeq))))), .Vals))
      => tuple(vCons(4.0, vCons(9.0, .ValSeq)))
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
