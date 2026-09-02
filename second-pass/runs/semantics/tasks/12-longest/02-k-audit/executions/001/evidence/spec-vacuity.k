requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: longest([]) returns noneV, never an empty string.
  claim
    <k>
      Call(Name("longest"), list(stringVals(.StringSeq)), .Exprs)
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("longest" |-> longestSolution, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(false-call-empty)]

endmodule
