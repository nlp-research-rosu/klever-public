requires "verification-mutant.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-MUTANT

  claim [mutated-body-must-not-prove]:
    <k>
      #loadAll(mutantSolutionModule)
      ~> Call(
           Name("make_palindrome"),
           (str(iCons(99, iCons(97, iCons(116, .IntSeq)))), .Exprs))
      =>
      str(iCons(99, iCons(97, iCons(116, iCons(97, iCons(99, .IntSeq))))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "is_palindrome" |-> isPalindromeClosure
                  "make_palindrome" |-> mutantMakePalindromeClosure,
                  parent(-1)))
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
