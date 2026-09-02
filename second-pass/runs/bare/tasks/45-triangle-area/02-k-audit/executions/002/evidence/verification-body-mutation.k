requires "semantic.k"

module VERIFICATION-BODY-MUTATION
  imports TINY-PYTHON

  syntax Stmt ::= "triangleProgramMutated"
  rule triangleProgramMutated =>
    Module(FuncDef("triangle_area", Params("a", "h"),
      Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Int(3)))))
endmodule
