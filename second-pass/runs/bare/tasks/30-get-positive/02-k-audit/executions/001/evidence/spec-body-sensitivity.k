requires "verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // Deliberately changes the submitted comparison threshold from 0 to 1 while
  // retaining the original postcondition.  INPUT = cons(1, nil) witnesses the
  // mismatch: the changed program yields nil, while filterGt(INPUT, 0) is
  // cons(1, nil).
  claim [label(changed-threshold)]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(1))))))))
            => filterGt(INPUT, 0) </k>
          <input> INPUT:PyList </input>
        </py>
endmodule
