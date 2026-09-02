requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Realizable witness [1, 2] returns 1.  The deliberately false result 0
  // must be rejected.
  claim [wrong-result]:
    <k>
      #loadAll(Module(smallestDef))
      ~> Call(
           Name("smallest_change"),
           list(vCons(1, vCons(2, .ValSeq))))
      =>
      0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", smallestBody, 0),
             parent(-1))
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
