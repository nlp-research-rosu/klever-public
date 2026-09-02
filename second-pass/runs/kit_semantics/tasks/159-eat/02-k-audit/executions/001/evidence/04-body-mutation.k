requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Reachable witness: this changed body adds one extra carrot in the taken
  // enough-stock branch, but the destination retains the real program result.
  claim [changed-executed-body]:
    <k> Call(Name("eat"), Int(5), Int(6), Int(10)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "eat" |-> closureVal(
          "number", "need", "remaining", .ParamNames,
          If(
            Compare(Name("need"), CmpOp("<=", Name("remaining"))),
            Return(
              ListExpr(
                BinOp(
                  "+",
                  BinOp("+", Name("number"), Name("need")),
                  Int(1)
                ),
                BinOp("-", Name("remaining"), Name("need"))
              )
            ),
            .Stmts
          )
          Return(
            ListExpr(
              BinOp("+", Name("number"), Name("remaining")),
              Int(0)
            )
          ),
          0
        ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(11, vCons(4, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
