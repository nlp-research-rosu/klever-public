requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal functional-correctness summary: execution of the translated
  // program returns the stable strict-positive projection for every input.
  claim <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => filterGt(INPUT, 0) </k>
          <input> INPUT:PyList </input>
        </py>

  // The two examples from prompt.py, plus empty and all-nonpositive edges.
  claim <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => cons(2, cons(5, cons(6, nil))) </k>
          <input> cons(-1, cons(2, cons(-4, cons(5, cons(6, nil))))) </input>
        </py>

  claim <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => cons(5, cons(3, cons(2, cons(3, cons(9, cons(123, cons(1, nil))))))) </k>
          <input> cons(5, cons(3, cons(-5, cons(2, cons(-3, cons(3, cons(9, cons(0, cons(123, cons(1, cons(-10, nil))))))))))) </input>
        </py>

  claim <py>
          <k> Module(
                FuncDef("get_positive", Params("l"),
                  Return(
                    ListComp(Name("x"),
                      CompFor(Name("x"), Name("l"),
                        Compare(Name("x"), CmpOp(">", Int(0))))))))
            => nil </k>
          <input> nil </input>
        </py>

  claim <py>
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
