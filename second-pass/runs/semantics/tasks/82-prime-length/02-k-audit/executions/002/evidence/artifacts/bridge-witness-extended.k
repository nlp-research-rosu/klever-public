requires "verification.k"

module BRIDGE-WITNESS-EXTENDED
  imports VERIFICATION

  // False relative to fixed execution: the real length-two call returns true,
  // while the proof bridge preempts its While and fabricates this marker.
  claim [fabricated-marker]:
    <k>
      #applyK(
        toCall(primeLengthClosure),
        (str(iCons(97, iCons(98, .IntSeq))), .Vals))
      =>
      #primeLoopEntry(2, 2)
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
