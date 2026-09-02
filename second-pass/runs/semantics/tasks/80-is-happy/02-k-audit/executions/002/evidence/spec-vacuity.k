requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfying input "abc": all three characters differ, so
  // both Python implementations and isHappySpec return true, not false.
  claim [abc-wrong-result]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map [ "s" <- str(iCons(97, iCons(98, iCons(99, .IntSeq)))) ],
        parent(0)))
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet => retV(false) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
