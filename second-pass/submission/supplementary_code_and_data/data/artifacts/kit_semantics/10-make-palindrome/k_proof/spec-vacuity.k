requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-result]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("make_palindrome"),
           (str(.IntSeq), .Exprs))
      =>
      str(iCons(0, .IntSeq))
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
