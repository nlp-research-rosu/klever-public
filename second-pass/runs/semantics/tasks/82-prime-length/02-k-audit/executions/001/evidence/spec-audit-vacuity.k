requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation of the result-constraining small-input claim.
  // The empty string satisfies the original precondition, but the real result
  // is false; this deliberately and incorrectly demands true.
  claim [false-small-result]:
    <k>
      #applyK(
        toCall(primeLengthClosure),
        (str(.IntSeq), .Vals))
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
endmodule
