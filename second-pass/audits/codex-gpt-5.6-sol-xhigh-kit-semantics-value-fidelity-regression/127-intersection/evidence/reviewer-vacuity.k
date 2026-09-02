requires "verification.k"

module REVIEWER-VACUITY
  imports VERIFICATION

  // Fresh false result obligation.  These well-formed intervals have
  // overlapLength = 2, so both implementations and intersectionResult return
  // "YES"; the mutation requires "NO".
  claim [false-length-two-result]:
    <k>
      Call(Name("intersection"),
           TupleExpr(Int(-3), Int(-1)),
           TupleExpr(Int(-5), Int(5)))
      => str(iCons(78, iCons(79, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("intersection" |-> intersectionClosure, parent(-1))
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
