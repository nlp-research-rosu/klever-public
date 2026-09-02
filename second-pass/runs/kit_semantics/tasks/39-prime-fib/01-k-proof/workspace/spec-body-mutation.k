requires "spec.k"

module SPEC-BODY-MUTATION
  imports SPEC

  // Mutates only `b = 1` to `b = 2` while retaining the original result
  // postcondition.  A body-sensitive entry proof must reject this claim.
  claim [changed-initial-b]:
    <k> Call(Name("prime_fib"), (Int(N), .Exprs))
      => primeFibSearch(N, 0, 0, 1)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
         "prime_fib" |-> closureVal(
           "n",
           Assign(Name("a"), Int(0))
           Assign(Name("b"), Int(2))
           Assign(Name("count"), Int(0))
           Assign(Name("next_value"), Int(0))
           Assign(Name("divisor"), Int(2))
           Assign(Name("is_prime"), Bool(false))
           primeFibOuter
           Return(Name("a"))
           .Stmts,
           0),
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
