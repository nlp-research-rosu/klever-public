requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation: both intervals are valid and their geometric
  // intersection length is 3, so the candidate and canonical return "YES".
  // The deliberately mutated result obligation below demands "NO".
  claim [wrong-length-three-result]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("intersection"),
              TupleExpr(Int(10), Int(13)),
              TupleExpr(Int(0), Int(20)))
      => str(strToCodes("NO"))
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
