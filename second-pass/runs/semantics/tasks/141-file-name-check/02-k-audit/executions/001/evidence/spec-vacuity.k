requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false mutation of the acceptance claim: all original
  // acceptance preconditions are unchanged, but "Yes" is replaced by "No".
  // "a123.txt" is a concrete satisfying witness and both Python functions
  // return "Yes" for it.
  claim [false-acceptance-result]:
    <k> runFileNameCheck(CS:IntSeq)
      => str(iCons(78, iCons(111, .IntSeq))) </k>
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
    requires charCount(CS, 46) ==Int 1
     andBool isLen(CS) >=Int 5
     andBool latinCode(headCode(CS))
     andBool allowedSuffix(CS)
     andBool digitCount(CS) <=Int 3
endmodule
