requires "semantic.k"

module SPEC
  imports MPY
  imports VERIFICATION

  // Universal functional-correctness claim: IS is an arbitrary integer list.
  // The left side is the exact constructor tree emitted in solution.mpy.
  claim
    <k>
      Run(
        Module(
          FuncDef("is_sorted", Params("lst"), CellVars("lst"), FreeVars(),
            Return(
              BoolOp(
                "and",
                Compare(
                  Name("lst"),
                  CmpOp("==", Call(Name("sorted"), Name("lst")))),
                Call(
                  Name("all"),
                  GenExp(
                    Compare(
                      Call(Attribute(Name("lst"), "count"), Name("x")),
                      CmpOp("<=", Int(2))),
                    CompFor(Name("x"), Name("lst"), Bool(true)))))))),
        PyList(IS))
      => BoolVal(isSortedContract(IS))
    </k>
endmodule
