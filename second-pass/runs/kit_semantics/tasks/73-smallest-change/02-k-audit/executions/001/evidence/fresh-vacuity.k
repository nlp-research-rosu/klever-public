requires "/tmp/audit-work/candidate-src/verification.k"

module FRESH-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: [1,2] satisfies the source precondition and the
  // submitted program returns 1, so changing the required result to 2 is false.
  claim [wrong-two]:
    <k>
      #loadAll(Module(smallestDef))
      ~> Call(
           Name("smallest_change"),
           list(vCons(1, vCons(2, .ValSeq))))
      =>
      2
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
