requires "verification.k"

module BODY-SENSITIVITY-MUTATION
  imports VERIFICATION

  // False for [2, 3]: change the real body from (sum, prod) to (sum, sum),
  // but retain the original result obligation (5, 6).
  claim
    <k>
      Module(
        ImportFrom("typing", "List", "Tuple")
        ImportFrom("math", "prod")
        FuncDef("sum_product", Params("numbers"),
          Return(
            TupleExpr(
              Call(Name("sum"), Name("numbers")),
              Call(Name("sum"), Name("numbers"))))))
      => .K
    </k>
    <input> PyList(2, 3, .Ints) </input>
    <functions>
      .Map
      => "sum_product" |-> Closure(
           "numbers",
           TupleExpr(
             Call(Name("sum"), Name("numbers")),
             Call(Name("sum"), Name("numbers"))))
    </functions>
    <result> .K => PyTuple(PyInt(5), PyInt(6)) </result>
endmodule
