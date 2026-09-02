requires "verification.k"

module SPEC
  imports VERIFICATION

  // Full target: load the exact translated module, install its exact closure,
  // invoke the required entry point, and characterize every finite Int list.
  claim [below-zero]:
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
      ~> Call(Name("below_zero"), list(INPUT:ValSeq))
      => belowFrom(0, INPUT)
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
          Return(Bool(false)),
          0),
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
    requires allInts(INPUT)
endmodule
