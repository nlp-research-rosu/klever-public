requires "spec.k"

module GROUND-WITNESS
  imports MATCH-PARENS-SPEC

  // A = B = empty, BASE = MODULELOCALS = empty, N = 1 satisfies every
  // matchParensCorrect precondition.  Its expected answer is explicitly Yes.
  claim
    <k> #applyK(
          toCall(matchParensClosure),
          (list(vCons(str(.IntSeq),
                      vCons(str(.IntSeq), .ValSeq))), .Vals))
      => str(strToCodes("Yes"))
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
    [label(groundEmpty)]
endmodule
