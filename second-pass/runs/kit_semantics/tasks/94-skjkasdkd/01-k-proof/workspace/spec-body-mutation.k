requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The exact target body with one material mutation: total starts at 1.
  // On input [2] the mutated program returns 3, so the original result 2
  // must be rejected.
  claim [mutated-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "skjkasdkd",
            Params("lst"),
            Assign(Name("largest"), Int(0))
            Assign(Name("value"), Int(0))
            Assign(Name("candidate"), Bool(false))
            Assign(Name("divisor"), Int(2))
            For(Name("value"), Name("lst"), scanBody)
            Assign(Name("total"), Int(1))
            While(
              Compare(Name("largest"), CmpOp(">", Int(0))),
              digitLoopBody)
            Return(Name("total")))))
      ~> Call(
           Name("skjkasdkd"),
           list(vCons(2, .ValSeq)))
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "skjkasdkd" |->
             closureVal(
               ("lst", .ParamNames),
               Assign(Name("largest"), Int(0))
               Assign(Name("value"), Int(0))
               Assign(Name("candidate"), Bool(false))
               Assign(Name("divisor"), Int(2))
               For(Name("value"), Name("lst"), scanBody)
               Assign(Name("total"), Int(1))
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
