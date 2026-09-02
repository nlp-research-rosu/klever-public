requires "semantic.k"

module FRESH-VACUITY-SPEC
  imports MPY
  imports VERIFICATION

  // Fresh false postcondition: the real program returns true for the empty
  // list, so requiring false changes a result-bearing obligation.
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
        PyList(Nil))
      => BoolVal(false)
    </k>
endmodule
