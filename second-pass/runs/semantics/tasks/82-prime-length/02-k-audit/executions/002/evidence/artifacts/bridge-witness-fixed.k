requires "verification-fixed.k"

module BRIDGE-WITNESS-FIXED
  imports VERIFICATION-FIXED

  // Expected success under the fixed supplied semantics.
  claim [real-result]:
    <k>
      #applyK(
        toCall(primeLengthClosureFixed),
        (str(iCons(97, iCons(98, .IntSeq))), .Vals))
      =>
      true
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

  // Expected failure: fixed execution has no path to this invented marker.
  claim [fabricated-marker]:
    <k>
      #applyK(
        toCall(primeLengthClosureFixed),
        (str(iCons(97, iCons(98, .IntSeq))), .Vals))
      =>
      #primeLoopEntryFixed(2, 2)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      .Map
    </scopes>
    <scopeLoc> 1 => 0 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
