requires "verification.k"

module UNICODE-WITNESS-SPEC
  imports VERIFICATION

  // U+00E9 LATIN SMALL LETTER E WITH ACUTE, code point 233.
  // The supplied semantics classifies it as non-alpha, unlike Python isalpha().
  claim
    <k> #checkIfLastChar(str(iCons(233, .IntSeq))) => false </k>
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
