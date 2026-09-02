requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable witness eat(5, 6, 10):
  // the first result element is mutated from 11 to 12.
  claim [false-result]:
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
                BinOp("+", Name("number"), Name("need")),
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
      0 |-> list(vCons(12, vCons(4, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
