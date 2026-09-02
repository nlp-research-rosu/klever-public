requires "verification.k"

module PRIME-FIB-SPEC-VACUITY
  imports PRIME-FIB-VERIFICATION

  // Deliberately false: the actual result of prime_fib(1) is 2, not 3.
  claim [pf1-false-result]:
    <k> Call(Name("prime_fib"), Int(1)) => 3 </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
              ("_is_prime" |-> isPrimeClosure)
              ("prime_fib" |-> primeFibClosure),
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
