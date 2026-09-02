requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // The original result obligation for N = 1, applied to a material mutation
  // of the program term actually loaded by #runEvenOdd.
  claim
    <k>
      #runEvenOdd(1)
      =>
      tuple(vCons(evenPalindromes(1),
            vCons(oddPalindromes(1), .ValSeq)))
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
