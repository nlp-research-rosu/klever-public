requires "/tmp/audit-work/37-sort-even-audit/reconstruction-fresh/spec.k"

module GROUND-SPEC
  imports SPEC

  // A ground instance of the exact entry precondition for the documented
  // even-length branch input [5, 6, 3, 4].
  claim [ground-example]:
    <k>
      Call(
        Name("sort_even"),
        list(vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq))))))
      ~> #observeResult
    =>
      list(vCons(3, vCons(6, vCons(5, vCons(4, .ValSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
        ("sort_even" |-> sortEvenClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?GROUNDHEAP </heap>
    <heapLoc> 0 => ?GROUNDHL </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
