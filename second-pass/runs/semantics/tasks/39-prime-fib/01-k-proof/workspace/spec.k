requires "verification.k"

module PRIME-FIB-SPEC
  imports PRIME-FIB-VERIFICATION

  // These claims cover the first eleven Fibonacci primes, including all five
  // examples in prompt.py. An unrestricted total-correctness claim for every
  // positive n would imply that infinitely many Fibonacci primes exist, which
  // is not currently known; the executable remains a general search.

  claim [pf1]:
    <k> Call(Name("prime_fib"), Int(1)) => 2 </k>
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

  claim [pf2]:
    <k> Call(Name("prime_fib"), Int(2)) => 3 </k>
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

  claim [pf3]:
    <k> Call(Name("prime_fib"), Int(3)) => 5 </k>
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

  claim [pf4]:
    <k> Call(Name("prime_fib"), Int(4)) => 13 </k>
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

  claim [pf5]:
    <k> Call(Name("prime_fib"), Int(5)) => 89 </k>
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

  claim [pf6]:
    <k> Call(Name("prime_fib"), Int(6)) => 233 </k>
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

  claim [pf7]:
    <k> Call(Name("prime_fib"), Int(7)) => 1597 </k>
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

  claim [pf8]:
    <k> Call(Name("prime_fib"), Int(8)) => 28657 </k>
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

  claim [pf9]:
    <k> Call(Name("prime_fib"), Int(9)) => 514229 </k>
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

  claim [pf10]:
    <k> Call(Name("prime_fib"), Int(10)) => 433494437 </k>
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

  claim [pf11]:
    <k> Call(Name("prime_fib"), Int(11)) => 2971215073 </k>
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
