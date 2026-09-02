requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [sum-loop]:
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(0))),
        AugAssign(Name("total"), "+", Name("n"))
        AugAssign(Name("n"), "-", Int(1)))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |-> scope(
        ("n" |-> (N:Int => 0)
         "total" |-> (S:Int => S +Int sumToN(N))),
        parent(0))
      ...
    </scopes>
    requires N >=Int 0

  claim [sum-to-n-empty-range]:
    <k>
      Call(Name("sum_to_n"), Int(N))
      => ?R:Int
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
         "sum_to_n" |-> closureVal(
           "n", .ParamNames,
           Assign(Name("total"), Int(0))
           While(Compare(Name("n"), CmpOp(">", Int(0))),
             AugAssign(Name("total"), "+", Name("n"))
             AugAssign(Name("n"), "-", Int(1)))
           Return(Name("total")),
           0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N <=Int 0
    ensures ?R ==Int 0

  claim [sum-to-n-positive]:
    <k>
      Call(Name("sum_to_n"), Int(N))
      => ?R:Int
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
         "sum_to_n" |-> closureVal(
           "n", .ParamNames,
           Assign(Name("total"), Int(0))
           While(Compare(Name("n"), CmpOp(">", Int(0))),
             AugAssign(Name("total"), "+", Name("n"))
             AugAssign(Name("n"), "-", Int(1)))
           Return(Name("total")),
           0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    ensures ?R ==Int sumToN(N)
endmodule
