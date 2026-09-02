requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-result]:
    <k>
      Call(Name("is_nested"), str(.IntSeq))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "is_nested" |-> closureVal(
          "string", .ParamNames,
          Assign(Name("state"), Int(0))
          Assign(Name("bracket"), Str(""))
          For(Name("bracket"), Name("string"),
            If(Compare(Name("state"), CmpOp("<", Int(2))),
              If(Compare(Name("bracket"), CmpOp("==", Str("["))),
                AugAssign(Name("state"), "+", Int(1)),
                .Stmts),
              If(Compare(Name("state"), CmpOp("<", Int(4))),
                If(Compare(Name("bracket"), CmpOp("==", Str("]"))),
                  AugAssign(Name("state"), "+", Int(1)),
                  .Stmts),
                .Stmts))
            .Stmts)
          Return(Compare(Name("state"), CmpOp("==", Int(4))))
          .Stmts,
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
