requires "verification.k"

module SPEC-FRESH-VACUITY-REVIEWER
  imports VERIFICATION

  // Fresh reviewer mutation. The exact submitted program executes on the
  // satisfying input [2, -3, 4], whose true result is (3, -24). Only the
  // result-constraining sum obligation is changed to the false value 4.
  claim [fresh-false-result]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List", "Tuple")
        FuncDef("sum_product", Params("numbers"),
          Assign(Name("total"), Int(0))
          Assign(Name("product"), Int(1))
          For(Name("number"), Name("numbers"),
            AugAssign(Name("total"), "+", Name("number"))
            AugAssign(Name("product"), "*", Name("number")))
          Return(TupleExpr(Name("total"), Name("product"))))
      ))
      ~> Call(Name("sum_product"),
              list(vCons(2, vCons(-3, vCons(4, .ValSeq)))))
      =>
      tuple(vCons(4, vCons(-24, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        .Map
        =>
        "sum_product" |->
          closureVal(
            "numbers", .ParamNames,
            Assign(Name("total"), Int(0))
            Assign(Name("product"), Int(1))
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
