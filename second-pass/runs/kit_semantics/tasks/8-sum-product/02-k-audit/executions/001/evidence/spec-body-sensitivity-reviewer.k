requires "verification.k"

module SPEC-BODY-SENSITIVITY-REVIEWER
  imports VERIFICATION

  // The program term actually executed has product initialized to 2 in both
  // the loaded module and the binding asserted after loading. The unchanged
  // contract still demands the empty-list result (0, 1), so fixed execution
  // must reject this claim with the actual result (0, 2).
  claim [mutated-body-empty]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List", "Tuple")
        FuncDef("sum_product", Params("numbers"),
          Assign(Name("total"), Int(0))
          Assign(Name("product"), Int(2))
          For(Name("number"), Name("numbers"),
            AugAssign(Name("total"), "+", Name("number"))
            AugAssign(Name("product"), "*", Name("number")))
          Return(TupleExpr(Name("total"), Name("product"))))
      ))
      ~> Call(Name("sum_product"), list(.ValSeq))
      =>
      tuple(vCons(0, vCons(1, .ValSeq)))
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
