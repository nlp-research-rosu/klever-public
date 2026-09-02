requires "verification.k"

module SPEC-VACUITY
  imports SPLIT-WORDS-VERIFICATION

  // Deliberately false: "abcdef" satisfies the precondition, and both the
  // candidate body and oddAlphabetCount return 3, not 4.
  claim [odd-lowercase-count-plus-one]:
    <k>
      Call(solutionClosure, str(CS:IntSeq))
      =>
      oddAlphabetCount(CS) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("$proofPath" |-> 3, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires whitespaceCount(CS) <=Int 0
     andBool commaCount(CS) <=Int 0
endmodule
