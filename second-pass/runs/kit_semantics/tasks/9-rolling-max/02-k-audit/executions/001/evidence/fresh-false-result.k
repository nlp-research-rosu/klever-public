requires "verification.k"

module FRESH-FALSE-RESULT
  imports VERIFICATION

  // Fresh auditor mutation. The satisfying input [1,-2,3,2] really returns
  // [1,1,3,3], but this postcondition changes the result obligation to
  // [1,1,4,4].
  claim [wrong-third-rolling-maximum]:
    <k>
      Call(
        Name("rolling_max"),
        (list(vCons(1, vCons(-2, vCons(3, vCons(2, .ValSeq))))), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "rolling_max" |->
          closureVal(
            ("numbers", .ParamNames),
            Expr(Str("Return the maximum seen at each position in numbers."))
            Assign(Name("result"), ListExpr(.Exprs))
            If(
              Name("numbers"),
              Assign(
                Name("current"),
                Subscript(Name("numbers"), Int(0)))
              Assign(Name("number"), Name("current"))
              For(
                Name("number"),
                Name("numbers"),
                If(
                  Compare(
                    Name("number"),
                    CmpOp(">", Name("current"))),
                  Assign(Name("current"), Name("number")) .Stmts,
                  .Stmts)
                Expr(Call(
                  Attribute(Name("result"), "append"),
                  (Name("current"), .Exprs))) .Stmts)
              .Stmts,
              .Stmts)
            Return(Name("result")) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(1, vCons(1, vCons(4, vCons(4, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
