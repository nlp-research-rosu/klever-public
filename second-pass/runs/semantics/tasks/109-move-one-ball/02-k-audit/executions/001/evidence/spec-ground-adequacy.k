requires "verification.k"

module SPEC-GROUND-ADEQUACY
  imports VERIFICATION

  claim [wrapper-empty]:
    <k> Call(Name("move_one_ball"), list(intVals(.IntSeq))) => true </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("move_one_ball" |-> MOVE-ONE-BALL-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc>
    <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [wrapper-documented-true]:
    <k>
      Call(Name("move_one_ball"),
        list(intVals(iCons(3, iCons(4, iCons(5, iCons(1, iCons(2, .IntSeq))))))))
      =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("move_one_ball" |-> MOVE-ONE-BALL-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc>
    <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [wrapper-documented-false]:
    <k>
      Call(Name("move_one_ball"),
        list(intVals(iCons(3, iCons(5, iCons(4, iCons(1, iCons(2, .IntSeq))))))))
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("move_one_ball" |-> MOVE-ONE-BALL-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc>
    <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // These two claims use the supplied semantics' real vCons list representation,
  // not the proof-local intVals representation.
  claim [real-list-documented-true]:
    <k>
      Call(Name("move_one_ball"),
        list(vCons(3, vCons(4, vCons(5, vCons(1, vCons(2, .ValSeq)))))))
      =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("move_one_ball" |-> MOVE-ONE-BALL-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc>
    <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [real-list-documented-false]:
    <k>
      Call(Name("move_one_ball"),
        list(vCons(3, vCons(5, vCons(4, vCons(1, vCons(2, .ValSeq)))))))
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("move_one_ball" |-> MOVE-ONE-BALL-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc>
    <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
