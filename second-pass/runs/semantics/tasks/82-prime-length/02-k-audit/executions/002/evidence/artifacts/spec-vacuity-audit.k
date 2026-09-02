requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the satisfying witnesses CS=.IntSeq and
  // CS=iCons(97,.IntSeq) make the real body return false, not true.
  claim [prime-length-small-false]:
    <k>
      #applyK(
        toCall(primeLengthClosure),
        (str(CS:IntSeq), .Vals))
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
    requires isLen(CS) >=Int 0
     andBool isLen(CS) <Int 2
endmodule
