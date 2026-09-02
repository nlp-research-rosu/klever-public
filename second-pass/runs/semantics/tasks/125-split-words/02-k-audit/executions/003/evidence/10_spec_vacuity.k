requires "verification.k"

module SPEC-VACUITY
  imports SPLIT-WORDS-VERIFICATION

  // Fresh false result obligation.  The satisfying witness CS = .IntSeq has
  // both delimiter counts zero, while the real and modeled result is 0, not 1.
  claim [odd-lowercase-count]:
    <k>
      Call(solutionClosure, str(CS:IntSeq))
      => oddAlphabetCount(CS) +Int 1
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
