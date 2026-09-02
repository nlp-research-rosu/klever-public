requires "verification.k"

module SUM-PRODUCT-SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Reviewer-authored false postcondition: sum is required to be one larger.
  // The empty-list witness satisfies the precondition, executes to (0, 1),
  // and contradicts this destination (1, 1).
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
    <result>
      .K
      => PyTuple(
           PyInt(sumInts(IS) +Int 1),
           PyInt(productInts(IS)))
    </result>
endmodule
