requires "spec-body-mutated.k"

module GROUND-WITNESS-BODY-MUTATED
  imports MATCH-PARENS-SPEC-BODY-MUTATED

  // The translated mutant's helper always returns the empty string, so its
  // real result on ["", ""] is No.  The proof rules nevertheless derive Yes.
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
    [label(groundMutantFalseYes)]
endmodule
