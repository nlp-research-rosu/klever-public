requires "verification.k"

module SUM-PRODUCT-SPEC-BODY-MUTATION
  imports VERIFICATION

  // Reviewer mutation: the executed body now returns product as both fields.
  // The destination closure is changed in parallel so failure tests the
  // unchanged result obligation rather than closure bookkeeping.
  claim
    <k>
      Module(
        ImportFrom("typing", "List", "Tuple")
        ImportFrom("math", "prod")
        FuncDef("sum_product", Params("numbers"),
          Return(
            TupleExpr(
              Call(Name("prod"), Name("numbers")),
              Call(Name("prod"), Name("numbers"))))))
      => .K
    </k>
    <input> PyList(IS) </input>
    <functions>
      .Map
      => "sum_product" |-> Closure(
           "numbers",
           TupleExpr(
             Call(Name("prod"), Name("numbers")),
             Call(Name("prod"), Name("numbers"))))
    </functions>
    <result> .K => expectedSumProduct(IS) </result>
endmodule
