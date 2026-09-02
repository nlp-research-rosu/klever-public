requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [inner-loop]:
    <k> primeFibInnerCore => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "n"          |-> N:Int
        "a"          |-> A:Int
        "b"          |-> B:Int
        "count"      |-> C:Int
        "next_value" |-> NV:Int
        "divisor"    |-> (D:Int => ?DF:Int)
        "is_prime"   |-> (P:Bool => primeScan(A, D, P)),
        parent(0))
      ...
    </scopes>
    requires A >=Int 0
     andBool D >=Int 2

  claim [outer-loop]:
    <k> primeFibOuterCore => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "n"          |-> N:Int
        "a"          |-> (A:Int  => primeFibSearch(N, C, A, B))
        "b"          |-> (B:Int  => ?BF:Int)
        "count"      |-> (C:Int  => ?CF:Int)
        "next_value" |-> (NV:Int => ?NVF:Int)
        "divisor"    |-> (D:Int  => ?DF:Int)
        "is_prime"   |-> (P:Bool => ?PF:Bool),
        parent(0))
      ...
    </scopes>
    requires N >=Int 1
     andBool A >=Int 0
     andBool B >=Int 1

  claim [prime-fib]:
    <k> Call(Name("prime_fib"), (Int(N), .Exprs))
      => primeFibSearch(N, 0, 0, 1)
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
