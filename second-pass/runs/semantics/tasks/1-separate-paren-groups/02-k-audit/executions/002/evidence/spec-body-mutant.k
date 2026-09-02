requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // The term actually executed by this claim increments on ")" instead of
  // decrementing; the correct prompt result must therefore become unprovable.
  claim [prompt-result-under-mutated-body]:
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
           vCons(str(strToCodes("()")),
           vCons(str(strToCodes("(())")),
           vCons(str(strToCodes("(()())")), .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
