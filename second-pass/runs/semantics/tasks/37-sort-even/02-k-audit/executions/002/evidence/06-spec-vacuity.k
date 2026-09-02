requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Satisfiable entry state, but deliberately false result:
  // real result for [5, 6, 3, 4] is [3, 6, 5, 4], not [4, 6, 5, 4].
  claim [false-result]:
    <k>
      Call(
        Name("sort_even"),
        list(vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq))))))
      ~> #observeResult
    =>
      list(vCons(4, vCons(6, vCons(5, vCons(4, .ValSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
        ("sort_even" |-> sortEvenClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HEAP </heap>
    <heapLoc> 0 => ?HL </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
