requires "spec.k"

module AUDIT-BODY-SENSITIVITY
  imports SPEC

  // Fresh auditor mutation: change the executed closure's initial b from 1
  // to 3 while retaining the original summary destination.
  claim [changed-initial-b-to-3]:
    <k> Call(Name("prime_fib"), (Int(1), .Exprs))
      => primeFibSearch(1, 0, 0, 1)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
         "prime_fib" |-> closureVal(
           "n",
           Assign(Name("a"), Int(0))
           Assign(Name("b"), Int(3))
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
endmodule
