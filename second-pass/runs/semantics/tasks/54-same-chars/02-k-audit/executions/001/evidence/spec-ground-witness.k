requires "verification.k"

module SAME-CHARS-SPEC-GROUND-WITNESS
  imports SAME-CHARS-VERIFICATION

  // Python inputs ("", ""): both distinct-code sets are empty.
  claim
    <k> #sameChars(.IntSeq, .IntSeq) => true </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Python inputs ("ab", "cd"): the distinct-code sets are disjoint.
  claim
    <k>
      #sameChars(
        iCons(97, iCons(98, .IntSeq)),
        iCons(99, iCons(100, .IntSeq)))
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
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
