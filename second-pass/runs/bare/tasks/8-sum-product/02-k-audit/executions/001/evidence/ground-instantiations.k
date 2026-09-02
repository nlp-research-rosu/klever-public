requires "verification.k"

module GROUND-INSTANTIATIONS
  imports VERIFICATION

  claim [empty]:
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
    <input> PyList(.Ints) </input>
    <functions>
      .Map
      => "sum_product" |-> Closure(
           "numbers",
           TupleExpr(
             Call(Name("sum"), Name("numbers")),
             Call(Name("prod"), Name("numbers"))))
    </functions>
    <result> .K => PyTuple(PyInt(0), PyInt(1)) </result>

  claim [four-elements]:
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
    <result> .K => PyTuple(PyInt(10), PyInt(24)) </result>
endmodule
