requires "semantic.k"

module SPEC-VACUITY
  imports SEMANTIC

  // Deliberately false: the unchanged submitted program retains 1.
  // The satisfying input [1] is inside the original universal precondition.
  claim [wrong-result]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => nil </k>
          <input> cons(1, nil) </input>
        </py>
endmodule
