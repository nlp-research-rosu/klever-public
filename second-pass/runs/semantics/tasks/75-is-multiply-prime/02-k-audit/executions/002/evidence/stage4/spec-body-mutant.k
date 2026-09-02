requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // The executed body was changed from factor_count == 3 to factor_count == 4.
  // Input 8 has exactly three prime factors, so the original true obligation
  // must now become stuck at false ~> #expect(true).
  claim <k> #runIsMultiplyPrime(8) ~> #expect(true) => .K </k>
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
