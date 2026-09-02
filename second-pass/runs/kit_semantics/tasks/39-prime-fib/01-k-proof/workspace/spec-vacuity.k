requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  claim [false-result]:
    <k> Call(Name("prime_fib"), (Int(N), .Exprs))
      => primeFibSearch(N, 0, 0, 1) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
         "prime_fib" |-> closureVal("n", primeFibBody, 0),
         parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
endmodule
