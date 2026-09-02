requires "validation.k"

module SPEC-BODY-MUTATION
  imports VALIDATION

  // The old postcondition is false after changing count's initializer to 1:
  // on [11] the mutated program returns 2, not 1.
  claim [changed-body]:
    <k>
      Call(Name("count_nums"), list(vCons(11, .ValSeq)))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_nums" |-> mutatedCountNumsClosure,
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
