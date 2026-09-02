requires "spec.k"

module SPEC-VACUITY-AUDITOR
  imports MATCH-PARENS-SPEC

  // Deliberately false result mutation.  The original program and canonical
  // implementation both return Yes on ["", ""], and this state satisfies the
  // universal entry claim's precondition with A=B=.IntSeq, N=1, BASE=.Map.
  claim
    <k> #applyK(
          toCall(matchParensClosure),
          (list(vCons(str(.IntSeq),
                      vCons(str(.IntSeq), .ValSeq))), .Vals))
      => str(strToCodes("No"))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(("is_good" |-> isGoodClosure), parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(falseEmptyIsNo)]
endmodule
