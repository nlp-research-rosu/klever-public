requires "verification.k"

module MATCH-PARENS-SPEC-VACUITY-GROUND
  imports MATCH-PARENS-VERIFICATION

  // False result mutation at the satisfying intended-domain input ["", ""].
  // The program and expectedAnswer both return "Yes"; this deliberately asks
  // the prover to establish "Wrong".
  claim
    <k> #applyK(
          toCall(matchParensClosure),
          (list(vCons(str(.IntSeq),
                      vCons(str(.IntSeq), .ValSeq))), .Vals))
         ~> .K
      => str(strToCodes("Wrong")) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_good" |-> isGoodClosure,
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(matchParensGroundFalseResult)]
endmodule
