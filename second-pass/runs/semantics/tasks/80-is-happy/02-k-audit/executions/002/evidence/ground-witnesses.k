requires "verification.k"

module GROUND-WITNESSES
  imports VERIFICATION

  claim [abc-true]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map [ "s" <- str(iCons(97, iCons(98, iCons(99, .IntSeq)))) ],
        parent(0)))
      => ?FINAL_SCOPES_ABC:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(true) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [aab-false]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map [ "s" <- str(iCons(97, iCons(97, iCons(98, .IntSeq)))) ],
        parent(0)))
      => ?FINAL_SCOPES_AAB:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(false) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [empty-false]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(.Map [ "s" <- str(.IntSeq) ], parent(0)))
      => ?FINAL_SCOPES_EMPTY:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(false) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
