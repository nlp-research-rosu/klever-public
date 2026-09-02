requires "semantic.k"

module SHADOWING-FALSE-CLAIM
  imports MPY

  // The trusted translator emits this term for shadowing_witness.py.  CPython
  // raises AttributeError on [1], but the over-broad fused rule proves true.
  claim
    <k>
      Run(
        Module(
          FuncDef("is_sorted", Params("lst"), CellVars("lst"), FreeVars(),
            Return(
              BoolOp(
                "and",
                Call(
                  Name("all"),
                  GenExp(
                    Compare(
                      Call(Attribute(Name("lst"), "count"), Name("lst")),
                      CmpOp("<=", Int(2))),
                    CompFor(Name("lst"), Name("lst"), Bool(true)))),
                Call(
                  Name("all"),
                  GenExp(
                    Compare(
                      Call(Attribute(Name("lst"), "count"), Name("x")),
                      CmpOp("<=", Int(2))),
                    CompFor(Name("x"), Name("lst"), Bool(true)))))))),
        PyList(Cons(1, Nil)))
      => BoolVal(true)
    </k>
endmodule
