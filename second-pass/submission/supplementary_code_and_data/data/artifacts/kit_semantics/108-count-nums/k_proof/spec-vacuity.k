requires "validation.k"

module SPEC-VACUITY
  imports VALIDATION

  // False for the satisfiable witness [11]: the real result is 1.
  claim [false-result]:
    <k>
      Call(Name("count_nums"), list(vCons(11, .ValSeq)))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_nums" |-> originalCountNumsClosure,
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
