requires "../../tmp/audit-work/pairs-audit/verification.k"

module AUDIT-GROUND-SPEC
  imports PAIRS-VERIFICATION

  // Fixed-semantics executions over ordinary vCons lists.  These claims do not
  // import the promoted loop or abstract-empty-list rules.
  claim [real-empty]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(.ValSeq), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [real-single-zero]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(vCons(0, .ValSeq)), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(0, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [real-double-zero]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(vCons(0, vCons(0, .ValSeq))), .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(0, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [real-late-pair]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(vCons(2,
                 vCons(4,
                 vCons(-5,
                 vCons(3,
                 vCons(5,
                 vCons(7, .ValSeq))))))), .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(2,
                   vCons(4,
                   vCons(-5,
                   vCons(3, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [real-no-pair]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(vCons(1,
                 vCons(3,
                 vCons(-2,
                 vCons(1, .ValSeq))))), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(1,
                   vCons(3,
                   vCons(-2,
                   vCons(1, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Concrete substitutions into the universal claim's formal result.
  claim [formal-empty]:
    <k> pairsIS(.IntSeq) => false </k>

  claim [formal-single-zero]:
    <k> pairsIS(iCons(0, .IntSeq)) => false </k>

  claim [formal-double-zero]:
    <k> pairsIS(iCons(0, iCons(0, .IntSeq))) => true </k>

  claim [formal-late-pair]:
    <k>
      pairsIS(iCons(2,
              iCons(4,
              iCons(-5,
              iCons(3,
              iCons(5,
              iCons(7, .IntSeq)))))))
      => true
    </k>

  claim [formal-no-pair]:
    <k>
      pairsIS(iCons(1,
              iCons(3,
              iCons(-2,
              iCons(1, .IntSeq)))))
      => false
    </k>
endmodule
