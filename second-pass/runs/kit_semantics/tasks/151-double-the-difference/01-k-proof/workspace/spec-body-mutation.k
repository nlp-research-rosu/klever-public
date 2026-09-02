requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The source body is materially changed from number*number to number+number.
  // On [1] it returns 2, so the original required result 1 must be rejected.
  claim [changed-body-rejected]:
    <k>
      Call(Name("double_the_difference"),
        (list(vCons(1, .ValSeq)), .Exprs))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "double_the_difference" |->
          closureVal(("lst", .ParamNames),
            Assign(Name("result"), Int(0))
            Assign(Name("number"), Int(0))
            For(Name("number"), Name("lst"),
              If(Call(Name("isinstance"),
                      (Name("number"), Name("int"), .Exprs)),
                If(Compare(Name("number"), CmpOp(">", Int(0))),
                  If(Compare(BinOp("%", Name("number"), Int(2)),
                             CmpOp("==", Int(1))),
                    AugAssign(Name("result"), "+",
                              BinOp("+", Name("number"), Name("number"))),
                    .Stmts),
                  .Stmts),
                .Stmts))
            Return(Name("result")),
            0),
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
