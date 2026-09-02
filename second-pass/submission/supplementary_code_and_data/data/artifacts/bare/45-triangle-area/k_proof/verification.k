requires "semantic.k"

module VERIFICATION
  imports TINY-PYTHON

  // This is exactly the constructor tree generated in solution.mpy.  Naming
  // it keeps the reachability claims legible without bypassing interpretation.
  syntax Stmt ::= "triangleProgram"
  rule triangleProgram =>
    Module(FuncDef("triangle_area", Params("a", "h"),
      Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Int(2)))))
endmodule
