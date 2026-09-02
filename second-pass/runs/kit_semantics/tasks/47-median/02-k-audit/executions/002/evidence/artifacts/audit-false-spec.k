requires "verification.k"

module AUDIT-FALSE-SPEC
  imports VERIFICATION

  // [9, 1, 5] has median 5.  Requiring 6 is deliberately false.
  claim [audit-false-odd-result]:
    <k>
      Call(
        Name("median"),
        list(vCons(9, vCons(1, vCons(5, .ValSeq)))))
      =>
      6
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(vCons(9, vCons(1, vCons(5, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
