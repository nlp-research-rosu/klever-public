requires "semantic.k"

module VERIFICATION-LABELED
  imports SEMANTIC

  claim [helper-positive-head]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => cons(I, filterGt(REST, 0)) </k>
          <input> cons(I, REST) </input>
        </py>
    requires I >Int 0

  claim [helper-nonpositive-head]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => filterGt(REST, 0) </k>
          <input> cons(I, REST) </input>
        </py>
    requires I <=Int 0

  claim [helper-empty]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => nil </k>
          <input> nil </input>
        </py>
endmodule
