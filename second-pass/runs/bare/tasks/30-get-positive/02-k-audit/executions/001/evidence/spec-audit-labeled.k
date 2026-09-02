requires "verification.k"

// Reviewer-authored label-only duplicate of every candidate positive claim.
// Labels permit one kprove invocation per original claim.
module AUDIT-VERIFICATION
  imports SEMANTIC

  claim [label(helper-positive-head)]:
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

  claim [label(helper-nonpositive-head)]:
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

  claim [label(helper-empty)]:
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

module AUDIT-SPEC
  imports VERIFICATION

  claim [label(spec-universal)]:
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

  claim [label(spec-example-1)]:
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

  claim [label(spec-example-2)]:
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

  claim [label(spec-empty)]:
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

  claim [label(spec-all-nonpositive)]:
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
