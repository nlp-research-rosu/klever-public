requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfying prompt input: the real first group is "()".
  claim [wrong-prompt-result]:
    <k> Call(Name("separate_paren_groups"),
             (str(strToCodes("( ) (( )) (( )( ))")), .Exprs))
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
      => 0 |-> list(
           vCons(str(strToCodes("(WRONG)")),
           vCons(str(strToCodes("(())")),
           vCons(str(strToCodes("(()())")), .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
