requires "verification.k"

module SPEC-BODY-SENSITIVITY-REVIEWER
  imports VERIFICATION

  // The actual executed closure is changed from total += n to total -= n.
  // For N=2 the mutated body returns -3, so the original result 3 must fail.
  claim [changed-loop-body]:
    <k> Call(Name("sum_to_n"), Int(2)) => ?R:Int </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
         "sum_to_n" |-> closureVal(
           "n", .ParamNames,
           Assign(Name("total"), Int(0))
           While(Compare(Name("n"), CmpOp(">", Int(0))),
             AugAssign(Name("total"), "-", Name("n"))
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
    ensures ?R ==Int 3
endmodule
