requires "/tmp/audit-work/reconstruction/verification.k"

module GROUND-WITNESS-SPEC
  imports VERIFICATION

  claim [example]:
    <k>
      Call(
        solutionClosure,
        (list(vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq))))), .Exprs))
      => 12
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [negative-odd]:
    <k>
      Call(
        solutionClosure,
        (list(vCons(-5, vCons(2, vCons(-3, .ValSeq)))), .Exprs))
      => -8
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [empty-extension]:
    <k>
      Call(solutionClosure, (list(.ValSeq), .Exprs))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
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
