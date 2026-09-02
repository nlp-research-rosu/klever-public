requires "semantic.k"

module MUTATION-SPEC
  imports MPY
  imports VERIFICATION

  // Expected to fail: three equal values expose the weakened <= 3 mutation.
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
                      CmpOp("<=", Int(3))),
                    CompFor(Name("x"), Name("lst"), Bool(true)))))))),
        PyList(Cons(2, Cons(2, Cons(2, Nil)))))
      => BoolVal(isSortedContract(Cons(2, Cons(2, Cons(2, Nil)))))
    </k>
endmodule
