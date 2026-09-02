requires "semantic.k"

module BODY-SENSITIVITY-SPEC
  imports MPY
  imports VERIFICATION

  // Independent operational-sensitivity mutation: replace sorted(lst) with
  // lst in the program body.  On [1, 0] the mutant returns true while the
  // original contract is false.
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
                  CmpOp("==", Name("lst"))),
                Call(
                  Name("all"),
                  GenExp(
                    Compare(
                      Call(Attribute(Name("lst"), "count"), Name("x")),
                      CmpOp("<=", Int(2))),
                    CompFor(Name("x"), Name("lst"), Bool(true)))))))),
        PyList(Cons(1, Cons(0, Nil))))
      => BoolVal(isSortedContract(Cons(1, Cons(0, Nil))))
    </k>
endmodule
