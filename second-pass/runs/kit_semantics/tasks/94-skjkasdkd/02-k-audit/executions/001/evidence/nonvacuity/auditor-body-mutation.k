requires "verification.k"

module AUDITOR-BODY-MUTATION
  imports VERIFICATION

  // Material mutation: initialize largest to 2. Empty input then returns 2,
  // while the original submitted body returns 0.
  claim [auditor-mutated-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "skjkasdkd",
            Params("lst"),
            Assign(Name("largest"), Int(2))
            Assign(Name("value"), Int(0))
            Assign(Name("candidate"), Bool(false))
            Assign(Name("divisor"), Int(2))
            For(Name("value"), Name("lst"), scanBody)
            Assign(Name("total"), Int(0))
            While(
              Compare(Name("largest"), CmpOp(">", Int(0))),
              digitLoopBody)
            Return(Name("total")))))
      ~> Call(Name("skjkasdkd"), list(.ValSeq))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "skjkasdkd" |->
             closureVal(
               ("lst", .ParamNames),
               Assign(Name("largest"), Int(2))
               Assign(Name("value"), Int(0))
               Assign(Name("candidate"), Bool(false))
               Assign(Name("divisor"), Int(2))
               For(Name("value"), Name("lst"), scanBody)
               Assign(Name("total"), Int(0))
               While(
                 Compare(Name("largest"), CmpOp(">", Int(0))),
                 digitLoopBody)
               Return(Name("total")),
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
endmodule
