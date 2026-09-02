requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated implementation: product starts at 2.  The expected
  // empty-list result remains the source contract's (0, 1), so proof must fail.
  claim [mutated-body]:
    <k>
      Call(Name("sum_product"), list(.ValSeq))
      =>
      tuple(vCons(0, vCons(1, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "sum_product" |->
          closureVal(
            "numbers", .ParamNames,
            Assign(Name("total"), Int(0))
            Assign(Name("product"), Int(2))
            For(Name("number"), Name("numbers"),
              AugAssign(Name("total"), "+", Name("number"))
              AugAssign(Name("product"), "*", Name("number")))
            Return(TupleExpr(Name("total"), Name("product"))),
            0
          ),
        parent(-1)
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
