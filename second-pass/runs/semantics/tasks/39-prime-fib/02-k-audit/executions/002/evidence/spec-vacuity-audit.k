requires "verification.k"

module PRIME-FIB-SPEC-VACUITY-AUDIT
  imports PRIME-FIB-VERIFICATION

  // Fresh reviewer mutation of pf1: the real result for this satisfiable
  // initial state is 2, so requiring 3 must leave an unmet obligation.
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
