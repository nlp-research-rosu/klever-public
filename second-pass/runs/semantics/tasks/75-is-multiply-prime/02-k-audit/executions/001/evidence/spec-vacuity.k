requires "verification.k"

// Reviewer-authored false mutation.  The original SPEC-72-81 obligation
// requires is_multiply_prime(75) == true.  This claim instead demands false
// from the same realizable initial configuration.
module SPEC-VACUITY
  imports VERIFICATION

  claim <k> #runIsMultiplyPrime(75) => false </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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
