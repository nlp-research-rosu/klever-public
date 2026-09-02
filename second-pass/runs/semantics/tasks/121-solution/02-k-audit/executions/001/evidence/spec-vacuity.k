requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False mutation: the submitted program returns 12 for this satisfying input,
  // while this result-constraining target deliberately requires 13.
  claim [false-result-13]:
    <k>
      Call(
        solutionClosure,
        (list(vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq))))), .Exprs))
      =>
      13
    </k>
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
