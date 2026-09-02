requires "verification.k"

module SPEC
  imports SPLIT-WORDS-VERIFICATION

  // Any modeled whitespace takes precedence and no-argument split drops runs
  // of whitespace, as required by the task.
  claim [whitespace]:
    <k> Call(solutionClosure, str(CS:IntSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("$proofPath" |-> 1, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(splitWS(CS, .IntSeq, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires whitespaceCount(CS) >Int 0

  // With no whitespace and at least one comma, explicit-separator split keeps
  // empty fields exactly like Python str.split(",").
  claim [comma]:
    <k> Call(solutionClosure, str(CS:IntSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("$proofPath" |-> 2, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(splitSep(CS, 44, .IntSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires whitespaceCount(CS) <=Int 0
     andBool commaCount(CS) >Int 0

  // If neither delimiter class occurs, the result counts exactly the lowercase
  // letters at odd zero-based alphabet positions: b,d,...,z.
  claim [odd-lowercase-count]:
    <k> Call(solutionClosure, str(CS:IntSeq)) => oddAlphabetCount(CS) </k>
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
