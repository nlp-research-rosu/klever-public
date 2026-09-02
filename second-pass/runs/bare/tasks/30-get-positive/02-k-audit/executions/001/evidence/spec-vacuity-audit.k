requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for INPUT = nil the real program returns nil, not
  // cons(1, nil).  This mutates the universal result-bearing obligation.
  claim [label(false-extra-positive)]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => cons(1, filterGt(INPUT, 0)) </k>
          <input> INPUT:PyList </input>
        </py>
endmodule
