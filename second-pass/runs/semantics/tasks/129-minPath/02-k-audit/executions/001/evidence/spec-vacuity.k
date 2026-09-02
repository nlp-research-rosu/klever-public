requires "verification.k"

module MINPATH-SPEC-VACUITY
  imports MINPATH-VERIFICATION

  // Reviewer mutation: the real result is [1,2,1], so requiring [1,3,1]
  // changes a reachable, result-constraining postcondition.
  claim [false-example-result]:
    <k>
      #loadAll(minPathProgram)
      ~> Call(
           Name("minPath"),
           list(vCons(
             list(vCons(1, vCons(2, vCons(3, .ValSeq)))),
             vCons(
               list(vCons(4, vCons(5, vCons(6, .ValSeq)))),
               vCons(
                 list(vCons(7, vCons(8, vCons(9, .ValSeq)))),
                 .ValSeq)))),
           Int(3))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(("minPath" |-> minPathClosure), parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(1, vCons(3, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
