requires "/tmp/audit-work/source/verification.k"

module BODY-SENSITIVITY-SPEC
  imports VERIFICATION

  claim [mutated-product-initializer]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List", "Tuple")
          FuncDef(
            "sum_product",
            Params("numbers"),
            Assign(Name("sum_value"), Int(0))
            Assign(Name("product_value"), Int(0))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("numbers"),
              AugAssign(Name("sum_value"), "+", Name("number"))
              AugAssign(Name("product_value"), "*", Name("number"))
            )
            Return(TupleExpr(Name("sum_value"), Name("product_value")))
          )
        )
      )
      ~> Call(Name("sum_product"), list(intListVals(.IntList)))
      => tuple(vCons(0, vCons(1, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        .Map
        => "sum_product" |-> closureVal(
             "numbers",
             Assign(Name("sum_value"), Int(0))
             Assign(Name("product_value"), Int(0))
             Assign(Name("number"), Int(0))
             For(
               Name("number"),
               Name("numbers"),
               AugAssign(Name("sum_value"), "+", Name("number"))
               AugAssign(Name("product_value"), "*", Name("number"))
             )
             Return(TupleExpr(Name("sum_value"), Name("product_value"))),
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
