requires "verification.k"

module FILTER-SPEC-VACUITY-REVIEW
  imports FILTER-VERIFICATION

  // [] satisfies the original empty claim's precondition, but the real
  // function returns []; requiring [1] is a meaningful false result mutation.
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
    <heap> .Map => 0 |-> list(vCons(1, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
