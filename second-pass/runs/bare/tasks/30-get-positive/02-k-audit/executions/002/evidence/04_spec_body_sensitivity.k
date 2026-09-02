requires "semantic.k"

module SPEC-BODY-SENSITIVITY
  imports SEMANTIC

  // The executed program term is materially changed from x > 0 to x > 1,
  // while the original expected answer for [1] is retained.
  claim [changed-threshold]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(1))))))))
            => cons(1, nil) </k>
          <input> cons(1, nil) </input>
        </py>
endmodule
