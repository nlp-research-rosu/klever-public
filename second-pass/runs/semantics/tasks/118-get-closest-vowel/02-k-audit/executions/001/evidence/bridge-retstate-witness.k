requires "verification.k"

module AUDIT-BRIDGE-RETSTATE
  imports HUMAN-EVAL-118-VERIFICATION

  // Exact candidate-rule witness.  The bridge's match domain constrains only
  // <k> and <env>; it therefore fires even while a return is already pending.
  // Fixed function execution cannot complete a new Return while <ret> is
  // retV(7), because the supplied Return/#endcall rules require noRet.
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
