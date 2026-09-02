requires "verification.k"

module FALSE-POSTCONDITION-MUTATION
  imports VERIFICATION

  // The exact submitted program returns (10, 24) on this satisfying input.
  // This mutation changes only the result-constraining sum to the false 11.
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
    <input> PyList(1, 2, 3, 4, .Ints) </input>
    <functions>
      .Map
      => "sum_product" |-> Closure(
           "numbers",
           TupleExpr(
             Call(Name("sum"), Name("numbers")),
             Call(Name("prod"), Name("numbers"))))
    </functions>
    <result> .K => PyTuple(PyInt(11), PyInt(24)) </result>
endmodule
