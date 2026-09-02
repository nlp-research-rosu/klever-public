requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: input 5 produces the odd trace [5, 1], so the result
  // object is sortVS([5, 1]), not sortVS([7, 1]).
  claim
    <k> #getOddCollatz(5) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        .Map [ "get_odd_collatz" <- getOddCollatzClosure ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(5, vCons(1, .ValSeq)))
      1 |-> list(sortVS(vCons(7, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(false-case-5-result)]
endmodule
