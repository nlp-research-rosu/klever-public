requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the empty input really returns an empty list, but this
  // mutation demands a one-element list containing "()".
  claim [false-empty-result]:
    <k> Call(Name("separate_paren_groups"),
             (str(.IntSeq), .Exprs))
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope("separate_paren_groups" |-> solutionClosure,
                   parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(str(strToCodes("()")), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

endmodule
