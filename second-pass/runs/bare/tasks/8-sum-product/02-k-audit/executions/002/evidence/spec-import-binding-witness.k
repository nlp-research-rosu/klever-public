requires "verification.k"

module SUM-PRODUCT-SPEC-IMPORT-BINDING-WITNESS
  imports VERIFICATION

  // This differs from the submitted program: typing does not export prod.
  // A Python implementation fails during import, but the candidate K semantics
  // erases the import and resolves textual Name("prod") as math.prod anyway.
  claim
    <k>
      Module(
        ImportFrom("typing", "List", "Tuple")
        ImportFrom("typing", "prod")
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
