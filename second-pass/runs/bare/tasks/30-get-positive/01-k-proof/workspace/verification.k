requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Symbolic boundary obligations run the actual translated program.  The
  // tail stays arbitrary, so these claims cover every possible first step.
  claim <py>
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

  claim <py>
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
endmodule
