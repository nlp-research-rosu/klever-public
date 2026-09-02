requires "continuation-test.k"

module CONTINUATION-SPEC
  imports CONTINUATION-TEST

  // The observable suffix must remain after both candidate semantic bridges.
  claim [suffix-preserved]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
               ~> observe
            => observed(cons(2, nil)) </k>
          <input> cons(-1, cons(2, nil)) </input>
        </py>
endmodule
