requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION-BASE

  // Fresh reviewer mutation. The exact body returns (6, 0) on
  // [-2, 3, 0, 5], so requiring (6, 1) changes a reachable result obligation.
  claim [wrong-product-ground]:
    <k>
      #applyK(
        toCall(
          closureVal(
            ("numbers", .ParamNames),
            Assign(Name("total"), Int(0))
            Assign(Name("product"), Int(1))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("numbers"),
              AugAssign(Name("total"), "+", Name("number"))
              AugAssign(Name("product"), "*", Name("number"))
            )
            Return(TupleExpr(Name("total"), Name("product"))),
            0
          )
        ),
        (list(vCons(-2,
              vCons(3,
              vCons(0,
              vCons(5, .ValSeq))))), .Vals)
      )
      =>
      tuple(vCons(6, vCons(1, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "sum_product" |->
          closureVal(
            ("numbers", .ParamNames),
            Assign(Name("total"), Int(0))
            Assign(Name("product"), Int(1))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("numbers"),
              AugAssign(Name("total"), "+", Name("number"))
              AugAssign(Name("product"), "*", Name("number"))
            )
            Return(TupleExpr(Name("total"), Name("product"))),
            0
          ),
        parent(-1)
      )
      -1 |-> _BUILTINS:Scope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
