requires "verification.k"

module AUDITOR-FALSE-POSTCONDITION
  imports VERIFICATION

  // Fresh non-vacuity mutation. [1,2,3] satisfies allInts and the documented
  // behavior is false, so requiring true must leave an unmet final result.
  claim [positive-list-is-true]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List")
        FuncDef("below_zero", Params("operations"),
          Assign(Name("balance"), Int(0))
          Assign(Name("operation"), Int(0))
          For(Name("operation"), Name("operations"),
            AugAssign(Name("balance"), "+", Name("operation"))
            If(Compare(Name("balance"), CmpOp("<", Int(0))),
              Return(Bool(true)), .Stmts))
          Return(Bool(false)))))
      ~> Call(Name("below_zero"), list(vCons(1, vCons(2, vCons(3, .ValSeq)))))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "below_zero" |-> closureVal(
          "operations", .ParamNames,
          Assign(Name("balance"), Int(0))
          Assign(Name("operation"), Int(0))
          For(Name("operation"), Name("operations"),
            AugAssign(Name("balance"), "+", Name("operation"))
            If(Compare(Name("balance"), CmpOp("<", Int(0))),
              Return(Bool(true)), .Stmts))
          Return(Bool(false)), 0),
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
