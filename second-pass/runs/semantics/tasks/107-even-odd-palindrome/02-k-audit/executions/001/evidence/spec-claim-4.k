requires "verification.k"

module SPEC-CLAIM-4
  imports VERIFICATION

  claim
    <k>
      #runEvenOdd(1000)
      =>
      tuple(vCons(evenPalindromes(1000),
            vCons(oddPalindromes(1000), .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "even_odd_palindrome"
                 |-> closureVal("n", solutionBody, 0),
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
