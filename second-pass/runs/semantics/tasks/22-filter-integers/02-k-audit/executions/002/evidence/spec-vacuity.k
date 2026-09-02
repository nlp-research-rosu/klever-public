requires "verification.k"

module FILTER-SPEC-VACUITY
  imports FILTER-VERIFICATION

  // Deliberately false result mutation.
  // Satisfying witness: the ordinary initial state below with empty input.
  // The real execution returns ref(0) whose heap object is list(.ValSeq), not [0].
  claim [false-empty-result]:
    <k> #loadAll(FILTER-PROGRAM)
         ~> Call(Name("filter_integers"), list(.ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope("filter_integers" |-> FILTER-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(vCons(0, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
