requires "spec.k"

module AUDIT-FALSE-N5
  imports SPEC

  // Fresh auditor mutation. N=5 satisfies the entry precondition, but both
  // trusted Python executions and fresh LLVM execution return 89, not 88.
  claim [false-n5-result]:
    <k> Call(Name("prime_fib"), (Int(5), .Exprs)) => 88 </k>
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
endmodule
