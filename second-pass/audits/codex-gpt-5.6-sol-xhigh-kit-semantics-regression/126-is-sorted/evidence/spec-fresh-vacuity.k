requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-FRESH-VACUITY
  imports VERIFICATION

  // Deliberately false reviewer mutation. [0, 1] satisfies nonNegativeInts,
  // and both the program and sortedScan return true, not false.
  claim [ascending-pair-is-false]:
    <k> #loadAll(isSortedModule)
        ~> Call(
             Name("is_sorted"),
             (list(vCons(0, vCons(1, .ValSeq))), .Exprs))
        => false
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
              "is_sorted" |->
                closureVal(
                  ("lst", .ParamNames),
                  isSortedBody,
                  0),
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
