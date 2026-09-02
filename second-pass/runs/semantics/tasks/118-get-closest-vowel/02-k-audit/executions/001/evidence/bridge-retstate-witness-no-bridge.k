requires "verification-no-recursive-bridge.k"

module AUDIT-BRIDGE-RETSTATE-NO-BRIDGE
  imports HUMAN-EVAL-118-VERIFICATION

  claim
    <k> #applyK(
          toCall(closureVal("word", getClosestBody, 0)),
          (str(iCons(98, iCons(98, iCons(98, .IntSeq)))), .Vals))
      => str(.IntSeq)
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(.Map, parent(0))
      0 |-> scope(
             "get_closest_vowel"
               |-> closureVal("word", getClosestBody, 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> retV(7) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
