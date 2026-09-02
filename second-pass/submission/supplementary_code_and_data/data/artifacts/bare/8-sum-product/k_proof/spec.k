requires "verification.k"

module SUM-PRODUCT-SPEC
  imports VERIFICATION

  claim
    <k>
      Module(
        ImportFrom("typing", "List", "Tuple")
        ImportFrom("math", "prod")
        FuncDef("sum_product", Params("numbers"),
          Return(
            TupleExpr(
              Call(Name("sum"), Name("numbers")),
              Call(Name("prod"), Name("numbers"))))))
      => .K
    </k>
    <input> PyList(IS) </input>
    <functions>
      .Map
      => "sum_product" |-> Closure(
           "numbers",
           TupleExpr(
             Call(Name("sum"), Name("numbers")),
             Call(Name("prod"), Name("numbers"))))
    </functions>
    <result> .K => expectedSumProduct(IS) </result>
endmodule
