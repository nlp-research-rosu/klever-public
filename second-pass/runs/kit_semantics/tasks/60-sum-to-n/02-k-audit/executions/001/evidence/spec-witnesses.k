requires "spec.k"

module SPEC-WITNESSES
  imports SPEC

  claim [empty-witness]:
    <k> Call(Name("sum_to_n"), Int(-3)) => 0 </k>
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

  claim [positive-witness]:
    <k> Call(Name("sum_to_n"), Int(5)) => 15 </k>
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
endmodule
