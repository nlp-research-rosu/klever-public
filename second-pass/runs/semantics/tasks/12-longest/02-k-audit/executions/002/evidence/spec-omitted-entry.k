requires "spec.k"

module SPEC-OMITTED-ENTRY
  imports SPEC

  // The result-constraining theorem absent from the candidate.
  claim
    <k>
      Call(Name("longest"),
        list(stringVals(sCons(HEAD:IntSeq, TAIL:StringSeq))),
        .Exprs)
      => longestAcc(str(HEAD), TAIL)
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
    [label(omitted-entry-nonempty)]
endmodule
