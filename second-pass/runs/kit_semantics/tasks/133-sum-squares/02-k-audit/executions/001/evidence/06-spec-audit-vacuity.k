requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: the satisfying input [1,2,3] returns 14, so the
  // destination 15 is a reachable, result-constraining false obligation.
  claim [false-entry-result]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(
           Name("sum_squares"),
           list(vCons(1, vCons(2, vCons(3, .ValSeq)))))
      => 15
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope)
      =>
      (0 |-> scope(?MUTGLOBALS:Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
