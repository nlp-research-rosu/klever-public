requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for every 1 <= N < 10, the executed even count is
  // evenPalindromes(N), not evenPalindromes(N) + 1.
  claim
    <k>
      #runEvenOdd(N:Int)
      =>
      tuple(vCons((evenPalindromes(N) +Int 1),
            vCons(oddPalindromes(N), .ValSeq)))
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
    requires 1 <=Int N andBool N <Int 10

endmodule
