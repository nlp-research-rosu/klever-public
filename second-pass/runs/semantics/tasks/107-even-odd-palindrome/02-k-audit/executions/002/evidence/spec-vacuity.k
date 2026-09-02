requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False mutation: for the satisfying input N = 1, require one even
  // palindrome instead of the actual zero.
  claim
    <k>
      #runEvenOdd(1)
      =>
      tuple(vCons(1, vCons(1, .ValSeq)))
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
