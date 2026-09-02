requires "verification.k"

module GROUND-SUBSTITUTIONS
  imports VERIFICATION

  claim [empty-is-false]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(.Map [ "s" <- str(.IntSeq) ], parent(0)))
    => ?FINAL_SCOPES_1:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(false) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [abc-is-true]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map [ "s" <- str(iCons(97, iCons(98, iCons(99, .IntSeq)))) ],
        parent(0)))
    => ?FINAL_SCOPES_2:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(true) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [aba-is-false]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map [ "s" <- str(iCons(97, iCons(98, iCons(97, .IntSeq)))) ],
        parent(0)))
    => ?FINAL_SCOPES_3:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(false) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [abcd-is-true]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "s" <- str(iCons(97, iCons(98, iCons(99, iCons(100, .IntSeq))))) ],
        parent(0)))
    => ?FINAL_SCOPES_4:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(true) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
