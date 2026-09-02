requires "verification.k"

module SPEC-VACUITY-REVIEW
  imports VERIFICATION

  // Fresh false mutation: the acceptance region is required to return "No".
  // Satisfying counterexample under the intended observations: "a123.txt".
  claim
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
