requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Original body returns 1 on [1]. This closure term materially changes the
  // multiplication to addition, so its real execution returns 2.
  claim [changed-body-rejects-original-result]:
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
          closureVal(
            ("lst", .ParamNames),
            Assign(Name("result"), Int(0))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("lst"),
              If(
                Call(
                  Name("isinstance"),
                  (Name("number"), Name("int"), .Exprs)),
                If(
                  Compare(Name("number"), CmpOp(">", Int(0))),
                  If(
                    Compare(
                      BinOp("%", Name("number"), Int(2)),
                      CmpOp("==", Int(1))),
                    AugAssign(
                      Name("result"),
                      "+",
                      BinOp(
                        "+",
                        Name("number"),
                        Name("number"))),
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
