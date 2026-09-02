requires "semantic.k"

module AUDIT-FALSE-SPEC
  imports MPY
  imports VERIFICATION

  // Reviewer-authored body-sensitive false mutation.
  // For [0, 0], the submitted <= 2 body and contract return true.
  // This executed term instead uses <= 1, so it returns false while the
  // unchanged original result obligation remains true.
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
                      CmpOp("<=", Int(1))),
                    CompFor(Name("x"), Name("lst"), Bool(true)))))))),
        PyList(Cons(0, Cons(0, Nil))))
      => BoolVal(isSortedContract(Cons(0, Cons(0, Nil))))
    </k>
endmodule
