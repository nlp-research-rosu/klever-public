requires "verification-labeled.k"

module SPEC-LABELED
  imports VERIFICATION-LABELED

  claim [universal]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => filterGt(INPUT, 0) </k>
          <input> INPUT:PyList </input>
        </py>

  claim [example-one]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => cons(2, cons(5, cons(6, nil))) </k>
          <input> cons(-1, cons(2, cons(-4, cons(5, cons(6, nil))))) </input>
        </py>

  claim [example-two]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => cons(5, cons(3, cons(2, cons(3, cons(9, cons(123, cons(1, nil))))))) </k>
          <input> cons(5, cons(3, cons(-5, cons(2, cons(-3, cons(3, cons(9, cons(0, cons(123, cons(1, cons(-10, nil))))))))))) </input>
        </py>

  claim [empty]:
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

  claim [all-nonpositive]:
        <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => nil </k>
          <input> cons(0, cons(-1, cons(-2, nil))) </input>
        </py>
endmodule
