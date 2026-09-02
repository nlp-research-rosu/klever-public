requires "verification.k"

module FRESH-NONVACUITY
  imports VERIFICATION

  // Satisfiable initial state: the ordinary entry configuration with input
  // "cat". The real/canonical result is "catac"; this deliberately demands
  // the false, result-constraining alternative "catab".
  claim [wrong-cat-result]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("make_palindrome"),
           (str(iCons(99, iCons(97, iCons(116, .IntSeq)))), .Exprs))
      =>
      str(iCons(99, iCons(97, iCons(116, iCons(97, iCons(98, .IntSeq))))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "is_palindrome" |-> isPalindromeClosure
                  "make_palindrome" |-> makePalindromeClosure,
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
