requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed module term itself has a materially changed helper body.
  // At the satisfying ground input 12 it returns 0, so the unchanged
  // signedDigitSum(12) result obligation must be rejected.
  claim [changed-executed-helper-body]:
    <k>
      #loadAll(
        Module(
          FuncDef("digit_sum", Params("number"), Return(Int(0)))
          FuncDef("order_by_points", Params("nums"), orderByPointsBody)))
      ~> Call(Name("digit_sum"), (Int(12), .Exprs))
      => signedDigitSum(12)
    </k>
    <env> 0 </env>
    <scopes>
        0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
        0 |-> scope(
          "digit_sum" |-> closureVal("number", Return(Int(0)), 0)
          "order_by_points" |->
            closureVal("nums", orderByPointsBody, 0),
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
