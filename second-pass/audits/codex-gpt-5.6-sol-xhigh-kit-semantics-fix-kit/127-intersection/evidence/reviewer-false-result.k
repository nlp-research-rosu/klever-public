requires "verification.k"

module REVIEWER-FALSE-RESULT
  imports VERIFICATION

  // Fresh reviewer mutation: this satisfying branch-2 input has intersection
  // length min(5,5)-max(0,2) = 3, so the submitted program returns YES.
  // The destination is deliberately mutated to the false result NO.
  claim [false-prime-result]:
    <k> #loadAll(SOLUTION-MODULE)
         ~> Call(Name("intersection"),
                 (tuple(vCons(0, vCons(5, .ValSeq))),
                  tuple(vCons(2, vCons(5, .ValSeq))),
                  .Exprs))
      => str(iCons(78, iCons(79, .IntSeq))) </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(
               "intersection" |->
                 closureVal(("interval1", "interval2", .ParamNames),
                            INTERSECTION-BODY, 0),
               parent(-1))
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
